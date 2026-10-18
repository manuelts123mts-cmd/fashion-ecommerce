# -*- coding: utf-8 -*-
"""M&C · Ensambla la Fase 1 editorial y conserva catálogo/admin existentes.

Fuentes editables: src/. Salidas: web/index.html y tienda_portable.html.
Sin framework de runtime, CDN, carrito, checkout ni dependencias de pagos.
El contrato de importación se mantiene para build_admin.py.
"""
from pathlib import Path
import base64
import html
import json
import mimetypes
import re
import shutil

ROOT = Path(__file__).resolve().parent
WEB = ROOT / 'web'
SRC = ROOT / 'src'


def read(path):
    return Path(path).read_text(encoding='utf-8')


def b64file(path, mime=None):
    """Recurso autocontenido para la versión offline y la plantilla del admin."""
    path = Path(path)
    if not path.is_absolute():
        path = ROOT / path
    mime = mime or mimetypes.guess_type(str(path))[0] or 'application/octet-stream'
    return 'data:%s;base64,%s' % (mime, base64.b64encode(path.read_bytes()).decode('ascii'))


def load_json(path):
    return json.loads(read(path))


logo_b64 = b64file(WEB / 'assets/home/brand-logo.webp')
hero_b64 = b64file(WEB / 'assets/home/hero-1088.webp')
PRODUCTOS = load_json(WEB / 'data/productos.json')
CSS = read(SRC / 'legacy/store.css')
STORE_JS = read(SRC / 'legacy/store.js')
HOME = load_json(SRC / 'data/home.json')
LOOKS = load_json(SRC / 'data/looks.json')['looks']
HEADER_CATEGORIES = load_json(SRC / 'data/categories.json')['categories']
CATEGORIES = {c['id']: c['label'] for c in HEADER_CATEGORIES}


def esc(value):
    return html.escape(str(value), quote=True)


def optimized_product_path(product):
    """La foto se conserva: solo cambia el formato de archivo, no el contenido."""
    original = product.get('imagen', '')
    # Un producto editado con una nueva imagen no debe recuperar una antigua WebP.
    expected = next((p.get('imagen') for p in PRODUCTOS if p['id'] == product['id']), None)
    candidate = WEB / 'assets/catalog' / (product['id'] + '.webp')
    if original == expected and candidate.exists():
        return '/assets/catalog/' + candidate.name
    return original


def asset(path, portable):
    if str(path).startswith('data:'):
        return path
    local = WEB / str(path).lstrip('/')
    return b64file(local) if portable and local.exists() else str(path)


def arrival_card(p, portable):
    image = asset(optimized_product_path(p), portable)
    category = CATEGORIES.get(p.get('categoria'), 'Colección')
    tag = '<span class="arrival-card__tag">Nuevo</span>' if p.get('nuevo') else ''
    return f'''<article class="arrival-card">
  <a class="arrival-card__link" href="#catalogo" data-home-product="{esc(p['id'])}" aria-label="Ver prenda: {esc(p['nombre'])}">
    <span class="arrival-card__visual"><img src="{esc(image)}" alt="{esc(p['nombre'])} — fotografía del catálogo" width="450" height="600" loading="lazy" fetchpriority="low" decoding="async">{tag}<span class="arrival-card__arrow" aria-hidden="true">↗</span></span>
    <span class="arrival-card__category">{esc(category)}</span><h3>{esc(p['nombre'])}</h3><span class="arrival-card__note">Precio por consulta</span>
  </a>
</article>'''


def look_card(look, portable):
    return f'''<article class="look-card reveal" data-look-card="{esc(look['id'])}">
  <a class="look-card__image" href="#looks" data-look-open="{esc(look['id'])}" aria-label="Explorar el look completo: {esc(look['title'])}">
    <img src="{esc(asset(look['image'], portable))}" alt="{esc(look['title'])} — recreación editorial con IA de un outfit completo" width="928" height="1152" loading="lazy" fetchpriority="low" decoding="async"><span class="look-card__number" aria-hidden="true">{esc(look['number'])}</span>
  </a>
  <span class="look-card__image-note">Recreación editorial con IA · propuesta de estilismo</span>
  <div class="look-card__bottom"><div><h3>{esc(look['title'])}</h3><p class="look-card__subtitle">{esc(look['subtitle'])}</p></div><button class="icon-button look-card__open" type="button" data-look-open="{esc(look['id'])}" aria-label="Ver las prendas del look: {esc(look['title'])}"><span aria-hidden="true">↗</span></button></div>
</article>'''


