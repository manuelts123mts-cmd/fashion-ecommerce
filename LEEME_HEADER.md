# M&C — complemento de header sticky

## Abrir ahora (sin instalación)
- `demo_header_sticky.html`: demo offline con las 73 prendas existentes y nueva navegación.
- `demo_header_mock.html`: 20 prendas ficticias en 5 categorías de prueba; no representa stock, WhatsApp deshabilitado.
- `HEADER_STICKY.md`: explicación, integración, pruebas y código completo comentado del componente.

## Fuente e integración
Este ZIP contiene el componente completo y los archivos de integración actualizados. Es un **complemento al proyecto de Fase 1 ya entregado**, no una copia adicional de todas sus fotografías ni de sus datos privados. Conserva intacto `M_C_Premium_Fase_1.zip`.

Para reconstruir desde código, extraer sobre una COPIA del proyecto anterior, conservando `uploads/`, `web/assets/`, `web/img/` y `web/data/productos.json`. Los HTML demo incluidos ya son autocontenidos y no necesitan esa copia para abrirse.

```bash
python3 build_portables.py
python3 build_admin.py
python3 scripts/export_static.py
python3 scripts/build_header_demo.py
python3 scripts/build_header_demo.py --mock
```

`site/` es la salida pública recomendada. El servidor/editor previo no tiene autenticación de producción: no publicar el directorio de desarrollo ni el admin sin protegerlo. La mejora no habilita pagos, carrito, checkout ni cuentas de cliente. No hay importes públicos.

## Repetir las pruebas
```bash
npm install
npx playwright install --with-deps chromium
# Otra terminal: python3 server.py
npm run test:header
npm run test:home
npm run test:static
```

Los resultados incluidos corresponden a Chromium. Header: 320/768/1024/1440 px; regresión Homepage: también 390 px. Se validó offline y movimiento reducido. No se presenta la auditoría automática como una certificación completa de WCAG ni se afirma validación en dispositivos físicos Safari/iOS.
