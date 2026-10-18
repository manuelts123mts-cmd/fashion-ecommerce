# -*- coding: utf-8 -*-
"""Genera el catálogo web autocontenido de M&C Heart of a Warrior."""
import base64, os

def b64(path):
    with open(path, 'rb') as f:
        return base64.b64encode(f.read()).decode()

logo = b64('uploads/image-1.png')

productos = [
    {
        'img': 'catalogo/imagenes/polera_oversize.jpg',
        'nombre': 'Polera oversize unisex',
        'desc': 'Corte holgado estilo streetwear, algodón pesado y cuello redondo. Incluye el emblema del corazón coronado de la marca.',
        'tallas': 'S – M – L – XL',
        'colores': 'Negro, blanco y rosa',
        'precio': 89,
    },
    {
        'img': 'catalogo/imagenes/jean_mom_fit.jpg',
        'nombre': 'Jean mom fit de dama',
        'desc': 'Tiro alto y corte mom fit con bota ligeramente entubada. Denim lavado de alta durabilidad.',
        'tallas': '26 – 28 – 30 – 32',
        'colores': 'Azul medio lavado',
        'precio': 199,
    },
    {
        'img': 'catalogo/imagenes/chaqueta_denim.jpg',
        'nombre': 'Chaqueta denim unisex',
        'desc': 'Chaqueta clásica de denim con cierre de botones y bolsillos en el pecho. Ideal para entretiempo.',
        'tallas': 'S – M – L – XL',
        'colores': 'Azul denim',
        'precio': 299,
    },
    {
        'img': 'catalogo/imagenes/vestido_midi.jpg',
        'nombre': 'Vestido midi de dama',
        'desc': 'Vestido midi de caída fluida con escote en V y manga corta. Elegante y cómodo para toda ocasión.',
        'tallas': 'S – M – L',
        'colores': 'Terracota y negro',
        'precio': 189,
    },
    {
        'img': 'catalogo/imagenes/conjunto_deportivo.jpg',
        'nombre': 'Conjunto deportivo',
        'desc': 'Set de dos piezas: buzo con capucha y pantalón jogger con puños elásticos. Tela suave de uso diario.',
        'tallas': 'S – M – L – XL',
        'colores': 'Gris y negro',
        'precio': 169,
    },
    {
        'img': 'catalogo/imagenes/casaca_bomber.jpg',
        'nombre': 'Casaca bomber',
        'desc': 'Casaca bomber con cuello y puños acanalados, cierre frontal y acabado satinado. Abrigo liviano con estilo urbano.',
        'tallas': 'M – L – XL',
        'colores': 'Negro y verde',
        'precio': 349,
    },
]

cards = []
for p in productos:
    img = b64(p['img'])
    import urllib.parse
    wa = 'https://wa.me/59164134784?text=' + urllib.parse.quote(
        'Hola M&C Heart of a Warrior, me interesa: ' + p['nombre'] +
        ' (Bs ' + str(p['precio']) + '). ¿Tienen disponibilidad?')
    cards.append(f'''
    <article class="card">
      <div class="foto"><img src="data:image/jpeg;base64,{img}" alt="{p['nombre']}"></div>
      <div class="cuerpo">
        <h2>{p['nombre']}</h2>
        <p class="desc">{p['desc']}</p>
        <p class="dato"><span>Tallas:</span> {p['tallas']}</p>
        <p class="dato"><span>Colores:</span> {p['colores']}</p>
        <p class="precio">Bs {p['precio']} <small>(precio referencial)</small></p>
        <a class="wa" href="{wa}" target="_blank" rel="noopener">Consultar por WhatsApp</a>
      </div>
    </article>''')

