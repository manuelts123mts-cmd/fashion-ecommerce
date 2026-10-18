# Header sticky de doble capa — M&C

Implementado en la tienda existente con HTML + CSS puro + JavaScript vanilla. **No se agregó carrito, checkout, pago ni registro obligatorio.** Esta es una mejora puntual solicitada para navegación; no equivale a ejecutar todas las fases pendientes del e-commerce.

## 1. Enfoque elegido

- Un **header global `position: sticky; top: 0; z-index: 50`**, hijo directo de `body`, contiene dos filas CSS Grid: `auto` y `56px`.
- La barra inferior también declara `position: sticky; top: 0; z-index: 50`. El header padre mantiene su contexto sticky a lo largo de toda la vista, no solo dentro de una sección del catálogo.
- Al bajar, `transform: translateY(calc(-100% + var(--category-bar-size)))` mueve exactamente la fila superior fuera del viewport. El `100%` es la altura intrínseca del conjunto: **no se mide la altura del header en JS**, no hay `position: fixed` para el header ni se elimina su espacio del flujo.
- Al subir, se retira la clase `.is-compact`. La transición es de **240 ms** y respeta `prefers-reduced-motion`.
- **IntersectionObserver** detecta el inicio para la elevación, las secciones visibles para la categoría activa y el final del catálogo para categorías cortas.
- **La dirección no se obtiene exclusivamente con IntersectionObserver**: este no emite eventos por cada movimiento dentro de una sección larga. Un listener `scroll` pasivo, agrupado con `requestAnimationFrame`, lee solo `scrollY` y utiliza histéresis de 12 px. Es una solución deliberada para evitar respuestas tardías o falsas.
- `will-change: transform` se aplica únicamente al contenedor del header. Los cambios de estado son clases/atributos; no se recalculan alturas ni posiciones `top` durante el scroll.

### Navegación real por categorías

Antes, elegir una categoría eliminaba las otras tarjetas del grid. Ahora las **ocho categorías reales** conservan sus secciones (`#categoria-sweaters`, `#categoria-jeans`, etc.). El nombre salta a su sección y la flecha adyacente abre el mega-menú. Así no se mezclan dos acciones en el mismo control.

Los filtros de talla, ordenación y buscador siguen funcionando. El contador superior representa todas las prendas activas del catálogo; el encabezado de cada sección muestra las coincidencias filtradas. Si una sección no tiene coincidencias, permite limpiar filtros sin dejar un enlace roto.

### Accesibilidad

- Enlaces/listas semánticas, sin un `role="menu"` incompleto.
- Categoría activa con `aria-current="page"` (una sola a la vez).
- Flechas de submenú con `aria-expanded` y `aria-controls`.
- Tab y Shift+Tab; flechas izquierda/derecha, Home/End; Enter para navegar; flecha abajo para entrar al submenú; Escape para cerrar y devolver el foco.
- Controles de al menos 44×44 px. El contenedor horizontal tiene snap obligatorio y gradientes que indican contenido a los lados.
- La fila superior compactada usa `inert` y `aria-hidden`; el botón de lupa en la barra permite recuperarla y enfocar el buscador en cualquier momento.
- La cabecera no se esconde mientras se escribe, hay un modal/menú abierto o se protege una interacción de teclado en la fila superior.
- Abrir o cerrar el mega-menú no mueve el scroll ni modifica la altura del documento. El panel está fuera del contenedor horizontal para que `overflow-x` no lo recorte.

### Iconos funcionales

El corazón guarda favoritos **locales**, disponibles desde las tarjetas y fichas. El icono personal abre «Tu espacio, sin registro»: explica claramente que no existen cuentas de cliente en esta versión. No se simula un login ni un servicio de cuenta. Si el navegador bloquea localStorage, los favoritos funcionan durante la sesión y se informa de que no persistirán.

## 2. Archivos y demostraciones

```text
src/components/header.html              Cabecera superior + contenedor de dos filas
src/components/category-bar.html        Categorías + overlay de mega-menú
src/styles/sticky-header.css            Estilos comentados y breakpoints
src/navigation/scroll-direction.js       Ayudante vanilla reutilizable con cleanup
src/scripts/sticky-header.js            Estado, IO, ARIA, URL, menú y favoritos
src/data/categories.json                Definiciones reales; contadores derivados
src/data/categories.mock.json           Fixtures ficticias, nunca se cargan al público
scripts/build_header_demo.py            Crea las dos demostraciones
src/legacy/store.js                     Integración con filtros y secciones
src/shell.html                          Posición global del header y datos JSON
build_portables.py                     Ensambla todo en web/ y portable
```

### Probar sin instalar nada

1. Abrir **`demo_header_sticky.html`** en un navegador moderno: usa el catálogo real existente, sin importes públicos.
2. O abrir **`demo_header_mock.html`**: cinco categorías y veinte prendas ficticias claramente marcadas, imágenes placeholder y WhatsApp deshabilitado. Es útil para probar nombres largos y aislar el componente.
3. Bajar unos 150 px: la cabecera superior debe deslizarse fuera de pantalla y las categorías quedar en el borde superior.
4. Subir más de 12 px: debe volver la cabecera completa.
5. En móvil, arrastrar horizontalmente las categorías. La flecha lateral ayuda también con ratón.
6. Pulsar un nombre para navegar; pulsar su chevron para abrir el panel. Probar Escape y clic fuera.
7. Navegar con teclado y comprobar que solo una categoría tiene `aria-current="page"`.
8. Guardar una prenda con el corazón y abrir el icono de favoritos.

Las fuentes e imágenes necesarias están incrustadas en las demos offline. WhatsApp/TikTok necesitan internet cuando se usan en la tienda real. La vista integrada de producción sigue siendo **`tienda_portable.html`**; también se actualizó `site/`.

## 3. Integración en la página actual

**La integración ya está aplicada.** No hay que pegar otro header encima del existente.

Para llevar este complemento al proyecto anterior de Fase 1, copiar las carpetas/archivos de código de este ZIP sobre ese proyecto, manteniendo sus imágenes originales y `web/data/productos.json`. Después reconstruir:

```bash
python3 build_portables.py
python3 build_admin.py
python3 scripts/export_static.py
python3 scripts/build_header_demo.py
python3 scripts/build_header_demo.py --mock
python3 server.py
```

Abrir `http://localhost:8000/` o `http://localhost:8000/demo-header.html` (demo de datos reales) y `http://localhost:8000/demo-header-mock.html` (fixtures). Para hosting estático se sigue publicando solo `site/`, no el admin ni la API de edición.

### Orden de montaje

```html
<body>
  <!-- Aviso superior, si existe -->
  <!-- header.html incluye category-bar.html y se sitúa directamente aquí -->
  <header class="site-header" id="site-header">…</header>

  <main id="catalogo">
    <!-- Cada sección renderizada tiene un ID estable -->
    <section id="categoria-jeans" data-category-section="jeans">…</section>
  </main>

  <script type="application/json" id="header-data">{"categories":[],"imageMap":{}}</script>
  <!-- Primero la lógica existente del catálogo: ALL, CATS, filtros, openPDP, setScreen -->
  <!-- Después scroll-direction.js, sticky-header.js y finalmente home.js -->
</body>
```

El generador rellena `__LOGO__`, `__CATEGORY_LINKS__`, `__HEADER_DATA__` y demás marcadores. **No son recursos remotos ni valores que haya que inventar.** `category_links()` está incluido en `build_portables.py` y prerenderiza enlaces/contadores, luego el componente los sincroniza con productos activos.

### Contrato con el catálogo

- `ALL`: productos activos; `CATS`: mapa de nombres derivado de `header-data`.
- `setScreen('catalogo')`, `openPDP(id)`, `tokensTalla()`, filtros existentes y `render()`.
- `init()` emite `mc:catalog-ready`; `render()` emite `mc:catalog-rendered`.
- `setScreen()` emite `mc:screen-change`; `openPDP()` emite `mc:pdp-open`.
- `mc:pdp-return-focus` entrega el elemento al que se debe devolver el foco al cerrar una ficha abierta desde un overlay.
- No se vuelve a renderizar el catálogo por cada cambio del observador: solo se actualizan el indicador, ARIA y la URL.

