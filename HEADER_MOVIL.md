# FASE 2 · Sección 1 — Header y categorías móviles

**Implementada tras tu aprobación. No se ha avanzado al hero ni a otra sección.**

La tienda usa el mismo HTML, los mismos componentes y el mismo JavaScript. Se añadió un archivo CSS comentado con overrides responsive: `src/styles/mobile-header.css`, cargado después de los estilos existentes.

## 1. Cambios aplicados, en orden de impacto

| Prioridad | Mejora | Justificación UX / implementación |
|---|---|---|
| P0 | Primera pantalla más ligera | Se oculta solo la franja informativa duplicada en móvil. El contacto sigue disponible por WhatsApp, tarjetas y footer. La cabecera conserva logo, buscador visible, favoritos y espacio informativo. |
| P0 | Masthead compacto | En teléfono pasa de 116 a 104px. Se ajustan padding, gaps y logo sin encoger el área de toque. La barra de categorías conserva sus 56px y su sticky. |
| P0 | Submenú sin quedar detrás de la barra inferior | `max-height` combina viewport pequeño, reserva CSS conservadora y safe area. No se mide el header en JS, no se usa un header fixed y no se bloquea/reemplaza la navegación. |
| P0 | X del submenú siempre alcanzable | El mismo botón pasa a 48×48px y usa `position:sticky` sobre una celda que abarca todo el contenido del panel. Sigue visible al leer las fotos, no solo durante el copy inicial. |
| P1 | Lectura y feedback táctil | Categorías 12px, contadores 10px, controles de la barra con 48px de alto, estado de tap breve y chevron abierto claramente indicado. Se conservan snap, gradientes y categoría activa. |
| P1 | Preview de dos columnas | Las mismas tres prendas del submenú se muestran en dos columnas en touch; no se crean, sustituyen ni duplican fotografías. |
| P1 | Buscador táctil | Campo visible de 16px también en tablet touch; sugerencias más legibles, sin cambiar Enter, flechas o la apertura de ficha. |
| P1 | Notch / laterales | `env(safe-area-inset-*)` reserva zona superior y bordes cuando el navegador informa insets. Al compactar se conserva esa zona, con una máscara decorativa que evita que asome el buscador debajo. |
| P2 | Coste mínimo | Solo CSS en producción; no hay nueva librería, fuente, asset ni listener. La fuente permanece comentada y el generador compacta únicamente este módulo. |

El espacio de toque del logo y los iconos superiores sigue siendo al menos 44×44px. Las flechas de categoría conservan 44px de ancho y pasan a 48px de alto; la X y las tallas del submenú son de 48×48px o más.

### Antes / después medido

Medidas con insets del navegador en cero. En un dispositivo con notch se añade la reserva segura correspondiente; no se presenta esa zona como espacio disponible para controles.

| Perfil | Header antes → después | Inicio del hero antes → después | Solape del panel antes → después |
|---|---:|---:|---:|
| se-320 | 172 → 160px | 215 → 161px | 101 → 0px |
| se-375 | 172 → 160px | 215 → 161px | 71 → 0px |
| iphone-14 | 172 → 160px | 202 → 161px | 0 → 0px |
| android-360 | 172 → 160px | 215 → 161px | 19 → 0px |
| android-414 | 172 → 160px | 202 → 161px | 0 → 0px |
| tablet-768 | 128 → 120px | 158 → 121px | 0 → 0px |
| tablet-1024 | 128 → 120px | 158 → 121px | 0 → 0px |


En el perfil 375×667 los CTA del hero ya entran encima de la barra inferior gracias al espacio recuperado, **sin cambiar el CSS del hero**. El caso más corto 320×568 todavía necesita su propia revisión del hero: no se da por solucionado todo el primer viewport.

## 2. Desktop queda igual

- Se compararon **15 vistas**: Inicio, catálogo, submenú, PDP y footer a **1024, 1440 y 1920px**, con ratón.
- Las capturas y los estilos comparados son **idénticos**. La comprobación se hizo frente al estado previo real y también activando/desactivando el override móvil en el mismo Chromium.
- Todas las reglas raíz del nuevo CSS están dentro de media queries. No hay un selector global activo fuera de ellas.
- Las reglas de teléfono usan `max-width:767.98px`. Tablet se limita a 768–1024px con `(hover:none) and (pointer:coarse)`, por lo que un PC con ratón a 1024px no cambia.
- El `body` completo del HTML web, incluidos sus scripts, conserva **exactamente los mismos bytes**. La única incorporación al documento está en el CSS de `<head>`.
- Los templates de header/category bar, controlador sticky, helper de dirección, JavaScript de Home/catálogo, estilos base, datos e imagen original siguen intactos por SHA-256.

