# Restauración visual del hero — Fase visual 1

**Alcance autorizado:** recuperar la imagen de las dos personas y elevar SOLO el hero. Las mejoras visuales del resto de secciones requieren aprobación individual. Esta secuencia visual no sustituye ni da por aprobadas las fases funcionales del proyecto.

El ZIP `M_C_Hero_Restaurado.zip` contiene las fuentes y assets del hero; la tienda autocontenida `tienda_portable.html` se entrega por separado para evitar duplicar todo el catálogo.

## FASE 1 · Hero restaurado e integrado

### Archivo confirmado y diagnóstico

Se usa el archivo confirmado por la propietaria: **`uploads/hero.jpg`**, original de 1088×1360 px. No se modificó, sustituyó ni regeneró con IA.

La imagen seguía conservada. La demo anterior del header (`demo_header_sticky.html`) abre directamente la vista de catálogo, donde no se muestra el hero. Además, el diseño de Inicio restringía la foto al 60% derecho en desktop. Ahora la **tienda principal** conserva Inicio como entrada y muestra la imagen de borde a borde.

**Abrir `tienda_portable.html` o `catalogo_web.html` para ver la portada completa.** La demo específica del header continúa abriendo el catálogo: no se cambió esa navegación para forzar un hero donde no corresponde.

### Cambios aplicados, por prioridad

| Prioridad | Cambio quirúrgico | Código |
|---|---|---|
| P0 | Imagen real de fondo al 100% del ancho, altura mínima 80vh/80svh | `src/styles/hero-restored.css` · `.hero`, `.hero-background` |
| P0 | Encuadres responsive: retrato móvil y recorte 4:3 del mismo original en desktop; ambos rostros visibles | `build_portables.py` · `hero_resources()`; `scripts/prepare_assets.py` · `prepare_hero()` |
| P0 | WebP, eager/high para la imagen LCP y preload responsive sin doble descarga | `hero_resources()`, `src/shell.html` |
| P1 | Gradiente localizado oscuro→transparente junto al texto; se retira la masa opaca de la mitad izquierda | `.hero::after`, `.hcontent` |
| P1 | Serif editorial protagonista: hasta 6rem desktop, escala responsive móvil; sans limpia en subtítulo y CTA | `.hero h1`, `.hero-description` |
| P1 | Un solo acento: el vino de marca ya existente para «Ver colección» | `.hero .editorial-button` |
| P2 | Fade + desplazamiento de 10px en texto; zoom-out 1.035→1 en la imagen | `heroCopyEntrance`, `heroPhotoEntrance` |
| P2 | Flechas con microdesplazamiento y transición de 360ms; foco visible y movimiento reducido | `.hero-actions`, media query `prefers-reduced-motion` |

Las dos tipografías existentes (Cormorant/DM Sans, locales) se mantienen. No se cargó una tercera fuente, CDN ni biblioteca de animación. No se añadieron listeners de scroll: la animación del hero es CSS de entrada, no un parallax ni un bucle.

**Ajuste técnico fuera del hero:** las imágenes que el generador ya marcaba `loading="lazy"` reciben `fetchpriority="low"` en su HTML inicial, para reducir competencia con el LCP. No se cambian sus fotografías, composición, enlaces, carruseles ni aspecto.

### Antes / después conceptual del hero

| Aspecto | Antes | Después |
|---|---|---|
| Presencia de la imagen | Ausente en la demo de catálogo; reducida al lado derecho en Inicio desktop | Portada de Inicio con fondo a ancho completo |
| Composición | División negra/fotografía; foto al 60% | Fotografía como lienzo editorial único, sin panel duro |
| Altura | 490px móvil; 590–640px desktop | Al menos 80% del viewport; mínimo de diseño para pantallas cortas |
| Texto | Menor conexión visual con la imagen y recuadro móvil | Serif grande, texto sobre la foto, gradiente localizado |
| Acción | CTA claro más neutro | Vino de marca con flecha sutil; misma acción y destino |
| Movimiento | Portada mayormente estática | Entrada única y contenida; se desactiva si el usuario lo prefiere |
| Imagen LCP móvil de mayor resolución | WebP de unos 186 KiB | WebP de unos 119 KiB; original JPEG intacto |

Capturas reales para comparar:
- `previews/hero-before-390.jpg` → `previews/hero-after-390.jpg`.
- `previews/hero-before-1440.jpg` → `previews/hero-after-1440.jpg`.
- Vista adicional a 320px: `previews/hero-after-320.jpg`.

