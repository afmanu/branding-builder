# Producción de activos (fase 04)

En los comandos, `$S` = la carpeta `scripts/` de esta skill y `$T` = `templates/piezas/`. Ejecuta los scripts con `python3` (en Windows, `python`).

## Carpeta de trabajo

```
<marca>-kit/
  expediente/  project-state.json, alcance, diagnóstico, plataforma, rutas y láminas (también lo descartado)
  project/
    README.md  plataforma.md  decisiones.md  tokens.json  design-system.json
    fonts/
    components/Cover/preview.html
    assets/Logos/  Iconos/  Redes/  Patrones/  Mockups/  Manual/  [Papeleria/  Presentaciones/]
  editables/   copias de las plantillas, brand.css, logo.svg, patron.svg y el HTML/SVG de cada pieza
  extra/       favicon.ico, <SIGLA>-brand-kit.zip, renders auxiliares
```

## Secuencia

1. **Fuentes:** `@fontsource/*` por npm si hay red (copia los woff2 latinos a `project/fonts/`); si no, `python3 $S/fuentes.py buscar "<Familia>"` y `python3 $S/fuentes.py convertir <archivo> --familia "<Familia>" --peso <n> --salida project/fonts`. Pega la entrada `token` que imprime en `type.fonts`.
2. **tokens.json** completo (forma en `identidad.md`) y `python3 $S/contraste.py --tokens project/tokens.json` hasta que no falle nada obligatorio.
3. **brand.css:** `python3 $S/tokens_css.py project/tokens.json editables/brand.css`. Las plantillas lo cargan: usan `var(--bg)`, `var(--ink)`, `var(--font-display)`… con los mismos nombres que el Design System.
4. **Logos:** escribe los SVG a mano en `project/assets/Logos/`. PNG de 4000 px transparente: `python3 $S/render.py png <logo>.svg <logo>_4000px.png --transparente`.
5. **Piezas:** copia de `$T` a `editables/` las plantillas que toquen, copia al lado el logo de la tinta adecuada como `logo.svg` (y `logo-negativo.svg`) y el patrón como `patron.svg`, y adapta textos y composición a la marca. Las plantillas son de estructura (zonas seguras, retícula, márgenes), no de estilo: cambia lo que haga falta para que la pieza sea de esta marca.
6. **Renderizar:** `python3 $S/render.py png editables/<pieza>.html project/assets/Redes/<nombre>_<W>x<H>.png [--param tema=<id>] [--param f=youtube]`. Para muchas piezas, `render.py lote manifiesto.json`. Revisa primero con `--param guias=1` (zonas seguras visibles) y renderiza la versión final sin guías.
7. **Iconos:** renderiza `app-icon-1024.html` cuadrado a sangre por fondo (`--param tema=<id>`, con el logo de la tinta que contraste), luego `python3 $S/iconos.py esquinas <cuadrado> project/assets/Iconos/SIGLA-app-icon-<fondo>_1024.png` y `python3 $S/iconos.py derivar <cuadrado> --dir project/assets/Iconos --ico extra/favicon.ico`. El SVG del icono (`SIGLA-app-icon-<fondo>.svg`) y `favicon.svg` se escriben a mano.
8. **Mockups:** `mockups.html` con `?escena=tarjetas|pegatinas|movil`, usando los renders de la tarjeta y de las piezas como imágenes.
9. **Manual PDF:** copia `manual.html`, duplica los tipos de página que necesites con el mismo contenido que el README y `python3 $S/render.py pdf editables/manual.html project/assets/Manual/SIGLA-Manual-de-Marca.pdf`. Revisa las páginas (p. ej. `pdftoppm -r 30 -png` si está, o la vista previa del PDF).
10. **Papelería:** `membrete-a4.html` → PDF con `render.py pdf`; `firma-email.html` con colores en HEX y estilos en línea (los clientes de correo no leen variables CSS ni fuentes web), logo en PNG alojado en una URL pública.

## Reglas

- Tamaño exacto en px, `deviceScaleFactor: 1` (lo aplica `render.py`).
- **Revisa visualmente** cada tipo de pieza (Read sobre el PNG) a su tamaño de uso antes de darla por buena: textos cortados, márgenes, jerarquía, contraste, reconocimiento al reducir. Hacer una hoja de contactos con Pillow ahorra lecturas.
- Piezas de redes: márgenes de seguridad de 80 px en 1080, etiqueta mono arriba a la izquierda, contenido realista y textos de ejemplo marcados como tales en el README del grupo.
- Logo sobre fondo oscuro: usa la tinta clara. Un logo de la misma tinta que el fondo desaparece; compruébalo en cada render.
- Mockups: escenas sencillas y limpias; datos de ejemplo si el usuario no dio los suyos. Un mockup enseña una aplicación; no demuestra eficacia.
- Tarjeta de visita: 90×54 mm = 1063×638 px a 300 ppp, margen de 5 mm. Para imprenta, confirma sangrado y formato con la imprenta.
- **Manual PDF:** portada (con versión, p. ej. v1.0), índice, la marca (plataforma resumida), concepto del símbolo, logo y construcción, zona de respeto y tamaño mínimo, versiones de color, usos prohibidos, lockups, color, tipografía, voz, elementos gráficos, aplicaciones, módulos de empresa si los hay, mantenimiento y descargas. 12–18 páginas, 16:9, el mismo contenido que el README.
- Guarda en `editables/` el HTML final de cada pieza: entra en el ZIP para que se puedan cambiar textos sin rehacer nada.