API de consola disponible para pruebas:

```js
MCHeader.goCategory('jeans');
MCHeader.reveal({focusSearch:true});
MCHeader.getState();
// En desmontaje de una integración SPA: MCHeader.destroy();
```

No corresponde un hook de React en este stack. El equivalente reutilizable es `createScrollDirectionObserver(callback, options)`, con `reset()` y `destroy()`.

### Extras incluidos

- Contadores derivados del catálogo activo.
- Persistencia de categoría en `?cat=jeans`, tanto al pulsar como al desplazarse; usa `replaceState` para el scroll y `pushState` para saltos explícitos.
- Back/Forward y entrada directa a una categoría.
- Indicador de elevación, subrayado animado, scroll-snap y controles de desplazamiento horizontal.
- Favoritos locales. Sin carrito ni checkout.

No se añaden prefetch de Next.js ni dependencias que este proyecto no usa. No hay un botón flotante nuevo de «volver arriba»: se conserva el existente de la portada. Tampoco se agrega un skeleton innecesario: los enlaces están prerenderizados y sus contadores se sincronizan al cargar datos.

## 4. Pruebas y límites

```bash
npm install
npx playwright install --with-deps chromium
# Mantener python3 server.py abierto en otra terminal
npm run test:header
npm run test:home
npm run test:static
```

`tests/results-sticky-header.json` registra los resultados en **320, 768, 1024 y 1440 px**. Comprueba:

- barra en `top: 0` al bajar y fila superior visible al subir;
- misma altura del header y del documento antes/después de compactar;
- ausencia de overflow horizontal del documento (el desplazamiento horizontal pertenece solo a las categorías);
- navegación suave a sección, observación automática de otra categoría y una sola marca activa;
- contadores, mega-menú por clic, Escape/clic exterior, teclado, favoritos y URL;
- funcionamiento offline, almacenamiento bloqueado y movimiento reducido;
- auditoría automática A/AA del header/Homepage sin hallazgos en los tamaños probados.

`tests/header-edges.spec.cjs` y `tests/results-header-edges.json` añaden comprobaciones de hover, ficha desde mega-menú y devolución de foco, sugerencia predictiva por encima de categorías, historial Back/Forward, catálogo vacío y las dos demos offline.

Capturas finales: `previews/sticky-320-{compact,expanded,menu}.png` y `previews/sticky-1440-{compact,expanded,menu}.png`.

La revisión automática no certifica todo el sitio como WCAG AA, ni reemplaza pruebas con lectores de pantalla y dispositivos físicos. Las comprobaciones se realizan en Chromium; no se declara validación en todos los iPhone/Safari reales ni una garantía de FPS.

### Edge cases importantes

1. **Ancestros con overflow/transform:** mantener el header directamente en `body`; `overflow:hidden/auto/scroll` en un ancestro puede cambiar o impedir el sticky. El `transform` de compactación pertenece al propio header, no a un wrapper de toda la página.
2. **Contenido que cambia de tamaño:** la fila superior es `auto`; la fórmula CSS usa su altura intrínseca. No reintroducir un `top` calculado por JS. Si se cambia `--category-bar-size`, todos los offsets CSS de categorías lo heredan.
3. **Filtro sin coincidencias:** la categoría permanece como destino y muestra un mensaje con «Limpiar filtros». Un catálogo vacío no publica inventario inventado.
4. **Últimas categorías cortas:** un observador del final resuelve el caso en que el último grupo no alcanza la línea central del viewport.
5. **Scroll programático largo:** se distingue del scroll manual para no mostrar categorías intermedias como selección final. Una rueda/touch cancela ese bloqueo temporal.
6. **Menú abierto o buscador enfocado:** se protege la interacción; el autohide se reanuda al terminarla. No se pierde el texto de búsqueda por compactar el header.
7. **Storage/History bloqueados en iframe o modo privado:** se mantienen navegación y favoritos de sesión; se informa de la limitación. No se necesita conexión para el sticky.
8. **Navegadores antiguos:** `IntersectionObserver`, `inert`, `<dialog>` y `scrollIntoView` suave se priorizan para navegadores modernos. Sin IO se conserva el sticky y la navegación manual; no se afirma un scrollspy automático inexistente en ese caso.
9. **Menús vs. selección:** hover abre la previsualización sin cambiar la categoría activa; esta representa la sección que se está leyendo, no el panel que se está previsualizando.
10. **Regiones o categorías no existentes:** no se añadieron Accesorios/Pantalones como inventario real. Están en los fixtures; el catálogo operativo conserva sus ocho categorías reales (incluido Jeans).

---

# 5. Código completo del componente

Los bloques siguientes son copias literales de los archivos entregados. Para editar, modificar las fuentes, no este documento ni los HTML generados. El ZIP también incluye el shell, el renderer adaptado y el generador, para no dejar la integración en pseudocódigo.

## src/components/header.html

```html
<!-- HEADER GLOBAL. Debe ser hijo directo de body: ningún ancestro con overflow. -->
<span class="header-sentinel" id="header-sentinel" aria-hidden="true"></span>
<header class="site-header" id="site-header" data-sticky-header>
  <!-- Fila de altura intrínseca. Se desplaza con transform, sin display:none. -->
  <div class="masthead" id="masthead">
    <div class="hwrap">
      <a class="brand" href="#home-title" data-home-top aria-label="M&amp;C Heart of a Warrior — Inicio"><img src="__LOGO__" alt="" width="46" height="46"><span class="brand-wordmark"><strong>M&amp;C</strong><span>HEART OF A WARRIOR</span></span></a>
      <div class="search">
        <input id="buscar" type="search" placeholder="Buscar prendas" aria-label="Buscar prenda" autocomplete="off" aria-controls="sugg">
        <div class="sugg" id="sugg" hidden></div>
      </div>
      <div class="header-actions" aria-label="Tu espacio">
        <button class="header-icon" type="button" data-open-favorites aria-haspopup="dialog" aria-controls="header-space" aria-label="Ver favoritos"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20.8 4.6a5.5 5.5 0 0 0-7.8 0L12 5.7l-1.1-1.1a5.5 5.5 0 0 0-7.8 7.8L12 21l8.8-8.6a5.5 5.5 0 0 0 0-7.8Z"/></svg><span class="favorite-counter" data-favorite-count hidden>0</span></button>
        <button class="header-icon" type="button" data-open-space aria-haspopup="dialog" aria-controls="header-space" aria-label="Mi espacio, sin registro obligatorio"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="8" r="4"/><path d="M4.5 21a7.5 7.5 0 0 1 15 0"/></svg></button>
        <a class="header-contact" href="https://wa.me/59164134784" target="_blank" rel="noopener noreferrer">Atención personal ↗</a>
      </div>
    </div>
  </div>
  <!-- Fila inferior: permanece visible también cuando la superior sale del viewport. -->
  __CATEGORY_BAR__
</header>

<!-- Fuera del header transformado; dialog usa la top layer nativa del navegador. -->
<dialog class="header-space" id="header-space" aria-labelledby="header-space-title">
  <button class="icon-button header-space-close" type="button" data-space-close aria-label="Cerrar tu espacio">×</button>
  <p class="eyebrow">M&amp;C · Tu espacio</p><h2 id="header-space-title">Tus favoritos</h2>
  <div id="header-space-content"></div>
  <p class="space-storage-note" id="favorite-storage-note">Los favoritos se guardan solo en este navegador. No creamos una cuenta ni solicitamos datos personales.</p>
</dialog>

```

## src/components/category-bar.html