### Integración aplicada

No pegar otro hero ni duplicar ningún `main`. La sección existente en `src/home/home.html` conserva sus nodos, título, copy, CTA y atributos `data-home-*`. El generador coloca dentro de ella la imagen responsive y carga los estilos en este orden:

```python
styles = CSS + tokens + home_css + hero_restored_css + sticky_header_css
picture, hints = hero_resources(portable=portable, hero_source=hero_source)
```

Las modificaciones a `src/shell.html` son solo resource hints en `<head>`, no cambios del árbol de navegación o de las vistas.

Para reconstruir sobre el proyecto actual:

```bash
python3 scripts/prepare_assets.py --hero-only
python3 build_portables.py
python3 build_admin.py
python3 scripts/export_static.py
# Opcional: regenerar las demos específicas de navegación
python3 scripts/build_header_demo.py
python3 scripts/build_header_demo.py --mock
```

`--hero-only` no reprocesa productos ni looks. `tienda_portable.html` incluye las imágenes/fuentes y funciona sin conexión. `site/` usa archivos WebP externos y es la salida recomendada para hosting; no publicar el HTML portable de casi 6 MB como página optimizada para una red móvil.

## FASE 2 · Pendiente de aprobación, una sección cada vez

No se han aplicado aún los siguientes cambios. Son propuestas conceptuales, no resultados ya ejecutados:

| Orden sugerido | Sección existente | Antes → propuesta visual | Qué se conservaría |
|---|---|---|---|
| 1 | Novedades | Tarjetas más planas → profundidad ligera, hover 1.05, mayor contraste editorial y badges «Nuevo» reales | Carrusel, productos, orden, accesos a ficha y controles |
| 2 | Edits & looks | Dos cards con peso similar → composición más editorial mediante CSS, jerarquía y encuadres | Las dos imágenes existentes, avisos IA, modal y sus prendas |
| 3 | Nuestra intención | Bloque más uniforme → contraste tipográfico, números y divisores más expresivos | Consejos, disclosures y ningún claim ambiental nuevo |
| 4 | Contacto / footer | Cierre más neutro → espaciado y jerarquía de marca | Contactos, enlaces y contenido validado |

No se añadirán nuevas secciones de Lookbook/Editorial si eso cambia la estructura solicitada: se puede dar ese carácter al bloque de looks que ya existe. No se publicarán testimonios ficticios, fotos/nombres de clientas inventadas, descuentos sin validar, «Envío gratis» ni sellos «Join Life» ajenos a esta marca. Una marquesina nueva también necesita aprobación expresa porque sería un componente adicional y una animación continua.

**Siguiente aprobación propuesta:** mejorar solo Novedades, antes de intervenir cualquier otra sección.

## FASE 3 · Resumen y checklist parcial de esta entrega

### Qué NO se tocó

- Archivos del header sticky, CategoryBar, scroll-direction y su controlador: **idénticos por SHA-256**.
- Lógica de catálogo/PLP, navegación, buscador, filtros, favoritos, URL e historial: sin cambios de código.
- JavaScript de Homepage, carrusel, looks y foco de PDP: idéntico.
- PDP, pantallas de información, footer y demás bloques: no se eliminaron ni reordenaron.
- No se añadieron ni borraron reseñas. Los mocks no se publican.
- Las 73 fotos WebP del catálogo son idénticas a las anteriores; también se conserva el dataset operativo.
- Imagen original, ZIP histórico de Fase 1 y ZIP del header: intactos.
- Sin carrito, checkout, pagos, registro obligatorio ni importes públicos nuevos.

Evidencia: `tests/results-hero-unchanged.json`, resultados de regresión y capturas.

### Checklist técnico / accesibilidad

