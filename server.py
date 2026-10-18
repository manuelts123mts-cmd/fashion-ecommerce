#!/usr/bin/env python3
"""Servidor de la plataforma M&C Heart of a Warrior.
Sirve la tienda (index.html), el panel de administración (admin.html)
y una API JSON que persiste el catálogo en web/data/productos.json."""
import base64
import json
import os
import re
import threading
import uuid
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'web')
DATA = os.path.join(ROOT, 'data', 'productos.json')
IMG = os.path.join(ROOT, 'img')
LOCK = threading.Lock()

CAMPOS = ('nombre', 'descripcion', 'tallas', 'colores', 'precio', 'imagen', 'activo', 'categoria', 'nuevo')


def load():
    with open(DATA, encoding='utf-8') as f:
        return json.load(f)


def save(prods):
    tmp = DATA + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(prods, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DATA)


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=ROOT, **kw)

    # ---------- utilidades ----------
    def _json(self, code, obj):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        self.send_header('Cache-Control', 'no-store')
        self.end_headers()
        self.wfile.write(body)

    def _body(self):
        n = int(self.headers.get('Content-Length', 0))
        return json.loads(self.rfile.read(n) or b'{}')

    def _guardar_imagen(self, d, pid):
        """Si la imagen llega como data-URL (subida desde el admin), la escribe en web/img/."""
        img = d.get('imagen', '')
        if isinstance(img, str) and img.startswith('data:image'):
            m = re.match(r'data:image/(\w+);base64,(.+)', img, re.S)
            if m:
                ext = {'jpeg': 'jpg', 'jpg': 'jpg', 'png': 'png',
                       'webp': 'webp', 'gif': 'gif'}.get(m.group(1).lower(), 'jpg')
                nombre = 'up_%s.%s' % (pid or uuid.uuid4().hex[:8], ext)
                with open(os.path.join(IMG, nombre), 'wb') as f:
                    f.write(base64.b64decode(m.group(2)))
                d['imagen'] = '/img/' + nombre

    # ---------- API ----------
    def do_GET(self):
        if self.path == '/api/productos':
            with LOCK:
                return self._json(200, load())
        m = re.match(r'^/api/productos/([\w-]+)$', self.path)
        if m:
            with LOCK:
                for p in load():
                    if p['id'] == m.group(1):
                        return self._json(200, p)
            return self._json(404, {'error': 'no existe'})
        return super().do_GET()

    def _upsert(self, pid=None):
        try:
            d = self._body()
        except Exception:
            return self._json(400, {'error': 'JSON inválido'})
        self._guardar_imagen(d, pid)
        with LOCK:
            prods = load()
            if pid:
                old = next((p for p in prods if p['id'] == pid), None)
                if old is None:
                    return self._json(404, {'error': 'no existe'})
                for k in CAMPOS:
                    if k in d:
                        old[k] = d[k]
                out = old
                code = 200
            else:
                out = {
                    'id': uuid.uuid4().hex[:8],
                    'nombre': str(d.get('nombre') or 'Prenda sin nombre'),
                    'descripcion': str(d.get('descripcion') or ''),
                    'tallas': str(d.get('tallas') or ''),
                    'colores': str(d.get('colores') or ''),
                    'precio': float(d.get('precio') or 0),
                    'imagen': str(d.get('imagen') or '/img/placeholder.svg'),
                    'activo': bool(d.get('activo', True)),
                    'categoria': str(d.get('categoria') or 'tops'),
                    'nuevo': bool(d.get('nuevo', True)),
                }
                prods.append(out)
                code = 201
            save(prods)
        return self._json(code, out)

    def do_POST(self):
        if self.path == '/api/productos':
            return self._upsert()
        return self._json(404, {'error': 'no existe'})

    def do_PUT(self):
        m = re.match(r'^/api/productos/([\w-]+)$', self.path)
        if m:
            return self._upsert(m.group(1))
        return self._json(404, {'error': 'no existe'})

    def do_DELETE(self):
        m = re.match(r'^/api/productos/([\w-]+)$', self.path)
        if m:
            with LOCK:
                prods = load()
                antes = len(prods)
                prods = [p for p in prods if p['id'] != m.group(1)]
                save(prods)
            return self._json(200, {'ok': True, 'eliminados': antes - len(prods)})
        return self._json(404, {'error': 'no existe'})


if __name__ == '__main__':
    srv = ThreadingHTTPServer(('0.0.0.0', 8000), Handler)
    print('Plataforma M&C sirviendo en 0.0.0.0:8000', flush=True)
    srv.serve_forever()