```html
<!-- CATEGORY BAR: navegación de secciones, no un filtro que destruya el scroll. -->
<nav class="category-bar" id="category-bar" aria-label="Categorías de prendas">
  <div class="category-bar-inner">
    <button class="category-control category-reveal" type="button" data-header-reveal aria-label="Mostrar cabecera y enfocar el buscador" aria-controls="masthead" aria-expanded="true"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m15.5 15.5 5 5"/></svg></button>
    <button class="category-control category-prev" type="button" data-categories-prev aria-label="Ver categorías anteriores" aria-controls="chips" disabled><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m14 6-6 6 6 6"/></svg></button>
    <div class="category-viewport can-scroll-right" id="category-viewport">
      <ul class="category-list" id="chips">__CATEGORY_LINKS__</ul>
    </div>
    <button class="category-control category-next" type="button" data-categories-next aria-label="Ver más categorías" aria-controls="chips"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="m10 6 6 6-6 6"/></svg></button>
  </div>
  <!-- Overlay absoluto: abrir/cerrar nunca cambia la altura ni el scroll del documento. -->
  <section class="category-mega" id="category-mega" aria-labelledby="mega-title" hidden>
    <div class="category-mega-inner">
      <div class="mega-copy"><p class="eyebrow">Explora la colección</p><h2 id="mega-title">La colección</h2><p id="mega-count"></p><a class="editorial-textlink" id="mega-explore" href="#catalogo" data-category="all">Ver categoría <span aria-hidden="true">↗</span></a><div class="mega-sizes" id="mega-sizes" aria-label="Tallas de esta categoría"></div><p class="mega-disclaimer">Precio, talla y disponibilidad por consulta. Las imágenes pertenecen al catálogo; algunas referencias previas son recreaciones con IA.</p></div>
      <div class="mega-products" id="mega-products"></div>
      <button class="icon-button mega-close" type="button" data-mega-close aria-label="Cerrar submenú de categorías">×</button>
    </div>
  </section>
</nav>

```

## src/styles/sticky-header.css