- [x] Hero visible en Inicio y fotografía correcta.
- [x] Fondo 100% del ancho; ≥80% de altura de viewport.
- [x] Revisado en 320, 390, 768, 1024 y 1440px, sin overflow horizontal.
- [x] Ambos rostros visibles en capturas móvil/desktop.
- [x] Una sola descarga de hero por viewport, incluso con preload + picture.
- [x] WebP, srcset, sizes, dimensiones intrínsecas; sin upscale de archivos.
- [x] LCP sin lazy-loading; imágenes secundarias conservan lazy.
- [x] Solo dos familias tipográficas locales.
- [x] CTA de al menos 44×44px y foco visible; destinos originales funcionan.
- [x] Texto alternativo descriptivo.
- [x] Movimiento reducido: sin zoom, fade ni desplazamientos.
- [x] Animaciones limitadas a transform/opacity; no provocan cambios de altura del hero.
- [x] Portable funciona offline en móvil y desktop.
- [x] Regresiones Homepage/header/estático aprobadas.
- [x] Auditoría automática A/AA de Homepage sin hallazgos en los tamaños probados.
- [ ] Validación manual con lectores de pantalla y dispositivos físicos Safari/iOS.
- [ ] LCP <2.5s en TODOS los perfiles: el perfil lento todavía no lo alcanza.
- [ ] Validación de rendimiento en el hosting de producción.
- [ ] Resumen visual final de toda la página: requiere completar las secciones aprobadas de Fase 2.

La auditoría automática no es una certificación completa WCAG. La ausencia de cambios de altura no implica CLS=0 absoluto: la carga de fuentes y el entorno pueden producir pequeños cambios iniciales.

### Rendimiento medido

Ver `tests/results-hero-performance.json`. Una muestra por perfil, caché vacía, viewport 390×844, DPR2, CPU emulada 4×. HTTP local de desarrollo, sin compresión de texto:

| Perfil | Red / latencia | LCP | CLS | Objetivo <2.5s |
|---|---|---:|---:|---|
| mobile-fast-4g | 4 Mbps / 80 ms | 1.34s | 0.0082 | Cumple en esta muestra |
| mobile-slow-4g | 1.6 Mbps / 150 ms | 3.31s | 0.0073 | Pendiente en este perfil |


**El objetivo <2.5s se cumple en el perfil rápido, no aún en el lento.** No se declara una garantía universal. Para el despliegue quedan por validar compresión Brotli/gzip de HTML/CSS/JS/JSON, caché con versionado y una nueva medición sobre el hosting/red de destino. No se modificó el servidor/backend para maquillar el resultado del laboratorio.

Repetir las pruebas:

```bash
npm install
npx playwright install --with-deps chromium
# En otra terminal: python3 server.py
npm run test:hero
npm run test:hero:performance
npm run test:home
npm run test:header
npm run test:static
```

---

# Código completo del hero

Referencia literal de la integración, no un segundo componente que haya que añadir. El `<section>` siguiente ya está dentro del `main.editorial-home` existente. La variante portable incrusta los mismos recursos en data URIs; el código web usa rutas locales.

## HTML existente + fotografía responsive

```html
  <section class="hero" aria-labelledby="home-title">
    <div class="hero-background"><picture><source media="(min-width: 768px)" srcset="/assets/home/hero-wide-768.webp 768w, /assets/home/hero-wide-1088.webp 1088w" sizes="max(100vw, 107svh)" width="1088" height="816"><img id="hero-image" src="/assets/home/hero-1088.webp" srcset="/assets/home/hero-640.webp 640w, /assets/home/hero-1088.webp 1088w" sizes="max(100vw, 64svh, 448px)" alt="Dos personas modelando ropa urbana en La Paz, con el Illimani al fondo" width="1088" height="1360" fetchpriority="high" loading="eager" decoding="async"></picture></div>
    <div class="hcontent">
      <p class="hero-eyebrow">M&amp;C · Heart of a Warrior</p>
      <h1 id="home-title">Carácter que<br><em>se lleva.</em></h1>
      <p class="hero-description">Prendas para hacer tuyo el ritmo de la ciudad.<span class="hero-extra"> Desde La Paz, a tu manera.</span></p>
      <div class="hero-actions">
        <a class="editorial-button editorial-button--light" href="#catalogo" data-home-catalog>Ver colección <span aria-hidden="true">↗</span></a>
        <a class="editorial-textlink hero-looks" href="#looks" data-home-scroll="looks">Explorar looks <span aria-hidden="true">↓</span></a>
      </div>
    </div>
    <p class="hero-caption" aria-hidden="true">ESTILO PROPIO / LA PAZ, BOLIVIA</p>
    <span class="hero-edition" aria-hidden="true">EDITORIAL / 01</span>
  </section>
```

## Preload en head (solo web)

