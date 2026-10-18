# -*- coding: utf-8 -*-
"""Comprime las fotos reales del emprendimiento y genera el catálogo ampliado (sin precios públicos)."""
import json
import os
from PIL import Image

SRC = 'uploads/imgs_pdf'
OUT = 'web/img/cat'
os.makedirs(OUT, exist_ok=True)

# (archivo origen, id, nombre, categoría, tallas)
NUEVAS = [
    ('wa2036_p1_0.jpg', 'sw01', 'Sweater amarillo NFL', 'sweaters', 'M – L – XL'),
    ('wa2036_p2_0.jpg', 'ch01', 'Campera deportiva blanca con cierre', 'chaquetas', 'M – L'),
    ('wa2036_p3_0.jpg', 'sw02', 'Sweater gris escudo clásico', 'sweaters', 'M – L – XL'),
    ('wa2036_p4_0.jpg', 'sw03', 'Sweater gris banda camuflada', 'sweaters', 'M – L – XL'),
    ('wa2036_p5_0.jpg', 'sw04', 'Sweater negro print tribal', 'sweaters', 'M – L – XL'),
    ('wa2036_p6_0.jpg', 'sw05', 'Sweater negro VENHIT', 'sweaters', 'M – L – XL'),
    ('wa2036_p7_0.jpg', 'sw06', 'Sweater gris claro deportivo', 'sweaters', 'M – L – XL'),
    ('wa2036_p8_0.jpg', 'sw07', 'Sweater negro liso', 'sweaters', 'M – L – XL'),
    ('wa2036_p9_0.jpg', 'sw08', 'Sweater vino Oklahoma', 'sweaters', 'M – L – XL'),
    ('wa2036_p10_0.jpg', 'sw09', 'Sweater rojo McCloud California', 'sweaters', 'M – L – XL'),
    ('wa2036_p11_0.jpg', 'sw10', 'Sweater verde oliva tipografía', 'sweaters', 'M – L – XL'),
    ('wa2036_p12_0.jpg', 'sw11', 'Sweater navy Los Ángeles 98', 'sweaters', 'M – L – XL'),
    ('wa2036_p13_0.jpg', 'sw12', 'Sweater navy cuello con cierre', 'sweaters', 'M – L – XL'),
    ('wa2036_p14_0.jpg', 'sw13', 'Sweater gris perla deportivo', 'sweaters', 'M – L – XL'),
    ('wa2036_p15_0.jpg', 'sw14', 'Sweater taupe print llama', 'sweaters', 'M – L – XL'),
    ('wa2036_p16_0.jpg', 'sw15', 'Sweater gris cierre detalle naranja', 'sweaters', 'M – L – XL'),
    ('wa2036_p17_0.jpg', 'sw16', 'Sweater rojo print oso', 'sweaters', 'M – L – XL'),
    ('wa2036_p18_0.jpg', 'sw17', 'Sweater negro logo bordado', 'sweaters', 'M – L – XL'),
    ('wa2036_p19_0.jpg', 'sw18', 'Sweater vino liso', 'sweaters', 'M – L – XL'),
    ('wa2036_p20_0.jpg', 'sw19', 'Sweater gris claro liso', 'sweaters', 'M – L – XL'),
    ('wa2036_p21_0.jpg', 'sw20', 'Sweater navy Jeep', 'sweaters', 'M – L – XL'),
    ('wa2036_p22_0.jpg', 'sw21', 'Sweater blanco liso', 'sweaters', 'M – L – XL'),
    ('wa2036_p23_0.jpg', 'sw22', 'Sweater blanco SKI', 'sweaters', 'M – L – XL'),
    ('wa2036_p24_0.jpg', 'sw23', 'Sweater negro engagement', 'sweaters', 'M – L – XL'),
    ('wa2036_p25_0.jpg', 'sw24', 'Hoodie blanco print smiley', 'sweaters', 'M – L – XL'),
    ('wa2036_p26_0.jpg', 'sw25', 'Sweater navy cuello camisa', 'sweaters', 'M – L – XL'),
    ('wa2036_p27_0.jpg', 'sw26', 'Sweater gris detalle cuadros', 'sweaters', 'M – L – XL'),
    ('wa2036_p28_0.jpg', 'sw27', 'Sweater beige oso USA', 'sweaters', 'M – L – XL'),
    ('wa2036_p29_0.jpg', 'sw28', 'Sweater blanco NY', 'sweaters', 'M – L – XL'),
    ('wa2036_p30_0.jpg', 'sw29', 'Sweater gris jaspeado deportivo', 'sweaters', 'M – L – XL'),
    ('wa2029_p1_0.jpg', 'top01', 'Manga larga dama terracota escote amplio', 'tops', 'S – M – L'),
    ('wa2029_p2_0.jpg', 'top02', 'Manga larga dama negro liso', 'tops', 'S – M – L'),
    ('wa2029_p3_0.jpg', 'top03', 'Sudadera dama crema', 'tops', 'S – M – L'),
    ('wa2029_p4_0.jpg', 'top04', 'Manga larga dama crema liso', 'tops', 'S – M – L'),
    ('wa2029_p5_0.jpg', 'top05', 'Sudadera dama gris college', 'tops', 'S – M – L'),
    ('wa2029_p6_0.jpg', 'top06', 'Manga larga dama print gráfico', 'tops', 'S – M – L'),
    ('wa2029_p7_0.jpg', 'cr01', 'Crop top verde salut', 'crops', 'S – M'),
    ('wa2029_p8_0.jpg', 'ch02', 'Top campera dama negro con cierre', 'chaquetas', 'S – M – L'),
    ('wa2029_p9_0.jpg', 'top07', 'Sweater dama gris cuello V', 'tops', 'S – M – L'),
    ('wa2029_p10_0.jpg', 'top08', 'Manga larga dama gris estrella', 'tops', 'S – M – L'),
    ('wa2029_p11_0.jpg', 'top09', 'Manga larga dama gris con capucha', 'tops', 'S – M – L'),
    ('wa2029_p12_0.jpg', 'top10', 'Manga larga dama negro selfie', 'tops', 'S – M – L'),
    ('wa2029_p13_0.jpg', 'top11', 'Manga larga dama blanco cuello V', 'tops', 'S – M – L'),
    ('wa2029_p14_0.jpg', 'top12', 'Manga larga dama beige print labios', 'tops', 'S – M – L'),
    ('wa2029_p15_0.jpg', 'ch03', 'Campera dama floral con cierre', 'chaquetas', 'S – M – L'),
    ('wa2029_p16_0.jpg', 'top13', 'Manga larga dama rayas navy', 'tops', 'S – M – L'),
    ('wa2029_p17_0.jpg', 'top14', 'Sweater dama negro GUESS', 'tops', 'S – M – L'),
    ('wa2029_p19_0.jpg', 'ch04', 'Campera dama tie-dye con cierre', 'chaquetas', 'S – M – L'),
    ('wa2029_p20_0.jpg', 'top15', 'Manga larga dama negro básico', 'tops', 'S – M – L'),
    ('wa2029_p21_0.jpg', 'top16', 'Manga larga dama rayas blancas', 'tops', 'S – M – L'),
    ('wa2029_p22_0.jpg', 'top17', 'Manga larga dama leopard print', 'tops', 'S – M – L'),
    ('wa2029_p23_0.jpg', 'top18', 'Manga larga dama violeta peplum', 'tops', 'S – M – L'),
    ('wa2029_p24_0.jpg', 'top19', 'Manga larga dama leopard oscuro', 'tops', 'S – M – L'),
    ('wa2029_p26_0.jpg', 'top20', 'Sudadera dama crema con print', 'tops', 'S – M – L'),
    ('wa2029_p27_0.jpg', 'top21', 'Manga larga dama negro escote amplio', 'tops', 'S – M – L'),
    ('wa2029_p28_0.jpg', 'top22', 'Sudadera dama gris Santa', 'tops', 'S – M – L'),
    ('wa2029_p29_0.jpg', 'top23', 'Polo dama negro con escudo', 'tops', 'S – M – L'),
    ('wa2029_p30_0.jpg', 'top24', 'Manga larga dama fucsia', 'tops', 'S – M – L'),
    ('wa2029_p31_0.jpg', 'top25', 'Set sudadera dama crema', 'tops', 'S – M – L'),
    ('wa2029_p32_0.jpg', 'cr02', 'Top dama beige rib', 'crops', 'S – M'),
    ('wa2029_p33_0.jpg', 'cr03', 'Top dama negro tiras cruzadas', 'crops', 'S – M'),
    ('wa2029_p34_0.jpg', 'cr04', 'Crop top dama gris fruncido', 'crops', 'S – M'),
    ('wa2029_p35_0.jpg', 'top26', 'Tejido dama lila', 'tops', 'S – M – L'),
    ('wa2029_p36_0.jpg', 'cr05', 'Top deportivo dama gris', 'crops', 'S – M'),
    ('wa2029_p37_0.jpg', 'cr06', 'Chaleco tejido dama azul V', 'crops', 'S – M'),
    ('wa2029_p38_0.jpg', 'cr07', 'Top tejido dama beige', 'crops', 'S – M'),
    ('wa2029_p39_0.jpg', 'cr08', 'Top dama colorblock', 'crops', 'S – M'),
]