```css
/* DOBLE CAPA STICKY · CSS puro. Cargar DESPUÉS de legacy/home.css.
 * La fila superior mide lo que su contenido necesita (auto).
 * La inferior tiene un tamaño de diseño constante de 56px.
 * -100% + 56px desplaza exactamente la fila auto SIN medirla con JavaScript.
 * El espacio del header permanece en el flujo: ocultarlo no provoca layout shift.
 */
:root{--category-bar-size:56px;--header-motion:240ms;}
html{scroll-behavior:smooth;scroll-padding-block-start:0;}
.header-sentinel{display:block;block-size:1px;inline-size:1px;pointer-events:none;}
.site-header{position:sticky;top:0;z-index:50;display:grid;grid-template-columns:minmax(0,1fr);grid-template-rows:auto var(--category-bar-size);inline-size:100%;min-inline-size:0;border:0;background:var(--mc-white);transform:translateY(0);transition:transform var(--header-motion) ease,box-shadow var(--header-motion) ease;will-change:transform;isolation:isolate;}
.site-header.is-compact{transform:translateY(calc(-100% + var(--category-bar-size)));}
.site-header.is-elevated{box-shadow:0 6px 20px rgba(24,30,23,.10);}
.masthead{min-inline-size:0;position:relative;z-index:60;background:var(--mc-white);}
.site-header.is-compact .masthead{pointer-events:none;}
/* No se usa display:none para ocultar la fila superior. JS aplica inert y aria-hidden. */
.site-header .hwrap{width:100%;min-width:0;display:grid;grid-template-columns:minmax(0,1fr) auto;gap:8px 12px;padding:10px 16px;max-width:var(--mc-wrap);}
.site-header .brand{min-height:44px;gap:8px;justify-self:start;}
.site-header .brand-wordmark strong{font-size:31px;}
.site-header .brand-wordmark span{font-size:6.8px;letter-spacing:1.1px;}
.site-header .brand img{width:30px;height:30px;}
.site-header .search{grid-column:1/-1;grid-row:2;max-width:none;width:100%;min-width:0;justify-self:stretch;}
.site-header .search input{font-size:16px;height:44px;}
.site-header .sugg{max-height:55svh;}
.header-actions{display:flex;align-items:center;gap:2px;}
.header-icon,.category-control{display:inline-flex;align-items:center;justify-content:center;position:relative;flex:0 0 44px;inline-size:44px;min-block-size:44px;border:0;background:transparent;color:var(--mc-ink);cursor:pointer;text-decoration:none;}
.header-icon svg,.category-control svg{width:21px;height:21px;fill:none;stroke:currentColor;stroke-width:1.5;stroke-linecap:round;stroke-linejoin:round;}
.header-icon:hover,.category-control:hover:not(:disabled){color:var(--mc-rose);background:#f2eee7;}
.favorite-counter{position:absolute;right:0;top:0;min-width:17px;min-height:17px;display:flex;align-items:center;justify-content:center;padding:1px 4px;background:var(--mc-rose);color:#fff;border-radius:12px;font:600 9px/1.5 var(--mc-sans);}
.header-contact{display:none;}
/* Fila inferior sticky. El padre sticky es global, no vive dentro del catálogo. */
.category-bar{min-inline-size:0;position:sticky;top:0;z-index:50;block-size:var(--category-bar-size);background:var(--mc-white);border-block:1px solid var(--mc-line);}
.category-bar-inner{width:100%;min-width:0;max-width:var(--mc-wrap);height:100%;margin:auto;display:flex;align-items:center;padding-inline:8px;}
.category-control:disabled{opacity:.25;cursor:default;}
.category-reveal{border-inline-end:1px solid var(--mc-line);margin-inline-end:4px;}
.category-prev{display:none;}
.category-next.is-reverse svg{transform:rotate(180deg);}
.category-viewport{min-width:0;flex:1;position:relative;align-self:stretch;}
.category-viewport::before,.category-viewport::after{content:'';position:absolute;top:0;bottom:0;z-index:2;inline-size:22px;pointer-events:none;opacity:0;transition:opacity var(--header-motion) ease;}
.category-viewport::before{left:0;background:linear-gradient(90deg,var(--mc-white),transparent);}
.category-viewport::after{right:0;background:linear-gradient(270deg,var(--mc-white),transparent);}
.category-viewport.can-scroll-left::before,.category-viewport.can-scroll-right::after{opacity:1;}
.category-list{display:flex;align-items:stretch;gap:4px;list-style:none;margin:0;padding:0;block-size:100%;overflow-x:auto;overflow-y:hidden;scroll-snap-type:x mandatory;scrollbar-width:none;overscroll-behavior-x:contain;-webkit-overflow-scrolling:touch;}
.category-list::-webkit-scrollbar{display:none;}
.category-item{display:flex;align-items:center;flex:0 0 auto;position:relative;scroll-snap-align:start;scroll-snap-stop:normal;}
.category-link.chip{display:inline-flex;align-items:center;gap:6px;position:relative;min-height:44px;border:0;border-radius:0;background:none;padding:4px 4px 4px 10px;font:500 11px/1.3 var(--mc-sans);color:#55594f;text-decoration:none;white-space:nowrap;}
.category-link__label{display:block;max-width:153px;overflow:hidden;text-overflow:ellipsis;}
.category-count{font-size:9px;color:#62665b;}
.category-link::after{content:'';position:absolute;bottom:2px;left:10px;right:4px;height:2px;background:currentColor;transform:scaleX(0);transform-origin:left;transition:transform var(--header-motion) ease;}
.category-link:hover,.category-link[aria-current="page"]{color:var(--mc-rose);}
.category-link:hover::after,.category-link[aria-current="page"]::after{transform:scaleX(1);}
.category-link[aria-current="page"] .category-count{color:var(--mc-rose);}
.category-expand{width:44px;height:44px;display:inline-flex;align-items:center;justify-content:center;border:0;background:transparent;color:#55594f;cursor:pointer;}
.category-expand svg{width:13px;height:13px;fill:none;stroke:currentColor;stroke-width:1.6;transition:transform var(--header-motion) ease;}
.category-expand[aria-expanded="true"] svg{transform:rotate(180deg);}
.category-link:focus-visible,.category-expand:focus-visible{outline:2px solid var(--mc-rose);outline-offset:-4px;}
.category-empty{padding:14px;font-size:12px;color:var(--mc-muted);}
/* Mega-menú en overlay: sin cambiar scrollTop ni bloquear el scroll de fondo. */
.category-mega{position:absolute;top:100%;inset-inline:0;max-width:none;margin:0;padding:0;background:var(--mc-white);border-bottom:1px solid var(--mc-line);box-shadow:0 15px 25px rgba(25,30,23,.12);max-height:70svh;overflow:auto;overscroll-behavior:contain;}
.category-mega-inner{position:relative;max-width:var(--mc-wrap);margin:auto;display:grid;grid-template-columns:1fr;padding:26px 20px 24px;gap:22px;}
.mega-copy{min-width:0;padding-right:35px;}
.mega-copy h2{font:400 32px/1.1 var(--mc-serif);letter-spacing:-.6px;margin:10px 0;}
#mega-count{font-size:12px;color:var(--mc-muted);line-height:1.7;}
#mega-explore{font-size:11px;margin-top:10px;}
.mega-sizes{display:flex;flex-wrap:wrap;gap:6px;margin-top:16px;}
.mega-sizes button{min-width:44px;min-height:44px;padding:7px 12px;border:1px solid var(--mc-line);background:transparent;color:var(--mc-ink);font:500 11px/1.4 var(--mc-sans);cursor:pointer;}
.mega-sizes button:hover{border-color:var(--mc-rose);color:var(--mc-rose);}
.mega-disclaimer{font-size:10px;line-height:1.6;color:var(--mc-muted);margin-top:14px;max-width:360px;}
.mega-products{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:10px;min-width:0;}
.mega-product{display:block;text-decoration:none;color:var(--mc-ink);min-width:0;}
.mega-product img{width:100%;height:clamp(100px,27vw,230px);object-fit:cover;display:block;background:#edeae2;}
.mega-product span{display:block;font:500 10px/1.5 var(--mc-sans);margin-top:8px;}
.mega-product:hover span{text-decoration:underline;}
.mega-close{position:absolute;top:14px;right:14px;background:var(--mc-white);font-size:25px;}
/* Secciones del catálogo: conservan su lugar para un scrollspy real. */
#catalogo{scroll-margin-top:calc(var(--category-bar-size) + 16px);}
.catalog-intro{scroll-margin-top:calc(var(--category-bar-size) + 16px);}
.catalog-intro h1{font:400 33px/1.1 var(--mc-serif);letter-spacing:-.6px;}
.catalog-nav-hint{font-size:11px;color:var(--mc-muted);line-height:1.65;margin:2px 0 12px;}
#grid{display:block;}
.catalog-end-sentinel{display:block;width:1px;height:1px;}
.catalog-category{max-width:none;min-block-size:130px;padding:0;margin:0 0 44px;scroll-margin-block-start:calc(var(--category-bar-size) + 20px);}
.catalog-category-heading{display:flex;justify-content:space-between;align-items:baseline;gap:15px;padding:24px 0 18px;border-top:1px solid var(--mc-line);}
.catalog-category-heading h2{font:400 30px/1.15 var(--mc-serif);letter-spacing:-.6px;}
.catalog-category-heading p{font-size:11px;color:var(--mc-muted);white-space:nowrap;}
.category-products{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:10px;}
.category-no-results{padding:20px 0 24px;color:var(--mc-muted);font-size:12px;line-height:1.7;}
.category-no-results button{min-height:44px;background:none;border:0;text-decoration:underline;color:var(--mc-rose);font-weight:500;cursor:pointer;}
/* Favoritos locales: los iconos del header no son botones decorativos. */
.product-favorite{position:absolute;top:8px;right:8px;z-index:3;width:44px;height:44px;border:1px solid #dfddd4;background:rgba(255,254,250,.96);color:var(--mc-ink);border-radius:50%;display:flex;align-items:center;justify-content:center;cursor:pointer;}
.product-favorite svg{width:20px;height:20px;fill:none;stroke:currentColor;stroke-width:1.5;}
.product-favorite[aria-pressed="true"]{color:var(--mc-rose);}
.product-favorite[aria-pressed="true"] svg{fill:currentColor;}
.header-space{width:calc(100% - 32px);max-width:580px;max-height:85svh;overflow:auto;margin:auto;border:0;padding:32px 24px;background:var(--mc-white);color:var(--mc-ink);}
.header-space::backdrop{background:rgba(20,26,19,.55);}
.header-space h2{font:400 40px/1.1 var(--mc-serif);margin:12px 44px 20px 0;letter-spacing:-1px;}
.header-space-close{position:absolute;right:12px;top:12px;font-size:26px;}
.space-intro{font-size:13px;line-height:1.8;color:var(--mc-muted);margin-bottom:20px;}
.space-storage-note{font-size:10px;line-height:1.8;color:var(--mc-muted);border-top:1px solid var(--mc-line);margin-top:24px;padding-top:15px;}
.favorite-list{list-style:none;margin:16px 0;}
.favorite-list li{display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--mc-line);}
.favorite-list a{display:flex;align-items:center;gap:14px;min-height:80px;flex:1;text-decoration:none;color:var(--mc-ink);font-size:12px;font-weight:500;}
.favorite-list img{width:40px;height:56px;object-fit:cover;}
.favorite-remove{flex:0 0 44px;width:44px;height:44px;background:none;border:0;color:var(--mc-rose);font-size:24px;cursor:pointer;}
.space-actions{display:flex;gap:12px;flex-wrap:wrap;}
#pdp-favorite{gap:9px;}
#pdp-favorite[aria-pressed="true"]{color:var(--mc-rose);border-color:var(--mc-rose);}
/* El índice editorial deja de ser una tercera capa sticky que podría solaparse. */
.home-index{position:relative;top:auto;z-index:auto;}
@media(min-width:768px){
  .site-header .hwrap{grid-template-columns:auto minmax(180px,1fr) auto;padding:14px var(--mc-gutter);gap:24px;}
  .site-header .search{grid-column:auto;grid-row:auto;max-width:380px;justify-self:center;}
  .site-header .search input{font-size:14px;}
  .site-header .brand-wordmark strong{font-size:36px;}
  .site-header .brand img{width:34px;height:34px;}
  .category-bar-inner{padding-inline:var(--mc-gutter);}
  .category-prev{display:inline-flex;}
  .category-link.chip{font-size:12px;padding-left:12px;}
  .category-link__label{max-width:200px;}
  .category-list{scroll-snap-type:x mandatory;}
  .category-mega-inner{grid-template-columns:1fr 1.75fr;padding:32px var(--mc-gutter);gap:40px;}
  .mega-products{gap:18px;}
  .mega-product img{height:225px;}
  .mega-copy{padding-right:0;}
  .mega-copy h2{font-size:39px;}
  .category-products{grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:18px;}
  .catalog-category-heading h2{font-size:38px;}
  .catalog-category{margin-bottom:55px;}
}
@media(min-width:1024px){.header-contact{display:inline-flex;align-items:center;min-height:44px;margin-left:16px;color:var(--mc-ink);font-size:11px;text-decoration:none;}}
@media(prefers-reduced-motion:reduce){
  .site-header,.category-link::after,.category-viewport::before,.category-viewport::after,.category-expand svg{transition:none!important;}
  html{scroll-behavior:auto;}
}

```

## src/navigation/scroll-direction.js