html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>M&amp;C Heart of a Warrior — Catálogo</title>
<style>
  :root {{ --rosa:#e0357a; --negro:#0b0b0d; --gris:#17171b; --texto:#f5f5f7; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--negro); color:var(--texto);
         font-family:'Segoe UI', Arial, Helvetica, sans-serif; }}
  header {{ background:#000; border-bottom:4px solid var(--rosa);
            padding:28px 16px; text-align:center; }}
  header img.logo {{ width:110px; height:110px; border-radius:50%;
                     border:3px solid var(--rosa); }}
  header h1 {{ margin-top:12px; font-size:1.9rem; letter-spacing:2px; }}
  header h1 b {{ color:var(--rosa); }}
  header p.lema {{ color:var(--rosa); letter-spacing:4px; font-weight:600;
                   text-transform:uppercase; font-size:.85rem; margin-top:4px; }}
  .aviso {{ max-width:960px; margin:22px auto 0; padding:14px 18px;
            background:var(--gris); border-left:4px solid var(--rosa);
            border-radius:6px; font-size:.92rem; line-height:1.5; }}
  main {{ max-width:1100px; margin:0 auto; padding:34px 16px 60px; }}
  h2.titulo-seccion {{ text-align:center; font-size:1.3rem; letter-spacing:3px;
                       text-transform:uppercase; margin-bottom:8px; }}
  h2.titulo-seccion span {{ color:var(--rosa); }}
  p.sub {{ text-align:center; color:#bdbdc4; font-size:.92rem; margin-bottom:30px; }}
  .grid {{ display:grid; gap:26px;
           grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); }}
  .card {{ background:var(--gris); border:1px solid #26262c; border-radius:12px;
           overflow:hidden; display:flex; flex-direction:column;
           transition:transform .15s ease, border-color .15s ease; }}
  .card:hover {{ transform:translateY(-4px); border-color:var(--rosa); }}
  .foto {{ background:#d9d9de; }}
  .foto img {{ width:100%; height:260px; object-fit:cover; display:block; }}
  .cuerpo {{ padding:18px 18px 22px; display:flex; flex-direction:column; gap:8px; flex:1; }}
  .cuerpo h2 {{ font-size:1.12rem; color:#fff; }}
  .desc {{ font-size:.9rem; color:#c9c9d1; line-height:1.45; }}
  .dato {{ font-size:.88rem; color:#e8e8ee; }}
  .dato span {{ color:var(--rosa); font-weight:700; }}
  .precio {{ font-size:1.35rem; font-weight:800; color:var(--rosa); margin-top:4px; }}
  .precio small {{ font-size:.7rem; color:#9a9aa2; font-weight:400; }}
  .wa {{ margin-top:auto; text-align:center; text-decoration:none;
         background:var(--rosa); color:#fff; font-weight:700; font-size:.95rem;
         padding:11px 12px; border-radius:8px; letter-spacing:.5px; }}
  .wa:hover {{ background:#c02364; }}
  footer {{ background:#000; border-top:4px solid var(--rosa); padding:26px 16px;
            text-align:center; font-size:.88rem; color:#bdbdc4; line-height:1.7; }}
  footer b {{ color:var(--rosa); }}
</style>
</head>
<body>
<header>
  <img class="logo" src="data:image/png;base64,{logo}" alt="Logotipo M&amp;C Heart of a Warrior">
  <h1>M&amp;C <b>HEART OF A WARRIOR</b></h1>
  <p class="lema">Clothing Store · Viacha, La Paz</p>
</header>

<div class="aviso">
  <strong>Cómo comprar:</strong> elige tu prenda, revisa tallas y colores, y pulsa
  «Consultar por WhatsApp». Confirmamos precio, disponibilidad y condiciones de
  entrega (retiro en Viacha o envíos a La Paz y al interior del país).
  Los pagos y la compra se concretan por WhatsApp; esta versión del catálogo no
  realiza cobros en línea.
</div>

<main>
  <h2 class="titulo-seccion">Catálogo de <span>prendas</span></h2>
  <p class="sub">Temporada 2026 · fotografías referenciales de cada línea de producto</p>
  <div class="grid">{''.join(cards)}
  </div>
</main>

<footer>
  <p><b>M&amp;C Heart of a Warrior</b> · La Paz, Bolivia</p>
  <p>WhatsApp: +591 64134784 · TikTok: @corazon.de.guerrera534</p>
  <p>© 2026 — Catálogo del emprendimiento para el sitio web del proyecto.</p>
</footer>
</body>
</html>'''

with open('catalogo_web.html', 'w') as f:
    f.write(html)
print('OK, tamaño KB:', os.path.getsize('catalogo_web.html') // 1024)
