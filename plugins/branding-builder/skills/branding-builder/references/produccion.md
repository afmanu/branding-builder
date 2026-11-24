# Producción de activos (fase 04)

En los comandos, `$S` = la carpeta `scripts/` de esta skill y `$T` = `templates/piezas/`. Ejecuta los scripts con `python3` (en Windows, `python`).

## Carpeta de trabajo

```
<marca>-kit/
  expediente/  project-state.json, alcance, diagnóstico, plataforma, rutas y láminas (también lo descartado)
  project/
    README.md  plataforma.md  decisiones.md  tokens.json  design-system.json
    fonts/
    components/Cover/preview.html  components/<Comp>/  components/bundle.css
    assets/Logos/  Iconos/  Redes/  [Banners/]  Patrones/  Mockups/  Manual/  Papeleria/  Presentaciones/  OnePager/
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
7. **Banners de perfil** (solo si hay redes; uno por perfil acordado en H00; detalle en «Banners» más abajo):
   ```bash
   cp $T/banner.html $T/banners-formatos.js editables/      # adapta banner.html a la marca, no toques el catálogo
   python3 $S/banners.py lote --redes youtube,x,linkedin-perfil --plantilla editables/banner.html \
       --dir project/assets/Banners --guias extra/banners-guias --salida extra/lote-banners.json
   python3 $S/render.py lote extra/lote-banners.json
   python3 $S/banners.py comprobar project/assets/Banners --redes youtube,x,linkedin-perfil
   python3 $S/banners.py simular project/assets/Banners --avatar project/assets/Redes/avatar-<fondo>_1000.png \
       --salida expediente/banners-simulacion.png
   ```
   Mira la simulación (Read) antes de darlos por buenos.
8. **Iconos:** renderiza `app-icon-1024.html` cuadrado a sangre por fondo (`--param tema=<id>`, con el logo de la tinta que contraste), luego `python3 $S/iconos.py esquinas <cuadrado> project/assets/Iconos/SIGLA-app-icon-<fondo>_1024.png` y `python3 $S/iconos.py derivar <cuadrado> --dir project/assets/Iconos --ico extra/favicon.ico`. El SVG del icono (`SIGLA-app-icon-<fondo>.svg`) y `favicon.svg` se escriben a mano.
9. **Mockups:** `mockups.html` con `?escena=tarjetas|pegatinas|movil`, usando los renders de la tarjeta y de las piezas como imágenes.
10. **Manual PDF:** copia `manual.html`, duplica los tipos de página que necesites con el mismo contenido que el README y `python3 $S/render.py pdf editables/manual.html project/assets/Manual/SIGLA-Manual-de-Marca.pdf`. Revisa las páginas (p. ej. `pdftoppm -r 30 -png` si está, o la vista previa del PDF).
11. **Papelería** (base): `membrete-a4.html` → PDF con `render.py pdf`; `firma-email.html` con colores en HEX y estilos en línea (los clientes de correo no leen variables CSS ni fuentes web), logo en PNG alojado en una URL pública.
12. **Presentación** (base): portada, separador y diapositiva de contenido 16:9 a 1920×1080, en PNG y en un PDF con todas.
13. **One pager** (base): copia `one-pager-a4.html`, rellena los textos desde la plataforma (titular, qué hace, cómo trabaja, para quién, qué se lleva el cliente, llamada a la acción) y `python3 $S/render.py pdf editables/one-pager-a4.html project/assets/OnePager/SIGLA-one-pager-A4.pdf`; la vista previa con `render.py png ... SIGLA-one-pager-A4_preview.png` a 1240×1754. Si no hay datos de contacto reales, márcalos como ejemplo en el README del grupo.
14. **Fondos 1920×1080** (base): al menos uno claro y uno oscuro, con el patrón o el motivo del logo en una zona y espacio limpio para texto o vídeo, en `Patrones/SIGLA-fondo-<nombre>-<fondo>_1920x1080.png`.
15. **Componentes UI** (base): botón, etiqueta, tarjeta y campo en `components/<Comp>/` con `preview.html` y `README.md`, y `components/bundle.css` generado desde los tokens.

## Reglas

- Tamaño exacto en px, `deviceScaleFactor: 1` (lo aplica `render.py`).
- **Revisa visualmente** cada tipo de pieza (Read sobre el PNG) a su tamaño de uso antes de darla por buena: textos cortados, márgenes, jerarquía, contraste, reconocimiento al reducir. Hacer una hoja de contactos con Pillow ahorra lecturas.
- Piezas de redes: márgenes de seguridad de 80 px en 1080, etiqueta mono arriba a la izquierda, contenido realista y textos de ejemplo marcados como tales en el README del grupo.
- Logo sobre fondo oscuro: usa la tinta clara. Un logo de la misma tinta que el fondo desaparece; compruébalo en cada render.
- Mockups: escenas sencillas y limpias; datos de ejemplo si el usuario no dio los suyos. Un mockup enseña una aplicación; no demuestra eficacia.
- Tarjeta de visita: 90×54 mm = 1063×638 px a 300 ppp, margen de 5 mm. Para imprenta, confirma sangrado y formato con la imprenta.
- **Manual PDF:** portada (con versión, p. ej. v1.0), índice, la marca (plataforma resumida), concepto del símbolo, logo y construcción, zona de respeto y tamaño mínimo, versiones de color, usos prohibidos, lockups, color, tipografía, voz, elementos gráficos, aplicaciones (redes y, si los hay, una página con los banners apilados), módulos de empresa si los hay, mantenimiento y descargas. 12–18 páginas, 16:9, el mismo contenido que el README.
- Guarda en `editables/` el HTML final de cada pieza: entra en el ZIP para que se puedan cambiar textos sin rehacer nada.

## Banners de perfil

El catálogo (`$T/banners-formatos.js`, revisado en noviembre de 2026) guarda por red el lienzo, la zona segura, lo que tapa la interfaz (foto de perfil, logo de la página, menús), lo que recortan los móviles, el peso máximo, la fuente y su fiabilidad. `banner.html` y `banners.py` leen ese mismo archivo: si una red cambia sus medidas, se corrige ahí y nada más.

- **Uno por perfil, no por red.** LinkedIn tiene perfil personal (`linkedin-perfil`, 1584×396) y página de empresa (`linkedin-pagina`, 1512×256); Facebook, página (`facebook`) y grupo (`facebook-grupo`). Produce solo los de los perfiles que existan o se vayan a abrir.
- **Fiabilidad `verificar`** (Skool, Whop, Twitch, Discord, Pinterest, grupo de Facebook): las fuentes se contradicen o la plataforma no publica la medida. Antes de producir, pide a la persona el tamaño que muestra la pantalla de subida (o míralo en el navegador si tienes acceso a su cuenta) y pásalo con `--tamano whop=3000x640`. Si no se puede comprobar, produce con la medida del catálogo y anótalo con `estado.py pendiente`.
- **Una familia, no N diseños.** Fija una regla de composición en el sistema aplicado (dónde va el contenido, qué llena el resto del lienzo, qué motivo lo acompaña) y aplícala a todos: lo que cambia entre redes es la proporción, no la idea.
- **Contenido:** lockup o nombre, una sola frase (eslogan, descriptor o promesa) y como mucho un dato estable (web, usuario o frecuencia). Nada que caduque (fechas, «este jueves», precios): un banner dura meses.
- **Fuera de lo tapado.** La foto de perfil ya enseña el símbolo: no lo repitas debajo de ella. La plantilla estrecha la zona de contenido para esquivar lo tapado y quita el dato en formatos muy bajos (LinkedIn página).
- **El fondo llena todo el lienzo** (lo recortado se ve en algún dispositivo: el banner de YouTube entero en TV); el motivo va en la franja libre, nunca detrás del texto.
- **Texto legible a su tamaño real:** un banner de 1500 px se ve a 600 en el perfil de X. Ningún texto por debajo de ~3 % del alto del lienzo; en Discord, casi nada de texto.
- **Peso:** Bluesky admite 1 MB como máximo; Facebook carga mejor por debajo de 100 KB en JPG. `banners.py comprobar` lo vigila.
- La imagen OG (1200×630) usa la misma plantilla (`?f=og`) pero va en el grupo Redes.