```javascript
/* Ayudante vanilla reutilizable; no hook de React ni librería de sticky.
 * IntersectionObserver detecta límites/secciones, NO avisa de cada cambio de
 * dirección dentro de una sección larga. Un scroll pasivo + rAF resuelve eso
 * sin leer geometría del DOM ni escribir estilos por cada píxel.
 */
window.createScrollDirectionObserver = function createScrollDirectionObserver(onChange, {threshold=12, topGuard=96}={}) {
  let lastY=Math.max(0,window.scrollY), lastSign=0, travel=0, lastDirection='up', frame=0;
  function sample(){
    frame=0;
    const y=Math.max(0,window.scrollY), delta=y-lastY;
    lastY=y;
    if(y<=topGuard){travel=0;lastSign=0;lastDirection='up';onChange('up',{y,atTop:true});return;}
    if(Math.abs(delta)<1)return;
    const sign=Math.sign(delta);
    travel=sign===lastSign?travel+Math.abs(delta):Math.abs(delta);
    lastSign=sign;
    if(travel>=threshold){
      const direction=sign>0?'down':'up';
      // Emitir también si continúa bajando después de soltar el foco/bloqueo.
      onChange(direction,{y,changed:direction!==lastDirection,atTop:false});
      lastDirection=direction;travel=0;
    }
  }
  function onScroll(){if(!frame)frame=requestAnimationFrame(sample);}
  window.addEventListener('scroll',onScroll,{passive:true});
  return {reset(){lastY=Math.max(0,window.scrollY);travel=0;lastSign=0;},destroy(){window.removeEventListener('scroll',onScroll);if(frame)cancelAnimationFrame(frame);}};
};

```

## src/scripts/sticky-header.js

