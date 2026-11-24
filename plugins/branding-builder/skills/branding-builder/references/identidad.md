# Identidad: fase 03

## Naming (solo si se crea o cambia el nombre)

- Genera candidatos por territorios, cada uno con su racional.
- Compara comprensión, pronunciación en los idiomas relevantes, asociaciones, diferenciación y capacidad de crecer.
- Presenta una lista corta (3–6) con razones y renuncias; incluye el nombre actual si es una alternativa real.
- Separa las comprobaciones hechas de las pendientes. Una búsqueda web puntual de dominio, redes o marcas registradas (p. ej. OEPM, EUIPO) orienta, pero no certifica disponibilidad ni derechos: dilo así y apúntalo como pendiente con `estado.py pendiente`.

**H03_N Nombre.**

## Rutas visuales (H03_V)

- **Completa:** abre 2–3 rutas desde la plataforma. Cada una con concepto, mecanismo generador (la metáfora o regla formal que produce las formas; de ahí saldrá la regla geométrica), criterio de la plataforma al que sirve, qué toma y qué evita de las referencias, y riesgos de interpretación. En modo B, si el logo se conserva, las rutas exploran el sistema que lo rodea (color, tipografía, composición) sin tocarlo.
- **Prueba de diversidad:** si al quitar nombres y colores dos rutas proponen lo mismo, son variantes de una sola; sustituye una por un mecanismo nuevo.
- **Exprés:** 2–3 variantes del símbolo dentro de un mismo concepto.
- Materializa cada opción en una **lámina comparable** con `templates/piezas/lamina-ruta.html`, mismo formato para todas: símbolo en SVG limpio, paleta, par tipográfico y una aplicación (p. ej. avatar o post). Cada lámina lleva su paleta y fuentes en su propio bloque `:root` (no usa brand.css). Renderiza con `render.py` y mírala (Read) antes de enseñarla. Ninguna más desarrollada que las otras.
- La persona elige o combina con razones. Elegir una ruta no aprueba el logo definitivo.
- **Límite honesto:** Claude diseña bien logos geométricos y tipográficos en SVG. Si quiere un logo ilustrado o muy detallado, recomienda traerlo hecho (o pasar al modo B cuando lo tenga) y construir el resto del kit alrededor. Una imagen generada no es un logo vectorial.

## Logo y geometría

- **Modo A:** desarrolla la ruta elegida en SVG a mano (paths limpios, una tinta, viewBox entero).
- **Modo B:** vectoriza con vtracer o potrace si están (si no, redibuja a mano solo si el logo es geométrico y sencillo), superpón el resultado al original, compáralos y avisa de cualquier diferencia. Nunca «mejores» ni aproximes un logo existente sin permiso.
- El archivo maestro es `SIGLA-logo-<tinta principal>.svg`; anota en el README el tamaño de su lienzo en unidades.
- Extrae la **regla geométrica** del logo (un ángulo, un radio, un módulo de grosor) y conviértela en token (p. ej. `angle-cut` para un ángulo, `radius-mark` para un radio o `stroke-unit` para un grosor). Esa regla alimenta patrón, separadores, portada e iconos.
- **Zona de respeto:** X = una medida del propio logo (grosor del trazo principal, altura de una letra); exprésala también en % del ancho.
- **Tamaño mínimo:** en px de alto (pantalla) y mm (impresión); por debajo, favicon.
- **Hoja de construcción** en SVG: retícula, cotas de X, ángulos.
- **Versiones de color:** como mínimo positivo y negativo; añade la variante sobre cada fondo de marca, con su caso de uso.
- **Usos prohibidos:** deformar, girar, recolorear fuera de paleta, sombras/efectos, poco contraste, fondos con ruido, separar piezas, contorno.
- **Lockups:** horizontal (símbolo + separador con la regla geométrica + nombre + eslogan) y vertical. Entrégalos en PNG. Si además quieres SVG, convierte el texto a trazados con `fuentes.py texto-svg` (sin kerning GPOS: revísalo a ojo); nunca SVG con texto vivo.

## Color

- 6–10 colores de marca con nombre propio evocador y HEX, asignados por función.
- Tokens semánticos para los dos temas: `bg`, `surface`, `ink`, `ink-muted`, `border`, `action`, `on-action` (y acentos si los hay). Cada tema con nombre propio; el principal va primero.
- Proporción de uso orientativa (p. ej. 60/30/10).
- **Comprueba el contraste con `contraste.py --tokens`**, nunca a ojo: texto ≥ 4,5:1 (≥ 3:1 a 24 px+), bordes de control e iconos ≥ 3:1, en AMBOS temas. Colores que deban distinguirse, diferentes en luminosidad, no solo en tono. Apunta las cifras en el README y en las notas de uso.
- Si una combinación del usuario no pasa, consérvala pero márcala en su nota de uso y propón alternativa.
- **Impresión** (si está en el alcance): no hay una conversión a CMYK universal. Da valores CMYK de partida marcados como «pendiente de prueba con la imprenta» y apúntalo como pendiente; Pantone solo si el usuario lo aporta.