total_kb = 0
for src, pid, nombre, cat, tallas in NUEVAS:
    im = Image.open(os.path.join(SRC, src)).convert('RGB')
    im.thumbnail((900, 900))
    out = os.path.join(OUT, pid + '.jpg')
    im.save(out, 'JPEG', quality=72, optimize=True)
    total_kb += os.path.getsize(out) // 1024

print('imágenes nuevas:', len(NUEVAS), '| total KB:', total_kb)

# ---------- catálogo completo (73 prendas) ----------
ANTERIORES = json.load(open('web/data/productos.json'))
for p in ANTERIORES:
    p.setdefault('categoria', {'polera': 'poleras', 'jean': 'jeans', 'chaqueta': 'chaquetas',
                               'vestido': 'vestidos', 'conjunto': 'sport', 'bomber': 'chaquetas'}.get(p['id'], 'sport'))
    p['nuevo'] = False

nuevas = [{'id': pid, 'nombre': nombre, 'descripcion': '', 'tallas': tallas, 'colores': '',
           'precio': 0, 'imagen': '/img/cat/%s.jpg' % pid, 'activo': True,
           'categoria': cat, 'nuevo': True} for _, pid, nombre, cat, tallas in NUEVAS]

todo = ANTERIORES + nuevas
json.dump(todo, open('web/data/productos.json', 'w'), ensure_ascii=False, indent=2)
print('catálogo total:', len(todo))
from collections import Counter
print(Counter(p['categoria'] for p in todo))