Pruebas: `audits/mobile-header/desktop-comparison.json`, `desktop-live-comparison.json`, `source-proof.json` y `css-scope.json`.

### Qué NO se tocó

No se añadieron hamburguesa, drawer, newsletter ni componentes nuevos. No se cambiaron hero, PLP, PDP, reseñas, carrusel de Novedades, looks o footer. No se alteran fotografías, precio por consulta, contactos, cuenta informativa ni la compra por WhatsApp.

**La X corregida aquí es la del submenú de categorías. La X de PDP y sus acciones siguen pendientes de la etapa específica de ficha.** No se confunden ambos problemas.

El panel sigue siendo el dropdown existente, no un drawer modal nuevo. Su scroll interno contiene el gesto; no se añadió un bloqueo global de body para este dropdown. El bloqueo de los modales que ya existían se conserva.

## 3. Integración y archivos

Ya aplicado en:
- `web/index.html` y `site/index.html`.
- `tienda_portable.html` y su alias `catalogo_web.html`.
- Plantilla de exportación de `admin_portable.html` / `web/admin.html`.
- Demos específicas del header, sin cambiar su vista inicial de catálogo.

La tienda principal abre Inicio como antes. En PC se ve igual por diseño. Para revisar rápidamente la diferencia móvil desde un PC, abrir **`COMPARATIVA_HEADER_MOVIL.html`**, que contiene capturas reales autocontenidas.

### Código e instalación

Archivo nuevo: `src/styles/mobile-header.css`.

El generador coloca el módulo al final, sin sustituir CSS/HTML/JS anteriores:

```python
mobile_css = ' '.join(
    re.sub(r'/\*.*?\*/', '', read(SRC / 'styles/mobile-header.css'), flags=re.S).split()
)
mobile_header = '\n/* MC_MOBILE_HEADER_START */\n' + mobile_css + '\n/* MC_MOBILE_HEADER_END */\n'
styles = existing_styles + mobile_header
```

Los marcadores son comentarios CSS para pruebas; no añaden nodos. Solo se compacta el módulo nuevo, no se reescriben reglas desktop.

Para llevar el complemento a una copia del proyecto actual, conservar todos sus assets y datos y copiar los archivos incluidos en el ZIP. Reconstruir con:

```bash
python3 build_portables.py
python3 build_admin.py
python3 scripts/export_static.py
# Opcional, demos de navegación:
python3 scripts/build_header_demo.py
python3 scripts/build_header_demo.py --mock
```

No hace falta reprocesar fotografías para este cambio. El HTML portable funciona sin servidor/internet para ver la tienda. Para hosting se sigue recomendando `site/`; no publicar el admin/editor de desarrollo sin protección.

## 4. Validación de esta sección

Perfiles Chromium con touch/DPR emulados:
- 320×568 y 375×667 (formatos SE).
- 390×844 (formato iPhone 14).
- Android de referencia 360×800 y 414×896.
- Tablet 768×1024 y 1024×768.
- Horizontal 844×390.

Resultados:
- [x] Sin overflow horizontal del documento.
- [x] Buscador visible a 16px y botones con áreas medidas.
- [x] Categorías siguen visibles al bajar, cabecera vuelve al subir.
- [x] Header y documento conservan su altura durante la compactación.
- [x] Panel no solapa la barra inferior, expandido ni compacto.
- [x] X tocable tras llegar al final del panel, sin scroll automático del test para encontrarla.
- [x] Tap, Escape, flechas y devolución de foco conservados.
- [x] Sugerencia predictiva visible y Enter abre la ficha existente.
- [x] Favoritos locales y filtro real por talla conservados.
- [x] Swipe horizontal de categorías no mueve verticalmente la página.
- [x] Arrastre vertical del panel no arrastra la página; su X permanece accesible.
- [x] Cambio móvil→desktop→móvil sin estilos inline residuales del componente.
- [x] Insets CSS controlados: 47px superior y 47px laterales; se verifica geometría, no hardware iOS.
- [x] Portable offline, storage bloqueado y movimiento reducido.
- [x] Cero errores JS y cero hallazgos automáticos A/AA en Inicio y submenú de los ocho perfiles.
- [x] Regresiones de header, Home, estático y hero aprobadas.
- [ ] Safari/VoiceOver/TalkBack y teléfonos físicos: requieren comprobación real.

