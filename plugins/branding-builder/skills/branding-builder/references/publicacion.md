# Publicación y entrega

`$S` = la carpeta `scripts/` de esta skill.

## Opción principal: artifact Design System

1. Lista los tipos de artifact (`list_types` o el equivalente de la herramienta de artifacts) y localiza «Design System». Si no aparece, ve a «Alternativa sin Design System».
2. Con todo el material terminado, crea el artifact UNA sola vez desde el tipo (`create_from_type` con su slug y `title` = nombre de la marca; si la herramienta ofrece `quickstart` o publica con `type_url`, es el mismo paso). El resultado trae el SKILL.md del tipo: síguelo. **En formato de archivos, el tipo manda sobre esta skill.**
3. Lee del tipo `artifact-type/reference/cover.md` (y `format.md` si hay componentes) con `describe_type` y `file`.
4. Sube cada binario de `project/assets/` (svg, png, pdf; ≤ 20 MB, SVG ≤ 2 MB) con `upload_asset`. Apunta en `blobs.json` cada ruta relativa a `assets/` con lo que devolvió la subida: `{"Logos/SIGLA-logo-negro.svg": "/_blob/<id>", …}`.
5. `publish_files` en modo `patch`, una llamada cada vez con el `base_version` de la anterior: `README.md`, `plataforma.md`, `decisiones.md`, `tokens.json`, `fonts/*` (con sus licencias) y los README de los grupos.
6. Genera el índice: `python3 $S/indice.py --project <kit>/project --blobs blobs.json --titulo "<Marca>" --autor "<nombre del usuario o Claude>" --nota "v1.0: primera versión del sistema."`. Si dice «Falta subir», sube lo que falta y repite.
7. **Última llamada:** `components/Cover/preview.html` y `design-system.json`.
8. Comprueba con `list_files` que están todas las rutas de texto esperadas.

## Revisar un sistema publicado (modo C)

- `list_files` del artifact; lee el índice, `decisiones.md` y cada archivo que vayas a cambiar justo antes de editarlo.
- Cambia solo lo pedido. `tokens.json` se envía siempre entero; los assets nuevos se suben y se añaden a `blobs.json`.
- Índice: guarda el leído (`design-system-leido.json`), vuelve a leerlo justo antes de la última llamada y genera el nuevo con `indice.py --existente design-system-leido.json --nota "v1.1: …"`: conserva título, claves y orden, y añade lo nuevo al final de cada grupo.
- `lastChange.note` lleva la versión nueva, la misma que `decisiones.md`, el README y la portada del manual.
- Si cambian fundamentos (color, tipografía, logo), regenera las piezas afectadas, los editables y el manual.
- No borres assets sin que te lo pidan. Si la publicación se rechaza porque alguien guardó entretanto, vuelve a leer, rehaz el cambio una vez y, si se rechaza otra vez, avisa y para.

## Alternativa sin Design System

Si la cuenta no tiene el tipo Design System (o la persona prefiere una página):

1. `python3 $S/libro_marca.py --project <kit>/project --salida <kit>/libro` crea un libro de marca en `index.html` con README, plataforma y decisiones, muestras de color por tema, escala tipográfica con las fuentes reales y galería de assets con descarga.
2. Publícalo como artifact hecho a mano con todos sus archivos (`publish_files` con `index.html` y las carpetas `assets/` y `fonts/`). Si no hay herramienta de artifacts, entrega el ZIP y el `libro/` comprimido.
3. Dilo en una línea: el libro no tiene el editor de un Design System, pero se puede compartir y descargar igual.

## Entrega fuera del artifact

- `python3 $S/empaquetar.py --kit <kit> --sigla <SIGLA>` → `extra/<SIGLA>-brand-kit.zip` con assets, fuentes y licencias, editables, `favicon.ico`, README, plataforma, decisiones y tokens.
- Si hay carpeta conectada, copia allí `<marca>-kit/` y el ZIP; si no, envía el ZIP como archivo.
