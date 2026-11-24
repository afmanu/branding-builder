# El plano: qué hay al final

Todo el proceso trabaja hacia este resultado. No cambies la estructura salvo que el usuario lo pida; quita solo las piezas de canales que no use. Si en H00 dijo que no necesita elementos para redes sociales, no hay grupos Redes ni Banners (si tiene web, la imagen OG va en Iconos).

## Archivos de texto (en `project/`)

| Ruta | Qué es |
|---|---|
| `README.md` | El manual de marca navegable (estructura fija abajo; esqueleto en `templates/textos/README-marca.md`) |
| `plataforma.md` | Solo en profundidad Completa: la plataforma con su racional y el resumen del diagnóstico con fuentes |
| `decisiones.md` | Registro de decisiones y versiones, pendientes y mantenimiento. Se genera con `estado.py md` |
| `tokens.json` | Color en dos temas + colores de marca, tipografía, spacing, radius y la regla geométrica del logo |
| `fonts/*.woff2` | Las fuentes reales (o `.woff`) y su archivo de licencia |
| `assets/<Grupo>/README.md` | Uno por grupo: qué hay, variantes y qué es de ejemplo |
| `components/Cover/preview.html` | La portada del sistema (plantilla `portada-ds.html`) |
| `design-system.json` | El índice: grupos, orden y registro de cada asset. Lo genera `indice.py` y se escribe el último |

## Assets subidos (hasta 8 grupos base, en este orden)

`SIGLA` = abreviatura de la marca (p. ej. `ACME` para «Acme Estudio»). `<tinta>` = color del logo (negro, blanco…); `<fondo>` = cada fondo de marca.

| Grupo | Tesela | Archivos |
|---|---|---|
| Logos | `l` | `SIGLA-logo-<tinta>.svg` (una tinta, sin fondo) y su `SIGLA-logo-<tinta>_4000px.png` transparente, por cada tinta · `SIGLA-logo-<tinta>-sobre-<fondo>.svg` (con fondo y zona de respeto) por cada versión de color · `SIGLA-construccion.svg` · `SIGLA-lockup-horizontal-sobre-<fondo>.png`, `SIGLA-lockup-horizontal-<tinta>.png`, `SIGLA-lockup-vertical-<tinta>.png` |
| Iconos | `m` | `SIGLA-app-icon-<fondo>.svg` y `SIGLA-app-icon-<fondo>_1024.png` por fondo (esquinas al 22,37%) · `favicon.svg` · `apple-touch-icon.png` (180 px) · `android-chrome-512x512.png` |
| Redes | `l` | Solo si hay redes sociales (pregunta de H00). `avatar-<fondo>_1000.png` por fondo · `OG-web-compartir_1200x630.png` · `Instagram-post-<formato>_1080x1080.png` por formato recurrente · `Instagram-story_1080x1920.png` · `YouTube-miniatura-<tipo>_1280x720.png` si hay vídeo |
| Banners | `l` | Un banner por cada perfil acordado en H00, con el nombre y el tamaño del catálogo (`banners.py lista`): `YouTube-banner_2560x1440.png` · `X-cabecera_1500x500.png` · `LinkedIn-perfil_1584x396.png` · `LinkedIn-pagina_1512x256.png` · `Facebook-portada_1702x630.png` · `Bluesky-banner_3000x1000.png` · `Twitch-banner_1200x480.png` · `Discord-banner_1920x1080.png` · `Skool-portada_<W>x<H>.png` · `Whop-banner_<W>x<H>.png` · `Pinterest-portada_1920x1080.png` · `Newsletter-cabecera_1200x400.png`. Sin perfiles con banner, el grupo no existe |
| Patrones | `m` | `SIGLA-patron-<nombre>-<fondo>.svg` sin costuras, en oscuro y claro · `SIGLA-patron-<nombre>-<fondo>_2048.png` · `SIGLA-patron-logos-<fondo>_1920.png` |
| Mockups | `l` | `mockup-tarjetas_1600x1200.png` · `mockup-pegatinas_1600x1200.png` · `mockup-perfil-<red>-movil_1200x1600.png` · `tarjeta-visita-anverso_90x54mm.png` y `tarjeta-visita-reverso_90x54mm.png` (1063×638 px) |
| Manual | `s` | `SIGLA-Manual-de-Marca.pdf` (12–18 páginas, 16:9) |
| OnePager | `s` | Siempre, en toda marca. `SIGLA-one-pager-A4.pdf` (A4 vertical, una cara, desde `one-pager.html`) · `SIGLA-one-pager-A4_794x1123.png` como vista previa |

Los nombres con el tamaño al final (`_1080x1080`, `_1000`, `_4000px`) permiten que `render.py` sepa a qué tamaño renderizar y que `indice.py` los ordene. En los banners, además, `banners.py comprobar` reconoce la red por el nombre y comprueba tamaño, proporción y peso.

## Módulos de empresa (opcionales, según el alcance)

