# <Marca>

**<Eslogan>.** <Un párrafo: qué es la marca, para quién y qué hace.>

Logo, lockups y construcción en **Assets → Logos**; manual completo en **Assets → Manual**.

## La marca

<Síntesis de la plataforma que se entienda sin leer la investigación: público prioritario, promesa (necesidad + diferencia + razón para creer), personalidad en 3–5 rasgos, idea de marca y los criterios que justifican la identidad.>

## El símbolo

<Concepto: qué representa y de qué criterio de la plataforma sale. Regla geométrica con su valor (`<token>`).>

- **Archivo maestro:** `assets/Logos/<SIGLA>-logo-<tinta>.svg` (lienzo <ancho> × <alto> unidades). Edita siempre desde los SVG.
- **Zona de respeto:** X = <medida del logo> (≈ <n>% del ancho del logo) en los cuatro lados.
- **Tamaño mínimo:** <n> px de alto en pantalla · <n> mm impreso. Por debajo, usa el favicon (`assets/Iconos/favicon.svg`).

Hoja de construcción: `assets/Logos/<SIGLA>-construccion.svg`.

### Versiones de color

| Versión | Fondo | Cuándo |
|---|---|---|
| <tinta> sobre <fondo> | `<token>` | <uso> |

**Evitar:** deformar, girar, añadir colores, sombras o efectos, poco contraste, fondos con ruido, separar las piezas, usar en contorno.

### Lockups

<Horizontal (símbolo + separador + nombre + eslogan) para cabeceras y web; vertical para piezas cuadradas.>

## Descargar y usar

Todo se descarga desde **Assets**: abre el grupo y descarga el archivo que necesites.

- **Logo para web, apps y diseño:** los SVG de `Logos/`. Para Canva, Word o redes, los PNG transparentes de 4000 px.
- **Foto de perfil:** `Redes/avatar-*.png`.
- **Icono de app y favicon:** `Iconos/`. El `favicon.ico` está en el ZIP del kit.
- **Piezas de redes:** `Redes/`, al tamaño exacto de cada plataforma. Sus editables (HTML/SVG) están en el ZIP, carpeta `editables/`.
- **Banners de perfil:** `Banners/`, uno por perfil (<redes>), listos para subir. Para cambiar el texto, `editables/banner.html?f=<red>` en el ZIP.
- **Manual completo:** `Manual/<SIGLA>-Manual-de-Marca.pdf`.
- **Colores y tipografías:** en **Colors** y **Typography**. Las fuentes <nombres> <dónde se consiguen y su licencia>.

## Color

<Enfoque y proporción orientativa.>

| Token | Hex | Uso |
|---|---|---|
| `<nombre>` | #<hex> | <uso> |

Para interfaces usa los tokens semánticos (`bg`, `surface`, `ink`, `ink-muted`, `border`, `action`, `on-action`), que cambian entre el tema **<claro>** y el tema **<oscuro>**. Contraste: <cifras de contraste.py en ambos temas>.

## Tipografía

- **<Fuente display>** (`display`) — <uso y reglas>.
- **<Fuente sans>** (`sans`) — <uso; tamaño mínimo en pantalla>.
- **<Fuente mono>** (`mono`) — <uso; mayúsculas y tracking en etiquetas>.

<Licencia de cada fuente y dónde están los archivos.>

## Voz y contenido

- <Tono, tratamiento y longitud de frase.>
- <Frases que la marca diría (propuesta) y frases que no, con el porqué.>
- Etiquetas con formato fijo: `<CATEGORÍA> · #01`.
- <Palabras prohibidas y política de emojis.>

## Elementos gráficos

<Patrón: de qué regla sale, dónde se usa y dónde nunca. Estilo de iconos: grosor, esquinas, color.>

## Piezas incluidas

- **Redes** (`assets/Redes/`): <lista con tamaños>. Los textos son de ejemplo.
- **Mockups** (`assets/Mockups/`): <lista>. Datos de ejemplo.
- **Manual** (`assets/Manual/`): PDF de <n> páginas.

Margen de seguridad en posts: 80 px en lienzo de 1080. Botones en `action` con texto en `on-action`.

## Banners de perfil

<Regla de composición común: dónde va el contenido, qué llena el resto del lienzo, qué motivo lo acompaña y qué texto lleva (lockup, una frase, un dato estable).>

| Red | Archivo | Tamaño | Qué evitar |
|---|---|---|---|
| <Red> | `<Archivo>_<W>x<H>.png` | <W×H> | <lo que tapa la foto de perfil o el logo, lo que recorta el móvil> |

<Medidas por verificar en la plataforma, si las hay. Las redes cambian sus medidas: comprueba la pantalla de subida antes de cambiar un banner.>