```javascript
/* HEADER / CATEGORY BAR · vanilla JS, sin librerías de sticky.
 * Contrato: CATS, ALL, setScreen, openPDP y filtros existen en store.js.
 * Este archivo solo actualiza clases, ARIA, contenido de overlays y URL.
 * NUNCA mide la altura del header ni modifica top/height durante el scroll.
 */
(() => {
  'use strict';
  const root=document.getElementById('site-header');
  if(!root)return;
  const config=JSON.parse(document.getElementById('header-data').textContent);
  const categories=[{id:'all',label:'Todo',description:'La colección completa, sin precios publicados.',featuredIds:[]},...config.categories];
  const byId=new Map(categories.map(c=>[c.id,c]));
  const list=document.getElementById('chips'),viewport=document.getElementById('category-viewport');
  const masthead=document.getElementById('masthead'),mega=document.getElementById('category-mega');
  const space=document.getElementById('header-space'),spaceContent=document.getElementById('header-space-content');
  const finePointer=matchMedia('(hover:hover) and (pointer:fine)'),reduced=matchMedia('(prefers-reduced-motion:reduce)');
  const clean=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const products=()=>typeof ALL==='undefined'?[]:ALL;
  const image=p=>config.imageMap[p.imagen]||p.imagen;
  const motion=()=>reduced.matches?'instant':'smooth';
  const state={active:'all',collapsed:false,openMenu:null,lastInput:'pointer',target:null,ready:!!window.MC_CATALOG_READY,spaceView:'favorites',persistent:true};
  let sectionObserver=null,topObserver=null,endObserver=null,resizeObserver=null,visible=new Map(),atEnd=false;
  let hoverTimer=0,closeTimer=0,navigationTimer=0,resizeTimer=0,rebuildFrame=0,scrollFrame=0,suppressHoverUntil=0;
  let menuTrigger=null,spaceTrigger=null,initialRouteHandled=false;
  const disposers=[];
  function on(target,type,handler,options){target.addEventListener(type,handler,options);disposers.push(()=>target.removeEventListener(type,handler,options));}
  let favorites=new Set();
  function readFavorites(){
    try{const data=JSON.parse(localStorage.getItem('mc_favorites_v1')||'[]');return new Set(Array.isArray(data)?data.filter(x=>typeof x==='string'&&x.length<100):[]);}
    catch(e){state.persistent=false;return new Set();}
  }
  favorites=readFavorites();

  // ---- 1. CSS hace el sticky; JS solo decide cuándo deslizar la capa superior. ----
  function blocked(){
    return !!(state.openMenu||space.open||document.getElementById('look-dialog')?.open||
      !document.getElementById('pdp-veil').hidden||document.activeElement===document.getElementById('buscar')||
      (state.lastInput==='keyboard'&&masthead.contains(document.activeElement)));
  }
  function collapse(value,{force=false}={}){
    if(value&&!force&&blocked())return;
    if(state.collapsed===value)return;
    state.collapsed=value;
    root.classList.toggle('is-compact',value);
    root.dataset.compact=String(value);
    masthead.inert=value;
    if(value)masthead.setAttribute('aria-hidden','true');else masthead.removeAttribute('aria-hidden');
    root.querySelector('[data-header-reveal]').setAttribute('aria-expanded',String(!value));
  }
  function reveal({focusSearch=false}={}){
    closeMenu();collapse(false,{force:true});
    if(focusSearch)requestAnimationFrame(()=>document.getElementById('buscar').focus({preventScroll:true}));
  }
  const direction=window.createScrollDirectionObserver((value,{atTop})=>{
    if(state.target||blocked())return;
    collapse(!atTop&&value==='down');
  },{threshold:12,topGuard:96});
  if('IntersectionObserver' in window){
    topObserver=new IntersectionObserver(entries=>{
      const atTop=entries[0].isIntersecting;
      root.classList.toggle('is-elevated',!atTop);
      if(atTop&&!state.target)collapse(false,{force:true});
    },{threshold:0});
    topObserver.observe(document.getElementById('header-sentinel'));
  }

  // ---- 2. URL opcional. Falla con elegancia en file/iframes opacos. ----
  function requestedCategory(){try{return new URL(location.href).searchParams.get('cat');}catch(e){return null;}}
  function writeURL(id,mode='replace'){
    try{
      const url=new URL(location.href);
      if(id)url.searchParams.set('cat',id);else url.searchParams.delete('cat');
      if(url.hash.startsWith('#categoria-')||url.hash==='#catalogo')url.hash='';
      if(url.href!==location.href)history[mode==='push'?'pushState':'replaceState'](null,'',url);
    }catch(e){/* Sandbox/file sin History API: toda la navegación local sigue operativa. */}
  }
  function ensureLinkVisible(link){
    if(!link)return;
    const a=link.getBoundingClientRect(),b=list.getBoundingClientRect();
    const delta=a.left<b.left?a.left-b.left:a.right>b.right?a.right-b.right:0;
    if(Math.abs(delta)>1)list.scrollBy({left:delta,behavior:reduced.matches?'instant':'smooth'});
  }
  function activate(id,{persist=true,scrollLink=true}={}){
    if(!byId.has(id))return;
    const changed=state.active!==id;
    state.active=id;
    if(typeof cat!=='undefined')cat=id; // compatibilidad; ya no filtra ni vuelve a renderizar
    list.querySelectorAll('[data-category]').forEach(a=>{
      const active=a.dataset.category===id;
      if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');
    });
    if(scrollLink&&changed)ensureLinkVisible(list.querySelector(`[data-category="${id}"]`));
    if(persist&&document.body.dataset.screen==='catalogo'&&!state.target)writeURL(id);
    if(changed)document.dispatchEvent(new CustomEvent('mc:category-change',{detail:{id}}));
  }
  function pickVisible(){
    if(document.body.dataset.screen!=='catalogo'||state.target)return;
    if(atEnd){const last=[...document.querySelectorAll('.catalog-category[data-category-section]')].at(-1);if(last){activate(last.dataset.categorySection);return;}}
    const candidates=[...visible.entries()].filter(([,entry])=>entry.target.isConnected);
    if(!candidates.length)return;
    const readingLine=innerHeight*.36;
    candidates.sort((a,b)=>Math.abs(a[1].target.getBoundingClientRect().top-readingLine)-Math.abs(b[1].target.getBoundingClientRect().top-readingLine));
    activate(candidates[0][0]);
  }
  function rebuildSections(){
    sectionObserver?.disconnect();endObserver?.disconnect();visible.clear();atEnd=false;
    if(!('IntersectionObserver' in window))return;
    // Porcentajes de rootMargin se resuelven con el ANCHO en la especificación.
    // Se convierten alturas de viewport a px, sin medir la altura del header.
    const top=Math.round(innerHeight*.36),bottom=Math.round(innerHeight*.49);
    sectionObserver=new IntersectionObserver(entries=>{
      entries.forEach(entry=>{
        const id=entry.target.dataset.categorySection;
        if(entry.isIntersecting)visible.set(id,entry);else visible.delete(id);
      });
      pickVisible();
    },{rootMargin:`-${top}px 0px -${bottom}px 0px`,threshold:0});
    document.querySelectorAll('[data-category-section]').forEach(el=>sectionObserver.observe(el));
    const end=document.getElementById('catalog-end-sentinel');
    if(end){endObserver=new IntersectionObserver(entries=>{atEnd=entries[0].isIntersecting;pickVisible();});endObserver.observe(end);}
  }
  function queueRebuild(){if(rebuildFrame)cancelAnimationFrame(rebuildFrame);rebuildFrame=requestAnimationFrame(()=>{rebuildFrame=0;rebuildSections();updateOverflow();updateFavorites();});}
  function finishNavigation(){clearTimeout(navigationTimer);state.target=null;direction.reset();pickVisible();}
  function goCategory(id,{historyMode='push',behavior=motion()}={}){
    if(!byId.has(id))return;
    closeMenu();if(space.open)space.close();
    suppressHoverUntil=performance.now()+700;
    state.target=id;
    clearTimeout(navigationTimer);
    if(document.body.dataset.screen!=='catalogo')setScreen('catalogo');
    activate(id,{persist:false});
    if(historyMode!=='none')writeURL(id,historyMode);
    // Un destino de categoría queda debajo de la barra compacta, nunca tapado.
    collapse(id!=='all',{force:true});
    requestAnimationFrame(()=>{
      const target=id==='all'?document.getElementById('catalogo'):document.getElementById(`categoria-${id}`);
      if(id==='all')window.scrollTo({top:0,left:0,behavior});
      else if(target)target.scrollIntoView({behavior,block:'start'});
      navigationTimer=setTimeout(finishNavigation,reduced.matches||behavior==='instant'||behavior==='auto'?100:1800);
    });
  }
  on(document,'scrollend',event=>{if(state.target&&(event.target===document||event.target===document.documentElement))finishNavigation();});
  on(window,'wheel',()=>{if(state.target)finishNavigation();},{passive:true});
  on(window,'touchstart',()=>{if(state.target)finishNavigation();},{passive:true});
  on(window,'popstate',()=>{
    const id=requestedCategory();
    if(byId.has(id))goCategory(id,{historyMode:'none',behavior:'instant'});
    else{state.target=null;setScreen('inicio');}
  });

  // ---- 3. Scroll horizontal y degradados. No se toca el scroll vertical. ----
  function updateOverflow(){
    const max=Math.max(0,list.scrollWidth-list.clientWidth),left=list.scrollLeft;
    viewport.classList.toggle('can-scroll-left',left>2);
    viewport.classList.toggle('can-scroll-right',left<max-2);
    root.querySelector('[data-categories-prev]').disabled=left<=2;
    const reverse=max>2&&left>=max-2;
    const next=root.querySelector('[data-categories-next]');
    next.disabled=max<=2;next.classList.toggle('is-reverse',reverse);
    next.setAttribute('aria-label',reverse?'Volver a las primeras categorías':'Ver más categorías');
  }
  on(list,'scroll',()=>{if(!scrollFrame)scrollFrame=requestAnimationFrame(()=>{scrollFrame=0;updateOverflow();});},{passive:true});
  function moveCategories(sign){list.scrollBy({left:sign*list.clientWidth*.8,behavior:motion()});}
  on(root.querySelector('[data-categories-prev]'),'click',()=>moveCategories(-1));
  on(root.querySelector('[data-categories-next]'),'click',()=>moveCategories(list.scrollLeft>=list.scrollWidth-list.clientWidth-2?-1:1));
  if('ResizeObserver' in window){resizeObserver=new ResizeObserver(updateOverflow);resizeObserver.observe(list);}

  // ---- 4. Mega-menú. Enlaces semánticos, NO role=menu sin implementación completa. ----
  function categoryProducts(id){return products().filter(p=>id==='all'||(p.categoria||'tops')===id);}
  function openMenu(id,{focus=false,trigger=null}={}){
    if(!byId.has(id))return;
    clearTimeout(hoverTimer);clearTimeout(closeTimer);
    if(state.openMenu!==id){
      const category=byId.get(id),all=categoryProducts(id);
      const preferred=category.featuredIds.map(pid=>all.find(p=>p.id===pid)).filter(Boolean);
      const selected=[...preferred,...all.filter(p=>!preferred.includes(p))].slice(0,3);
      document.getElementById('mega-title').textContent=category.label;
      document.getElementById('mega-count').textContent=`${all.length} ${all.length===1?'prenda':'prendas'} · ${category.description}`;
      const explore=document.getElementById('mega-explore');explore.dataset.category=id;explore.href=id==='all'?'#catalogo':`#categoria-${id}`;
      const sizes=[...new Set(all.flatMap(p=>tokensTalla(p.tallas)))];
      document.getElementById('mega-sizes').innerHTML=sizes.map(size=>`<button type="button" data-menu-size="${clean(size)}" data-size-category="${id}" aria-label="Ver ${clean(category.label)} en talla ${clean(size)}">${clean(size)}</button>`).join('');
      document.getElementById('mega-products').innerHTML=selected.map(p=>`<a class="mega-product" href="#catalogo" data-header-product="${clean(p.id)}"><img src="${clean(image(p))}" alt="${clean(p.nombre)} — imagen del catálogo" width="300" height="400" loading="lazy" decoding="async"><span>${clean(p.nombre)}</span></a>`).join('')||'<p class="category-empty">No hay prendas activas en esta categoría.</p>';
    }
    state.openMenu=id;
    menuTrigger=trigger||list.querySelector(`[data-mega-for="${id}"]`);
    mega.hidden=false;
    list.querySelectorAll('[data-mega-for]').forEach(button=>button.setAttribute('aria-expanded',String(button.dataset.megaFor===id)));
    document.getElementById('sugg').hidden=true;
    if(focus)requestAnimationFrame(()=>document.getElementById('mega-explore').focus({preventScroll:true}));
  }
  function closeMenu({focus=false}={}){
    clearTimeout(hoverTimer);clearTimeout(closeTimer);
    const wasOpen=state.openMenu!==null;
    state.openMenu=null;mega.hidden=true;
    list.querySelectorAll('[data-mega-for]').forEach(button=>button.setAttribute('aria-expanded','false'));
    if(focus&&wasOpen)menuTrigger?.focus({preventScroll:true});
  }
  on(root,'pointerover',event=>{
    if(!finePointer.matches||performance.now()<suppressHoverUntil)return;
    clearTimeout(closeTimer);
    const item=event.target.closest('.category-item');
    if(!item||item.contains(event.relatedTarget))return;
    clearTimeout(hoverTimer);
    hoverTimer=setTimeout(()=>openMenu(item.dataset.categoryItem),150);
  });
  on(document.getElementById('category-bar'),'pointerleave',()=>{if(finePointer.matches)closeTimer=setTimeout(()=>closeMenu(),220);});
  on(document,'pointerdown',event=>{
    state.lastInput='pointer';
    if(!root.contains(event.target))closeMenu();
  },{capture:true});
  on(document,'focusin',event=>{
    if(event.target===document.getElementById('buscar'))closeMenu();
    if(masthead.contains(event.target)&&state.collapsed)collapse(false,{force:true});
    if(state.openMenu&&!root.contains(event.target))closeMenu();
  });
  on(document,'keydown',event=>{
    state.lastInput='keyboard';
    if(event.key==='Escape'&&state.openMenu){event.preventDefault();closeMenu({focus:true});return;}
    const item=event.target.closest('.category-item');
    if(!item)return;
    if(event.key==='ArrowDown'){event.preventDefault();openMenu(item.dataset.categoryItem,{focus:true,trigger:event.target});return;}
    if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;
    event.preventDefault();closeMenu();
    const links=[...list.querySelectorAll('.category-link')].filter(a=>!a.closest('[hidden]'));
    const index=links.findIndex(a=>a.closest('.category-item')===item);
    const next=event.key==='Home'?0:event.key==='End'?links.length-1:(index+(event.key==='ArrowRight'?1:-1)+links.length)%links.length;
    links[next]?.focus({preventScroll:true});ensureLinkVisible(links[next]);
  });

  // ---- 5. Favoritos locales y espacio informativo, sin cuenta ni acceso obligatorio. ----
  function toggleFavorite(id){
    const p=products().find(p=>p.id===id);if(!p)return false;
    favorites.has(id)?favorites.delete(id):favorites.add(id);
    try{localStorage.setItem('mc_favorites_v1',JSON.stringify([...favorites]));}catch(e){state.persistent=false;}
    updateFavorites();
    if(space.open&&state.spaceView==='favorites'){
      const hadFocus=space.contains(document.activeElement);renderSpace();
      if(hadFocus)(space.querySelector('.favorite-remove')||space.querySelector('[data-space-close]')).focus({preventScroll:true});
    }
    return favorites.has(id);
  }
  function updateFavorites(){
    const count=products().filter(p=>favorites.has(p.id)).length;
    document.querySelectorAll('[data-favorite-count]').forEach(el=>{el.textContent=count;el.hidden=!count;});
    root.querySelector('[data-open-favorites]').setAttribute('aria-label',`Ver favoritos: ${count} ${count===1?'prenda guardada':'prendas guardadas'}`);
    document.querySelectorAll('[data-favorite-id]').forEach(button=>{
      const active=favorites.has(button.dataset.favoriteId),p=products().find(p=>p.id===button.dataset.favoriteId);
      button.setAttribute('aria-pressed',String(active));
      button.setAttribute('aria-label',`${active?'Quitar de':'Guardar en'} favoritos${p?': '+p.nombre:''}`);
      if(button.id==='pdp-favorite')button.textContent=active?'♥ Guardado en favoritos':'♡ Guardar en favoritos';
    });
    document.getElementById('favorite-storage-note').textContent=state.persistent?'Los favoritos se guardan solo en este navegador. No creamos una cuenta ni solicitamos datos personales.':'Este navegador bloquea el almacenamiento local. Puedes usar favoritos durante esta sesión, pero no se conservarán al cerrar.';
  }
  function renderSpace(){
    const saved=products().filter(p=>favorites.has(p.id));
    document.getElementById('header-space-title').textContent=state.spaceView==='favorites'?'Tus favoritos':'Tu espacio, sin registro';
    if(state.spaceView==='account'){
      spaceContent.innerHTML=`<p class="space-intro">No necesitas iniciar sesión para explorar la colección. Esta versión no crea cuentas de cliente: tus favoritos son locales y las consultas se atienden personalmente por WhatsApp.</p><div class="space-actions"><button class="editorial-button editorial-button--dark" type="button" data-open-favorites>Ver favoritos (${saved.length})</button><a class="editorial-textlink" href="https://wa.me/59164134784" target="_blank" rel="noopener noreferrer">Contactar con M&amp;C ↗</a></div>`;
    }else{
      spaceContent.innerHTML=saved.length?`<ul class="favorite-list">${saved.map(p=>`<li><a href="#catalogo" data-header-product="${clean(p.id)}"><img src="${clean(image(p))}" alt="" width="40" height="56" loading="lazy"><span>${clean(p.nombre)}</span></a><button class="favorite-remove" type="button" data-favorite-id="${clean(p.id)}" aria-label="Quitar de favoritos: ${clean(p.nombre)}" aria-pressed="true">×</button></li>`).join('')}</ul>`:'<p class="space-intro">Aún no has guardado prendas. Toca el corazón de una tarjeta o «Guardar en favoritos» en una ficha para volver a encontrarlas aquí.</p>';
    }
  }
  function openSpace(view,trigger){
    closeMenu();collapse(false,{force:true});state.spaceView=view;spaceTrigger=trigger;
    renderSpace();updateFavorites();document.body.style.overflow='hidden';
    if(!space.open)space.showModal();else space.querySelector('[data-space-close]').focus({preventScroll:true});
  }
  function productFromOverlay(id,trigger){
    const returnFocus=state.openMenu?menuTrigger:space.open?spaceTrigger:trigger;
    closeMenu();if(space.open)space.close();
    document.dispatchEvent(new CustomEvent('mc:pdp-return-focus',{detail:{element:returnFocus}}));
    openPDP(id);
  }
  on(space,'close',()=>{if(document.getElementById('pdp-veil').hidden){document.body.style.overflow='';spaceTrigger?.focus({preventScroll:true});}});
  on(space,'click',event=>{if(event.target!==space)return;const r=space.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)space.close();});
  on(space,'keydown',event=>{
    if(event.key!=='Tab')return;
    const items=[...space.querySelectorAll('button:not([disabled]),a[href]')].filter(el=>el.getClientRects().length);
    if(event.shiftKey&&document.activeElement===items[0]){event.preventDefault();items.at(-1)?.focus();}
    else if(!event.shiftKey&&document.activeElement===items.at(-1)){event.preventDefault();items[0]?.focus();}
  });
  on(window,'storage',event=>{if(event.key==='mc_favorites_v1'){favorites=readFavorites();updateFavorites();if(space.open)renderSpace();}});
  // Captura: evita que el corazón dispare el onclick de la tarjeta padre.
  on(document,'click',event=>{
    const favorite=event.target.closest('[data-favorite-id]');
    if(!favorite)return;
    event.preventDefault();event.stopPropagation();toggleFavorite(favorite.dataset.favoriteId);
  },{capture:true});

  // ---- 6. Delegación de acciones. Enlace y flecha desplegable son controles distintos. ----
  on(document,'click',event=>{
    const target=event.target.closest('a,button');if(!target)return;
    if(target.tagName==='A'&&(event.ctrlKey||event.metaKey||event.shiftKey||event.altKey||event.button!==0))return;
    if(target.hasAttribute('data-category')){event.preventDefault();goCategory(target.dataset.category);}
    else if(target.hasAttribute('data-mega-for')){event.preventDefault();state.openMenu===target.dataset.megaFor?closeMenu():openMenu(target.dataset.megaFor,{trigger:target});}
    else if(target.hasAttribute('data-mega-close')){event.preventDefault();closeMenu({focus:true});}
    else if(target.hasAttribute('data-header-reveal')){event.preventDefault();reveal({focusSearch:true});}
    else if(target.hasAttribute('data-menu-size')){
      event.preventDefault();tallasSel.clear();tallasSel.add(target.dataset.menuSize);renderSizes();render();goCategory(target.dataset.sizeCategory);
    }else if(target.hasAttribute('data-header-product')){event.preventDefault();productFromOverlay(target.dataset.headerProduct,target);}
    else if(target.hasAttribute('data-open-favorites')){event.preventDefault();openSpace('favorites',root.querySelector('[data-open-favorites]'));}
    else if(target.hasAttribute('data-open-space')){event.preventDefault();openSpace('account',target);}
    else if(target.hasAttribute('data-space-close')){event.preventDefault();space.close();}
  });
  on(document,'mc:pdp-open',event=>{
    const button=document.getElementById('pdp-favorite');button.dataset.favoriteId=event.detail.id;updateFavorites();
  });
  on(document,'mc:screen-change',event=>{
    closeMenu();collapse(false,{force:true});direction.reset();
    if(event.detail.name!=='catalogo'){clearTimeout(navigationTimer);state.target=null;activate('all',{persist:false});writeURL(null);}
    else if(!state.target){activate('all',{persist:false});writeURL('all');}
    queueRebuild();
  });
  on(document,'mc:catalog-rendered',queueRebuild);
  function refresh(){
    const all=products();
    list.querySelectorAll('[data-category-item]').forEach(item=>{
      const id=item.dataset.categoryItem,n=id==='all'?all.length:all.filter(p=>(p.categoria||'tops')===id).length;
      item.querySelector('.category-count').textContent=`(${n})`;
      item.hidden=state.ready&&id!=='all'&&n===0;
    });
    updateFavorites();queueRebuild();
    if(!initialRouteHandled&&state.ready){
      initialRouteHandled=true;
      const id=requestedCategory();
      if(byId.has(id))goCategory(id,{historyMode:'replace',behavior:'instant'});
    }
  }
  on(document,'mc:catalog-ready',()=>{state.ready=true;refresh();});
  on(window,'resize',()=>{clearTimeout(resizeTimer);resizeTimer=setTimeout(()=>{rebuildSections();updateOverflow();},120);});
  window.MCHeader={goCategory,reveal,collapse,toggleFavorite,refresh,getState:()=>({active:state.active,collapsed:state.collapsed,openMenu:state.openMenu,favorites:[...favorites]}),destroy(){
    disposers.forEach(fn=>fn());direction.destroy();topObserver?.disconnect();sectionObserver?.disconnect();endObserver?.disconnect();resizeObserver?.disconnect();
    [hoverTimer,closeTimer,navigationTimer,resizeTimer].forEach(clearTimeout);
    [rebuildFrame,scrollFrame].forEach(cancelAnimationFrame);root.classList.remove('is-compact','is-elevated');masthead.inert=false;masthead.removeAttribute('aria-hidden');
  }};
  root.dataset.compact='false';activate('all',{persist:false,scrollLink:false});refresh();
})();