| Módulo | Dónde va | Contenido |
|---|---|---|
| Papelería | Grupo `Papeleria` (tesela `m`), tras Mockups | Membrete A4 en PDF (`membrete-a4.html`); firma de email en PNG (`firma-email.html`), con su HTML en un bloque de código dentro del README del grupo; plantilla de factura o presupuesto en PDF si la pide |
| Presentaciones | Grupo `Presentaciones` (tesela `l`) | Portada, separador y diapositiva de contenido 16:9 en PNG, más la plantilla en PDF. Si quiere una plantilla editable, ofrece aparte un artifact de Slides |
| Componentes UI | `components/<Comp>/README.md` + `preview.html` | Botón, etiqueta, tarjeta y campo de formulario hechos con los tokens; previews estáticos en HTML/CSS. Lee antes `format.md` del tipo Design System |

## Fuera del artifact

El almacén de assets no acepta `.ico`, `.zip` ni HTML. Se entrega aparte (carpeta conectada o archivo enviado) el ZIP de `empaquetar.py`, con `favicon.ico`, todos los assets, las fuentes y sus licencias, y la carpeta `editables/` (el HTML o SVG fuente de cada pieza y su `brand.css`) para cambiar textos sin rehacer nada. Los README de Iconos y Redes lo indican. Las piezas de redes son ejemplos en PNG: no las llames plantillas editables; los editables están en el ZIP.

## README (estructura fija)

1. `# <Marca>`, el eslogan en negrita y un párrafo sobre qué es; después, una línea que remite a **Assets → Logos** y **Assets → Manual**.
2. `## La marca`: público, promesa, personalidad, idea de marca y los criterios que justifican la identidad, en una síntesis que se entienda sin leer la investigación.
3. `## El símbolo`: concepto y de qué criterio sale, regla geométrica con su valor, archivo maestro y lienzo, zona de respeto, tamaño mínimo y hoja de construcción. Dentro: `### Versiones de color` (tabla Versión | Fondo | Cuándo), una línea **Evitar:** y `### Lockups`.
4. `## Descargar y usar`: para quien no diseña. SVG para web y diseño; PNG de 4000 px para Canva, Word o redes; dónde están el avatar, los iconos, las piezas, los editables (ZIP) y el manual; dónde se consiguen las fuentes.
5. `## Color`: enfoque y proporción; tabla Token | Hex | Uso de los colores de marca; tokens semánticos y temas; cifras de `contraste.py`; valores de impresión si los hay.
6. `## Tipografía`: los tres roles con sus reglas, licencia y dónde están los archivos.
7. `## Voz y contenido`: con ejemplos y contraejemplos.
8. `## Elementos gráficos`: patrón y su regla de uso; estilo de iconos.
9. `## Piezas incluidas`: lista con tamaños, margen de seguridad, uso de botones y dónde están sus editables.
10. `## Banners de perfil` (si hay grupo Banners): tabla Red | Archivo | Tamaño | Qué evitar (lo que tapa la interfaz y lo que recorta el móvil), la regla de composición común y qué medidas quedan por verificar en la plataforma.
11. `## One pager`: qué cuenta (titular, resumen, cómo trabajamos, para quién, qué te llevas, llamada a la acción), qué datos son de ejemplo y dónde está su editable.
12. Una sección por módulo de empresa, si los hay.

## README de cada grupo

1–3 frases: qué contiene, qué variantes hay, qué textos o datos son de ejemplo y qué queda fuera del artifact. Ejemplos de forma (no de contenido):

- Logos: «Símbolo y lockups. Los SVG sin fondo son de una tinta; los `-sobre-` incluyen fondo y zona de respeto. PNG transparentes de 4000 px para usar fuera de herramientas de diseño. `SIGLA-construccion.svg` es la hoja de construcción.»
- Iconos: «Icono de app por fondo (esquinas al 22,37%) en SVG y PNG de 1024 px; `favicon.svg`, `apple-touch-icon.png` y `android-chrome-512x512.png`. El `favicon.ico` está en el ZIP del kit.»
- Redes: «Avatares y piezas listas para publicar. Los textos son de ejemplo; los editables están en el ZIP. Mantén los márgenes de 80 px y la etiqueta arriba a la izquierda.»
- OnePager: «Presentación de la marca en una página A4, en PDF para enviar o imprimir y en PNG como vista previa. El contacto es de ejemplo. Editable: `editables/one-pager.html` en el ZIP.»
- Banners: «Un banner por perfil, al tamaño exacto de cada red. La esquina inferior izquierda queda libre porque ahí cae la foto de perfil. Para cambiar el texto, `editables/banner.html?f=<red>`. Las medidas de Skool y Whop están por verificar en su pantalla de subida.»

## Portada

`components/Cover/preview.html` sale de `templates/piezas/portada-ds.html`: línea 1 `<!-- @dsCard height=300 -->`, 960×300, solo variables de los tokens. Bloques a la derecha cuyo motivo sale de la regla geométrica del logo; nombre y eslogan abajo a la izquierda. Lee `cover.md` del tipo Design System antes de componerla.