def home_config(portable):
    """Solo datos editoriales. Los mocks de reseñas/tiendas NUNCA se publican."""
    return {
        'featuredIds': HOME['featuredIds'], 'whatsapp': HOME['whatsapp'],
        'looks': [{k: v for k, v in item.items() if k != 'image'} for item in LOOKS],
        'imageMap': {} if portable else {p['imagen']: optimized_product_path(p) for p in PRODUCTOS}
    }


def category_links():
    """HTML semántico prerenderizado; los conteos se actualizan con el API/admin."""
    active=[p for p in PRODUCTOS if p.get('activo')]
    items=[{'id':'all','label':'Todo'}]+HEADER_CATEGORIES
    result=[]
    for item in items:
        key,label=item['id'],item['label']
        count=len(active) if key=='all' else sum((p.get('categoria') or 'tops')==key for p in active)
        target='#catalogo' if key=='all' else '#categoria-'+key
        current=' aria-current="page"' if key=='all' else ''
        result.append(f'''<li class="category-item" data-category-item="{esc(key)}"><a class="category-link chip" href="?cat={esc(key)}{target}" data-category="{esc(key)}" title="{esc(label)}"{current}><span class="category-link__label">{esc(label)}</span><span class="category-count">({count})</span></a><button class="category-expand" type="button" data-mega-for="{esc(key)}" aria-expanded="false" aria-controls="category-mega" aria-label="Abrir submenú de {esc(label)}"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg></button></li>''')
    return '\n'.join(result)


def hero_resources(portable=True, hero_source=None):
    """Responsive + preload sin duplicar transferencias; ningún cálculo de altura JS.

    Fallback vertical móvil; source usa un recorte del MISMO archivo en desktop.
    En portable se incrustan ambos encuadres, sin preloads data: redundantes.
    """
    alt = 'Dos personas modelando ropa urbana en La Paz, con el Illimani al fondo'
    hero = hero_source or (hero_b64 if portable else '/assets/home/hero-1088.webp')
    if hero_source:
        # Respeta el contrato anterior si un consumidor aporta otra imagen.
        return (f'<picture><img id="hero-image" src="{esc(hero)}" alt="{alt}" width="1088" height="1360" fetchpriority="high" loading="eager" decoding="async"></picture>', '')
    mobile_set = '/assets/home/hero-640.webp 640w, /assets/home/hero-1088.webp 1088w'
    wide_set = '/assets/home/hero-wide-768.webp 768w, /assets/home/hero-wide-1088.webp 1088w'
    # cover puede dibujar una foto MÁS ancha que el viewport: se dimensiona srcset.
    mobile_sizes, wide_sizes = 'max(100vw, 64svh, 448px)', 'max(100vw, 107svh)'
    wide = asset('/assets/home/hero-wide-1088.webp', portable)
    source = f'<source media="(min-width: 768px)" srcset="{esc(wide if portable else wide_set)}"'
    source += '' if portable else f' sizes="{wide_sizes}"'
    source += ' width="1088" height="816">'
    attrs = '' if portable else f' srcset="{mobile_set}" sizes="{mobile_sizes}"'
    picture = f'<picture>{source}<img id="hero-image" src="{esc(hero)}"{attrs} alt="{alt}" width="1088" height="1360" fetchpriority="high" loading="eager" decoding="async"></picture>'
    if portable:
        return picture, ''
    hints = f'''<link rel="preload" as="image" type="image/webp" href="/assets/home/hero-1088.webp" imagesrcset="{mobile_set}" imagesizes="{mobile_sizes}" media="(max-width: 767.98px)" fetchpriority="high">
<link rel="preload" as="image" type="image/webp" href="/assets/home/hero-wide-1088.webp" imagesrcset="{wide_set}" imagesizes="{wide_sizes}" media="(min-width: 768px)" fetchpriority="high">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/editorial.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/sans.woff2" crossorigin>'''
    return picture, hints