## Tipografía

- Tres roles: `display` (titulares), `sans` (texto), `mono` o secundaria (etiquetas y datos). Prioriza fuentes libres (SIL OFL, Google Fonts). Distingue el lettering del logo de las fuentes del sistema.
- Archivos reales: `@fontsource/*` por npm si hay red; si no, `fuentes.py buscar` y `fuentes.py convertir` con las instaladas (fija el peso de las variables, hace el subconjunto latino y copia la licencia). Si no está instalada, pide los archivos o propone una equivalente instalada.
- Tres grupos de estilos: **Titulares** (`display-xl`, `display-l`, `heading-1`, `heading-2`), **Texto** (`body-l`, `body`, `small`) y **Etiquetas** (`label`), cada estilo con tamaño, interlineado, peso, tracking, texto de muestra y uso. Para etiquetas en mayúsculas puedes añadir `"textTransform": "uppercase"`.
- Reglas propias (tamaño mínimo en pantalla, mayúsculas en etiquetas, etc.).
- **Licencias:** sube a `fonts/` solo fuentes cuya licencia permita incluirlas, con su archivo de licencia. Si la marca usa una fuente comercial, no incluyas sus archivos: el README dice dónde se licencia y queda como pendiente.

## Tokens de interfaz y elementos gráficos

- Espaciado: escala de 4 px (`space-1`, `2`, `4`, `6`, `12`, `24`) con el uso de cada uno, incluido el margen de seguridad de posts.
- Radios: `radius-sm`, `radius-md`, `radius-pill` (o rectos si la geometría lo pide).
- Patrón derivado de la regla geométrica del logo, sin costuras, en versión oscura y clara; regla de uso (en qué zona de la pieza, nunca detrás del logo ni de texto pequeño).
- Estilo de iconos: grosor, esquinas, color (token). Principios de imagen o ilustración solo si la marca los necesita.
- Evita los tópicos de IA: degradados azul-morado, tarjetas con emoji, tarjetas con borde izquierdo de color.

## Forma de `tokens.json`

- Cada familia es una LISTA: `{"tokens":[{"name","value","usage"}]}`. Nunca el formato DTCG con mapas (`$value`): el Design System no lo lee.
- `color` lleva además `themes` (`[{"id":"light","name":"<tema claro>"},{"id":"dark","name":"<tema oscuro>"}]`, el principal primero). Los tokens semánticos llevan valor por tema (`{"light":"#…","dark":"#…"}`); los colores de marca, un HEX simple.
- `type` lleva `fonts` (un registro por archivo y peso: `{"family","file","weight"}`), `families` (`display`, `sans`, `mono`) y `groups` (los tres de arriba).
- La regla geométrica va en una familia propia (`angle`, `module`…) con la misma forma de lista.
- Nombres únicos `[A-Za-z0-9][A-Za-z0-9_.-]`; sin colores con nombre, `var()` ni `color-mix()`. Una nota de uso en cada token.

```json
{"name": "Acme", "version": 1,
 "color": {"themes": [{"id": "light", "name": "<Claro>"}, {"id": "dark", "name": "<Oscuro>"}],
  "tokens": [{"name": "bg", "value": {"light": "#…", "dark": "#…"}, "usage": "Fondo de página."},
             {"name": "<color-de-marca>", "value": "#…", "usage": "…"}]},
 "type": {"fonts": [{"family": "<Fuente>", "file": "fonts/<fuente>-latin-700-normal.woff2", "weight": "700"}],
  "families": {"display": "\"<Fuente>\", system-ui, sans-serif", "sans": "…", "mono": "…"},
  "groups": [{"name": "Titulares", "family": "display", "styles": [{"name": "display-xl", "fontSize": "96px", "lineHeight": 0.95, "fontWeight": 700, "letterSpacing": "-0.03em", "sample": "…", "usage": "…"}]}]},
 "spacing": {"tokens": [{"name": "space-4", "value": "16px", "usage": "…"}]},
 "radius": {"tokens": [{"name": "radius-md", "value": "12px", "usage": "…"}]},
 "angle": {"tokens": [{"name": "angle-cut", "value": "54deg", "usage": "…"}]}}
```

## Sistema aplicado (H03_S)

Antes de producir todo, enseña: el logo final con sus versiones de color y lockups, la paleta y la tipografía aplicadas, y **3 piezas de muestra** que pongan a prueba restricciones distintas: una pequeña (avatar o favicon), una densa con texto realista (post o membrete) y una de formato extremo (story o banner). Si hay banners en el alcance, la de formato extremo es un banner (el más extremo de la lista: LinkedIn página a 6:1 o YouTube) y se enseña con `banners.py simular`, que dibuja lo que tapa la foto de perfil y lo que recorta el móvil; con él se aprueba la regla de composición común a todos los banners. Renderízalas con las plantillas y `?guias=1` para revisar las zonas seguras (y otra vez sin guías para enseñarlas). En Completa, confirma aquí la `SIGLA`, los nombres de los temas, los fondos y la lista de archivos. La persona aprueba o pide cambios; solo entonces se produce el resto.