La auditoría automática no equivale a una certificación WCAG completa. Los insets inyectados para tests no simulan las barras del navegador ni el teclado de iOS.

### Performance actual

Una muestra por perfil, caché vacía, viewport 390×844, DPR2, CPU4×, HTTP local sin compresión. No es una garantía de producción ni una comparación estadística de velocidad.

| Perfil | Red / latencia / CPU | LCP | CLS | Objetivo <2.5s |
|---|---|---:|---:|---|
| fast-4g | 4 Mbps / 80ms / 4× | 1.34s | 0.00037 | Cumple en esta muestra |
| slow-4g | 1.6 Mbps / 150ms / 4× | 3.27s | 0.00075 | Pendiente |


El perfil lento **todavía supera 2.5s**. Este ajuste no se presenta como una solución completa al LCP: sigue pendiente revisar entrega/hosting e imágenes en las etapas que se autoricen. No se añadieron animaciones de scroll, parallax o trabajo JS nuevo para el header.

### Repetir las pruebas

```bash
npm install
npx playwright install --with-deps chromium
# En otra terminal: python3 server.py
npm run test:mobile-header
node audits/mobile-header/verify-extras.cjs
npm run test:header
npm run test:home
npm run test:static
npm run test:hero
```

`test:mobile-header` valida móvil y la igualdad de capturas desktop con/sin módulo en el mismo motor, sin depender de la rasterización de otro sistema operativo.

## 5. Capturas y siguiente aprobación

- Antes: `audits/mobile/before/` (auditoría inicial, conservada).
- Después: `audits/mobile-header/after/`.
- Comparativa offline: `COMPARATIVA_HEADER_MOVIL.html`.
- Resultado funcional: `tienda_portable.html`.

**Siguiente propuesta, aún NO aplicada:** hero móvil, manteniendo intacta su versión desktop. Se revisaría especialmente la pantalla 320×568, la escala tipográfica y una entrada móvil más sutil. También siguen pendientes PLP/PDP/footer; no se avanza automáticamente.

Testing físico recomendado antes del cierre global: SE con Safari y barras visibles, iPhone 14 con notch/home indicator y teclado abierto, Android medio con Chrome/red limitada, tablet en ambas orientaciones y con ratón/teclado externo.

---

# Código completo del override móvil

El código siguiente es una copia literal del archivo editable entregado. No se añade ningún fragmento oculto de JavaScript.