def store_html(hero_source=None, portable=True):
    """HTML base. Por defecto, todo incrustado para exportar desde el admin."""
    tokens = read(SRC / 'styles/tokens.css')
    tokens = tokens.replace('__FONT_EDITORIAL__', asset('/assets/fonts/editorial.woff2', portable))
    tokens = tokens.replace('__FONT_SANS__', asset('/assets/fonts/sans.woff2', portable))
    # Override estrictamente móvil. Fuente comentada; salida compacta sin dependencias.
    # Los marcadores permiten aislarlo en pruebas de regresión del escritorio.
    mobile_css = ' '.join(re.sub(r'/\*.*?\*/', '', read(SRC / 'styles/mobile-header.css'), flags=re.S).split())
    mobile_header = '\n/* MC_MOBILE_HEADER_START */\n' + mobile_css + '\n/* MC_MOBILE_HEADER_END */\n'
    styles = CSS + '\n' + tokens + '\n' + read(SRC / 'styles/home.css') + '\n' + read(SRC / 'styles/hero-restored.css') + '\n' + read(SRC / 'styles/sticky-header.css') + mobile_header
    picture, hints = hero_resources(portable=portable, hero_source=hero_source)
    active = [p for p in PRODUCTOS if p.get('activo')]
    selected = [p for pid in HOME['featuredIds'] for p in active if p['id'] == pid]
    home_html = read(SRC / 'home/home.html')
    home_html = home_html.replace('__HERO_PICTURE__', picture)
    home_html = home_html.replace('__ARRIVAL_CARDS__', '\n'.join(arrival_card(p, portable) for p in selected))
    home_html = home_html.replace('__LOOK_CARDS__', '\n'.join(look_card(look, portable) for look in LOOKS))
    home_html = home_html.replace('__FIRST_LOOK_IMAGE__', asset(LOOKS[0]['image'], portable))
    data = json.dumps(home_config(portable), ensure_ascii=False).replace('<', '\\u003c')
    category_bar=read(SRC / 'components/category-bar.html').replace('__CATEGORY_LINKS__',category_links())
    header=read(SRC / 'components/header.html').replace('__CATEGORY_BAR__',category_bar)
    header_data=json.dumps({'categories':HEADER_CATEGORIES,'imageMap':home_config(portable)['imageMap']},ensure_ascii=False).replace('<','\\u003c')
    header_js=read(SRC / 'navigation/scroll-direction.js')+'\n'+read(SRC / 'scripts/sticky-header.js')
    return (read(SRC / 'shell.html').replace('__HOME__', home_html)
            .replace('__HEADER__',header).replace('__HEADER_DATA__',header_data).replace('__HEADER_JS__',header_js)
            .replace('__RESOURCE_HINTS__', hints).replace('__CSS__', styles).replace('__LOGO__', asset('/assets/home/brand-logo.webp', portable))
            .replace('__HOME_DATA__', data).replace('__JS__', STORE_JS)
            .replace('__HOME_JS__', read(SRC / 'scripts/home.js')))


def build():
    WEB.mkdir(exist_ok=True)
    # API local de administración conservada. Fallback JSON permite hosting estático.
    (WEB / 'index.html').write_text(store_html(portable=False).replace('__PRODUCTS__', 'null'), encoding='utf-8')
    portable_products = []
    for p in PRODUCTOS:
        public = dict(p)
        public.pop('precio', None)  # no se publican importes en la versión autocontenida
        public['imagen'] = asset(optimized_product_path(p), portable=True)
        portable_products.append(public)
    data = json.dumps(portable_products, ensure_ascii=False).replace('<', '\\u003c')
    portable = store_html().replace('__PRODUCTS__', data)
    (ROOT / 'tienda_portable.html').write_text(portable, encoding='utf-8')
    shutil.copyfile(ROOT / 'tienda_portable.html', ROOT / 'catalogo_web.html')
    print('Generados: web/index.html, tienda_portable.html y catalogo_web.html')
    print('Portable: %.2f MB · %d productos · 2 looks editoriales' % (len(portable.encode()) / 1024**2, len(portable_products)))

if __name__ == '__main__':
    build()
