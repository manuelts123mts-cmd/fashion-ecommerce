# M&C · Complemento de header móvil

Primera sección aprobada de la optimización móvil. No se han ejecutado hero/PLP/PDP/footer de esta revisión.

## Ver el resultado
- `tienda_portable.html`: tienda actualizada, entregada por separado. En PC se ve igual por diseño.
- `COMPARATIVA_HEADER_MOVIL.html`: capturas reales antes/después, autocontenidas; entregada por separado para no duplicar fotos en el ZIP.
- `HEADER_MOVIL.md`: código CSS completo, integración, alcance, pruebas y límites.

## Aplicar las fuentes
Este ZIP es un complemento al proyecto actual. Extraer sobre una COPIA del mismo proyecto, conservando las fuentes previas, assets e inventario. El archivo nuevo es `src/styles/mobile-header.css`; el generador lo carga al final, dentro de media queries móviles. El script de pruebas se añade en `package.json`.

```bash
python3 build_portables.py
python3 build_admin.py
python3 scripts/export_static.py
```

No se necesita procesar fotos ni instalar librerías de frontend. Para publicar se recomienda `site/`; no publicar el editor/admin de desarrollo sin protegerlo.

## Probar
```bash
npm install
npx playwright install --with-deps chromium
# En otra terminal: python3 server.py
npm run test:mobile-header
node audits/mobile-header/verify-extras.cjs
```

También siguen disponibles `test:header`, `test:home`, `test:static` y `test:hero`.

Las comparaciones desktop de 15 vistas fueron idénticas. Las pruebas móviles son emulación Chromium, no hardware Safari/iOS. El LCP del perfil lento sigue por encima de 2.5s y no se promete una garantía universal. Más detalles en la guía.

No cambia la estructura HTML ni el JS del sitio. La X que permanece visible en esta etapa es la del SUBMENÚ de categorías, no la de la ficha PDP.