```css
/* FASE MÓVIL · sección 1: SOLO header, categorías y su submenú.
 * Cargar después de sticky-header.css. No se reemplaza ni se reordena HTML.
 * No hay selectores activos en desktop >=1025px ni en PC/tablet con ratón
 * entre 768–1024px. No se añaden listeners, librerías ni alturas medidas en JS.
 */

/* Teléfonos + tablets cuya entrada principal es táctil. */
@media (max-width:767.98px),
       (min-width:768px) and (max-width:1024px) and (hover:none) and (pointer:coarse){
  /* El contacto se conserva en WhatsApp, tarjetas y footer. Solo se oculta
   * la franja informativa repetida: libera 29–42px sin eliminar sus nodos. */
  .topbar{display:none;}
  .site-header{
    --mc-mobile-panel-reserve:14rem;
    --mc-mobile-safe-top:env(safe-area-inset-top,0px);
    --mc-mobile-safe-left:env(safe-area-inset-left,0px);
    --mc-mobile-safe-right:env(safe-area-inset-right,0px);
    padding-block-start:var(--mc-mobile-safe-top);
  }
  /* La reserva superior permanece en el flujo y también en estado compacto.
   * Así los controles no suben bajo el notch; no se mide la altura en JS. */
  .site-header.is-compact{
    --mc-mobile-panel-reserve:7.5rem;
    transform:translateY(calc(-100% + var(--category-bar-size) + var(--mc-mobile-safe-top)));
  }
  .site-header::before{
    content:"";position:absolute;inset-inline:0;top:0;
    height:var(--mc-mobile-safe-top);background:var(--mc-white);
    z-index:70;pointer-events:none;
  }
  /* Máscara de la zona insegura: no deja asomar el buscador desplazado. */
  .site-header.is-compact::before{top:calc(100% - var(--category-bar-size) - var(--mc-mobile-safe-top));}
  .site-header .header-contact{display:none;}
  .site-header .header-actions{gap:8px;}

  /* La altura de toque se conserva aunque el dibujo del logo sea menor. */
  .site-header .brand{min-height:44px;}
  .site-header .header-icon{min-width:44px;min-height:44px;}
  .site-header .header-icon svg{width:20px;height:20px;}
  .site-header .search input{font-size:16px;line-height:1.25;}

  /* Categorías: misma fila de 56px, snap y scrollspy originales.
   * 48px de alto + 44px de ancho en iconos; no se comprime la zona de toque. */
  .site-header .category-control{min-height:48px;}
  .site-header .category-expand{width:44px;height:48px;min-height:48px;}
  .site-header .category-link.chip{min-height:48px;font-size:12px;line-height:1.35;}
  .site-header .category-count{font-size:10px;}
  .site-header .category-link__label{max-width:153px;}
  .site-header .category-list{scroll-padding-inline:4px;}
  .site-header .category-viewport::before,
  .site-header .category-viewport::after{inline-size:20px;}
  .site-header .category-expand[aria-expanded="true"]{background:#f3e7eb;color:var(--mc-rose);}

  /* Feedback breve al tap. Se neutraliza el hover pegado de pantallas touch;
   * el estado abierto sigue indicado por aria-expanded y su color propio. */
  .site-header .header-icon,
  .site-header .category-control,
  .site-header .category-expand{
    transition:background-color 160ms ease,color 160ms ease,transform 160ms ease;
  }
  .site-header .header-icon:hover,
  .site-header .category-control:hover:not(:disabled){background:transparent;color:var(--mc-ink);}
  .site-header .header-icon:active,
  .site-header .category-control:active:not(:disabled),
  .site-header .category-expand:active{background:#f3e7eb;color:var(--mc-rose);transform:scale(.97);}
  .site-header .header-icon:focus-visible,
  .site-header .category-control:focus-visible,
  .site-header .category-expand:focus-visible{outline:2px solid var(--mc-rose);outline-offset:-3px;}

  /* Reserva CSS conservadora para cabecera + barra inferior + margen.
   * El fallback vh cubre navegadores antiguos; svh evita que las barras del
   * navegador reduzcan por sorpresa el espacio útil. Nada usa position:fixed.
   * rem también amplía la reserva cuando el usuario aumenta su fuente base. */
  .site-header .category-mega{
    max-height:min(70vh,calc(100vh - var(--mc-mobile-panel-reserve) - var(--mc-mobile-safe-top) - env(safe-area-inset-bottom,0px)));
    max-height:min(70svh,calc(100svh - var(--mc-mobile-panel-reserve) - var(--mc-mobile-safe-top) - env(safe-area-inset-bottom,0px)));
    overscroll-behavior:contain;
    -webkit-overflow-scrolling:touch;
    scrollbar-width:thin;
    scrollbar-color:var(--mc-muted) transparent;
  }
  .site-header .mega-close{
    width:48px;height:48px;min-height:48px;
    margin:0;border:1px solid var(--mc-line);border-radius:0;
    background:var(--mc-white);color:var(--mc-ink);font-size:26px;
    box-shadow:0 2px 8px rgba(26,26,26,.06);
    z-index:4;
  }
  .site-header .mega-close:active{background:#f3e7eb;}
  .site-header #mega-explore{min-height:48px;font-size:12px;}
  .site-header .mega-sizes{gap:8px;margin-top:12px;}
  .site-header .mega-sizes button{min-width:48px;min-height:48px;font-size:12px;}
  .site-header .mega-sizes button:active{background:#f3e7eb;color:var(--mc-rose);border-color:var(--mc-rose);}
  .site-header .mega-products{grid-template-columns:repeat(2,minmax(0,1fr));gap:16px 12px;}
  .site-header .mega-product{min-width:0;}
  .site-header .mega-product img{height:clamp(120px,36vw,180px);}
  .site-header .mega-product span{font-size:11px;line-height:1.5;margin-top:8px;}
  .site-header .mega-product:active{opacity:.8;}
  .site-header .mega-disclaimer{font-size:11px;line-height:1.65;}

  /* El dropdown predictivo sigue siendo el mismo: filas más claras y cómodas.
   * No cambia Enter, las flechas del buscador ni la selección de una prenda. */
  .site-header .sugg{max-height:min(55svh,calc(100svh - var(--mc-mobile-panel-reserve) - var(--mc-mobile-safe-top)));}
  .site-header .sugg-item{min-height:48px;padding:8px 12px;gap:10px;}
  .site-header .sugg-item img{width:36px;height:48px;flex-shrink:0;}
  .site-header .sugg-item .nm{font-size:14px;line-height:1.4;}
  .site-header .sugg-item .ct{font-size:11px;line-height:1.4;}
}

@media (max-width:767.98px){
  /* Dos filas accesibles: 44 + 44 + 4 de gap + 12 de padding = 104px.
   * Se conserva el buscador visible; no hay lupa nueva ni campos escondidos. */
  .site-header .hwrap{padding:6px 16px;row-gap:4px;column-gap:8px;padding-inline-start:max(16px,var(--mc-mobile-safe-left));padding-inline-end:max(16px,var(--mc-mobile-safe-right));}
  .site-header .category-bar-inner{padding-inline-start:max(8px,var(--mc-mobile-safe-left));padding-inline-end:max(8px,var(--mc-mobile-safe-right));}
  .site-header .brand img{width:28px;height:28px;}
  .site-header .brand-wordmark strong{font-size:28px;}
  .site-header .search input{height:44px;}

  /* Misma estructura: copy y fotos usan el ancho completo.
   * La X ocupa una celda superpuesta que ABARCA AMBAS FILAS: así el sticky
   * no termina al salir el copy y permanece al leer las fotos del submenú. */
  .site-header .category-mega-inner{
    display:grid;
    grid-template-columns:minmax(0,1fr) 48px;
    grid-template-rows:auto auto;
    align-items:start;
    gap:18px 8px;
    padding:16px 16px 20px;
    padding-inline-start:max(16px,var(--mc-mobile-safe-left));
    padding-inline-end:max(16px,var(--mc-mobile-safe-right));
  }
  .site-header .mega-copy{grid-column:1/-1;grid-row:1;padding-right:0;}
  .site-header .mega-copy .eyebrow,
  .site-header .mega-copy h2{padding-inline-end:56px;}
  .site-header .mega-copy h2{font-size:clamp(1.75rem,6.4vw,2rem);line-height:1.1;letter-spacing:-.5px;}
  .site-header .mega-products{grid-column:1/-1;grid-row:2;}
  .site-header .mega-close{
    position:sticky;top:8px;right:auto;
    grid-column:2;grid-row:1/-1;
    align-self:start;justify-self:end;
  }
}

/* Se mantiene la composición lateral en tablets, sin afectar al PC a 1024px. */
@media (min-width:768px) and (max-width:1024px) and (hover:none) and (pointer:coarse){
  .site-header{--mc-mobile-panel-reserve:11.5rem;}
  .site-header .hwrap{padding:10px 24px;gap:16px;padding-inline-start:max(24px,var(--mc-mobile-safe-left));padding-inline-end:max(24px,var(--mc-mobile-safe-right));}
  .site-header .category-bar-inner{padding-inline-start:max(24px,var(--mc-mobile-safe-left));padding-inline-end:max(24px,var(--mc-mobile-safe-right));}
  .site-header .brand img{width:30px;height:30px;}
  .site-header .brand-wordmark strong{font-size:32px;}
  .site-header .category-mega-inner{
    display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.5fr);
    grid-template-rows:auto;gap:24px;padding:20px 24px;
    padding-inline-start:max(24px,var(--mc-mobile-safe-left));
    padding-inline-end:max(24px,var(--mc-mobile-safe-right));
    align-items:start;
  }
  .site-header .mega-copy{grid-column:1;grid-row:1;padding-right:0;}
  .site-header .mega-copy h2{font-size:32px;}
  .site-header .mega-products{grid-column:2;grid-row:1;padding-top:56px;}
  .site-header .mega-close{
    position:sticky;top:8px;right:auto;
    grid-column:2;grid-row:1;
    align-self:start;justify-self:end;
  }
}

/* Sin nuevas animaciones para quien solicita movimiento reducido. */
@media (max-width:767.98px) and (prefers-reduced-motion:reduce),
       (min-width:768px) and (max-width:1024px) and (hover:none) and (pointer:coarse) and (prefers-reduced-motion:reduce){
  .site-header .header-icon,
  .site-header .category-control,
  .site-header .category-expand{transition:none!important;}
  .site-header .header-icon:active,
  .site-header .category-control:active,
  .site-header .category-expand:active{transform:none;}
}

```