```

## src/data/categories.json

```json
{
  "description": "Categorías reales existentes. Los contadores se calculan sobre productos activos, no son valores inventados.",
  "categories": [
    {"id":"sweaters","label":"Sweaters","description":"Capas y sweaters para combinar a tu manera.","featuredIds":["sw07","sw18","sw21"]},
    {"id":"tops","label":"Mangas largas y tops","description":"Mangas largas, básicos y texturas del catálogo.","featuredIds":["top03","top02","top13"]},
    {"id":"crops","label":"Crop tops y chalecos","description":"Tops y chalecos para jugar con las capas.","featuredIds":["cr02","cr06","cr07"]},
    {"id":"chaquetas","label":"Camperas y casacas","description":"Una capa más para tu próximo look.","featuredIds":["ch01","ch02","ch03"]},
    {"id":"poleras","label":"Poleras","description":"Poleras del catálogo, con tallas por confirmar.","featuredIds":["polera"]},
    {"id":"jeans","label":"Jeans","description":"Explora los pantalones de denim del catálogo.","featuredIds":["jean"]},
    {"id":"vestidos","label":"Vestidos","description":"Vestidos y propuestas para combinar.","featuredIds":["vestido"]},
    {"id":"sport","label":"Deportivo","description":"Conjuntos para vestir a tu ritmo.","featuredIds":["conjunto"]}
  ]
}