```html
<link rel="preload" as="image" type="image/webp" href="/assets/home/hero-1088.webp" imagesrcset="/assets/home/hero-640.webp 640w, /assets/home/hero-1088.webp 1088w" imagesizes="max(100vw, 64svh, 448px)" media="(max-width: 767.98px)" fetchpriority="high">
<link rel="preload" as="image" type="image/webp" href="/assets/home/hero-wide-1088.webp" imagesrcset="/assets/home/hero-wide-768.webp 768w, /assets/home/hero-wide-1088.webp 1088w" imagesizes="max(100vw, 107svh)" media="(min-width: 768px)" fetchpriority="high">
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/editorial.woff2" crossorigin>
<link rel="preload" as="font" type="font/woff2" href="/assets/fonts/sans.woff2" crossorigin>
```

## CSS del hero

Archivo editable: `src/styles/hero-restored.css`.

```css
/* FASE VISUAL 1 — solo el hero existente.
 * Cargar después de home.css. No modifica header, navegación, PLP, PDP o footer.
 * La foto sigue siendo uploads/hero.jpg; <picture> elige su encuadre responsive.
 */
.editorial-home .hero{
  /* Altura reservada desde el primer render: la imagen no empuja el contenido. */
  position:relative;
  isolation:isolate;
  overflow:hidden;
  display:flex;
  align-items:flex-end;
  width:100%;
  max-width:none;
  min-height:80vh; /* fallback para navegadores anteriores a svh */
  min-height:max(35rem,80svh);
  margin:0;
  padding:38px var(--mc-gutter) calc(112px + env(safe-area-inset-bottom));
  background:#1a1a1a;
  color:#faf8f5;
  text-align:left;
}
/* Fondo real de borde a borde. No volver a width:60% en desktop. */
.editorial-home .hero-background{
  position:absolute;
  inset:0;
  width:100%;
  max-width:none;
  z-index:0;
}
.editorial-home .hero-background picture{display:block;width:100%;height:100%;}
.editorial-home .hero-background img{
  display:block;
  width:100%;
  height:100%;
  max-width:none;
  object-fit:cover;
  object-position:50% 24%;
  /* Solo transform/opacity; no filtros, blur ni will-change permanente. */
  animation:heroPhotoEntrance 1500ms cubic-bezier(.22,.61,.36,1) both;
}
/* Oscuro → transparente SOLO junto al texto. No es un filtro sobre toda la foto. */
.editorial-home .hero::after{
  content:"";
  position:absolute;
  inset:0;
  z-index:1;
  pointer-events:none;
  background:linear-gradient(0deg,rgba(26,26,26,.72) 0%,rgba(26,26,26,.28) 35%,transparent 68%);
}
/* Se retira únicamente el antiguo recuadro opaco; se conservan sus nodos/CTA. */
.editorial-home .hero .hcontent{
  position:relative;
  z-index:2;
  width:100%;
  max-width:34rem;
  padding:0;
  border:0;
  border-radius:0;
  background:transparent;
  backdrop-filter:none;
  -webkit-backdrop-filter:none;
}
.editorial-home .hero .hero-eyebrow{
  margin:0 0 14px;
  color:#f1e7e1;
  font:500 9px/1.5 var(--mc-sans);
  letter-spacing:2.1px;
  text-transform:uppercase;
}
.editorial-home .hero h1{
  margin:0 0 18px;
  font:400 clamp(3.5rem,13vw,4.5rem)/.94 var(--mc-serif);
  letter-spacing:-1.8px;
  color:#faf8f5;
  text-transform:none;
  text-shadow:0 2px 18px rgba(26,26,26,.28);
}
.editorial-home .hero h1 em{font-weight:400;}
.editorial-home .hero .hero-description{
  max-width:24rem;
  margin:0 0 22px;
  color:#f6f1eb;
  font:400 13px/1.75 var(--mc-sans);
  text-shadow:0 1px 10px rgba(26,26,26,.3);
}
.editorial-home .hero-actions{display:flex;align-items:center;flex-wrap:wrap;gap:14px 20px;}
.editorial-home .hero .editorial-button{
  min-height:48px;
  padding:13px 18px;
  gap:20px;
  border:1px solid var(--mc-rose);
  background:var(--mc-rose);
  color:#faf8f5;
  font:500 12px/1.5 var(--mc-sans);
  transition:background 360ms cubic-bezier(.22,.61,.36,1),border-color 360ms ease;
}
.editorial-home .hero .editorial-button:hover{
  background:var(--mc-rose-hover);
  border-color:var(--mc-rose-hover);
}
.editorial-home .hero .hero-looks{
  min-height:48px;
  color:#faf8f5;
  font:500 11px/1.5 var(--mc-sans);
  border-bottom:1px solid rgba(250,248,245,.7);
}
.editorial-home .hero .hero-looks:hover{color:#faf8f5;border-bottom-color:#faf8f5;}
.editorial-home .hero-actions a span{display:inline-block;transition:transform 360ms cubic-bezier(.22,.61,.36,1);}
.editorial-home .hero .editorial-button:hover span{transform:translate(3px,-2px);}
.editorial-home .hero .hero-looks:hover span{transform:translateY(3px);}
.editorial-home .hero a:focus-visible{outline:3px solid #faf8f5;outline-offset:5px;}
/* Entrada una sola vez por aparición, no un bucle ni un efecto ligado al scroll. */
.editorial-home .hero .hcontent>*{animation:heroCopyEntrance 650ms cubic-bezier(.22,.61,.36,1) both;}
.editorial-home .hero .hero-eyebrow{animation-delay:60ms;}
.editorial-home .hero h1{animation-delay:120ms;}
.editorial-home .hero .hero-description{animation-delay:180ms;}
.editorial-home .hero .hero-actions{animation-delay:240ms;}
@keyframes heroPhotoEntrance{
  from{transform:scale(1.035);opacity:.96;}
  to{transform:scale(1);opacity:1;}
}
@keyframes heroCopyEntrance{
  from{opacity:.35;transform:translateY(10px);}
  to{opacity:1;transform:translateY(0);}
}
@media(min-width:768px){
  .editorial-home .hero{padding:64px max(var(--mc-gutter),calc((100% - 1152px)/2));}
  .editorial-home .hero-background img{object-position:50% 24%;}
  .editorial-home .hero::after{
    background:radial-gradient(ellipse at 0 100%,rgba(26,26,26,.72),transparent 68%),linear-gradient(0deg,rgba(26,26,26,.4),transparent 64%);
  }
  .editorial-home .hero .hero-eyebrow{font-size:10px;letter-spacing:2.8px;margin-bottom:18px;}
  .editorial-home .hero h1{font-size:clamp(4.5rem,7.2vw,6rem);letter-spacing:-2.8px;margin-bottom:22px;}
  .editorial-home .hero .hero-description{font-size:14px;line-height:1.8;max-width:25rem;margin-bottom:25px;}
  .editorial-home .hero-actions{gap:28px;}
  .editorial-home .hero .editorial-button{min-height:50px;padding:14px 21px;}
  .editorial-home .hero .hero-looks{font-size:12px;}
  .editorial-home .hero .hero-caption,.editorial-home .hero .hero-edition{color:#faf8f5;}
}
/* Respeto estricto al usuario: sin zoom, fade, desplazamientos ni esperas. */
@media(prefers-reduced-motion:reduce){
  .editorial-home .hero-background img,.editorial-home .hero .hcontent>*{animation:none!important;transform:none!important;opacity:1!important;}
  .editorial-home .hero-actions a,.editorial-home .hero-actions a span{transition:none!important;}
}

```

## Generación de picture y preload

Archivo editable: `build_portables.py`.

```python
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



```

## Preparación de los mismos archivos de imagen

Archivo editable: `scripts/prepare_assets.py`.

```python
def prepare_hero():
    """Mismo original: retrato móvil + recorte 4:3 de escritorio, sin IA/upscale."""
    source = ROOT / 'uploads/hero.jpg'
    for width in (640, 1088):
        webp(source, WEB / f'assets/home/hero-{width}.webp', width, 75)
    with Image.open(source) as original:
        image = ImageOps.exif_transpose(original).convert('RGB')
        height = min(image.height, round(image.width * .75))
        # Illimani, ambos rostros y planos medios del MISMO archivo suministrado.
        crop = image.crop((0, 0, image.width, height))
        for width in (768, 1088):
            framed = crop.copy()
            if framed.width > width:
                framed.thumbnail((width, round(width * height / image.width)), Image.Resampling.LANCZOS)
            output = WEB / f'assets/home/hero-wide-{width}.webp'
            output.parent.mkdir(parents=True, exist_ok=True)
            framed.save(output, 'WEBP', quality=83, method=6)



```