```

## src/data/categories.mock.json

```json
{
  "mock": true,
  "publish": false,
  "description": "Casos para probar el componente aislado. No representan inventario ni se cargan en la tienda.",
  "categories": [
    {
      "id": "pantalones-demo",
      "label": "Pantalones",
      "featuredIds": [
        "pantalones-demo-01",
        "pantalones-demo-02",
        "pantalones-demo-03"
      ],
      "description": "Categoría ficticia para probar el componente; no representa inventario."
    },
    {
      "id": "poleras-demo",
      "label": "Poleras",
      "featuredIds": [
        "poleras-demo-01",
        "poleras-demo-02",
        "poleras-demo-03"
      ],
      "description": "Categoría ficticia para probar el componente; no representa inventario."
    },
    {
      "id": "vestidos-demo",
      "label": "Vestidos",
      "featuredIds": [
        "vestidos-demo-01",
        "vestidos-demo-02",
        "vestidos-demo-03"
      ],
      "description": "Categoría ficticia para probar el componente; no representa inventario."
    },
    {
      "id": "chaquetas-demo",
      "label": "Chaquetas",
      "featuredIds": [
        "chaquetas-demo-01",
        "chaquetas-demo-02",
        "chaquetas-demo-03"
      ],
      "description": "Categoría ficticia para probar el componente; no representa inventario."
    },
    {
      "id": "accesorios-demo",
      "label": "Accesorios con un nombre largo para probar el scroll",
      "featuredIds": [
        "accesorios-demo-01",
        "accesorios-demo-02",
        "accesorios-demo-03"
      ],
      "description": "Categoría ficticia para probar el componente; no representa inventario."
    }
  ],
  "cases": [
    "cero productos",
    "una categoría",
    "categorías con nombres largos",
    "100 categorías",
    "teclado",
    "RTL si se adapta el proyecto"
  ],
  "products": [
    {
      "id": "pantalones-demo-01",
      "nombre": "Pantalones · prenda DEMO 01",
      "categoria": "pantalones-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": true
    },
    {
      "id": "pantalones-demo-02",
      "nombre": "Pantalones · prenda DEMO 02",
      "categoria": "pantalones-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": false
    },
    {
      "id": "pantalones-demo-03",
      "nombre": "Pantalones · prenda DEMO 03",
      "categoria": "pantalones-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": true
    },
    {
      "id": "pantalones-demo-04",
      "nombre": "Pantalones · prenda DEMO 04",
      "categoria": "pantalones-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": false
    },
    {
      "id": "poleras-demo-01",
      "nombre": "Poleras · prenda DEMO 01",
      "categoria": "poleras-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": true
    },
    {
      "id": "poleras-demo-02",
      "nombre": "Poleras · prenda DEMO 02",
      "categoria": "poleras-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": false
    },
    {
      "id": "poleras-demo-03",
      "nombre": "Poleras · prenda DEMO 03",
      "categoria": "poleras-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": true
    },
    {
      "id": "poleras-demo-04",
      "nombre": "Poleras · prenda DEMO 04",
      "categoria": "poleras-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": false
    },
    {
      "id": "vestidos-demo-01",
      "nombre": "Vestidos · prenda DEMO 01",
      "categoria": "vestidos-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": true
    },
    {
      "id": "vestidos-demo-02",
      "nombre": "Vestidos · prenda DEMO 02",
      "categoria": "vestidos-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": false
    },
    {
      "id": "vestidos-demo-03",
      "nombre": "Vestidos · prenda DEMO 03",
      "categoria": "vestidos-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": true
    },
    {
      "id": "vestidos-demo-04",
      "nombre": "Vestidos · prenda DEMO 04",
      "categoria": "vestidos-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": false
    },
    {
      "id": "chaquetas-demo-01",
      "nombre": "Chaquetas · prenda DEMO 01",
      "categoria": "chaquetas-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": true
    },
    {
      "id": "chaquetas-demo-02",
      "nombre": "Chaquetas · prenda DEMO 02",
      "categoria": "chaquetas-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": false
    },
    {
      "id": "chaquetas-demo-03",
      "nombre": "Chaquetas · prenda DEMO 03",
      "categoria": "chaquetas-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": true
    },
    {
      "id": "chaquetas-demo-04",
      "nombre": "Chaquetas · prenda DEMO 04",
      "categoria": "chaquetas-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": false
    },
    {
      "id": "accesorios-demo-01",
      "nombre": "Accesorios · prenda DEMO 01",
      "categoria": "accesorios-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": true
    },
    {
      "id": "accesorios-demo-02",
      "nombre": "Accesorios · prenda DEMO 02",
      "categoria": "accesorios-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": false
    },
    {
      "id": "accesorios-demo-03",
      "nombre": "Accesorios · prenda DEMO 03",
      "categoria": "accesorios-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": true
    },
    {
      "id": "accesorios-demo-04",
      "nombre": "Accesorios · prenda DEMO 04",
      "categoria": "accesorios-demo",
      "tallas": "S – M – L",
      "imagen": "/img/placeholder.svg",
      "descripcion": "Prenda ficticia para probar el header y la navegación; no se vende ni representa stock real.",
      "activo": true,
      "nuevo": false
    }
  ]
}

```
