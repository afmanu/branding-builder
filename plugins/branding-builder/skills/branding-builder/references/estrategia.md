# Estrategia: fases 00, 01 y 02

## Fase 00 — Preparar el alcance

Extrae del encargo y los materiales: qué ofrece la organización y qué puede demostrar hoy, qué cambio busca, sus públicos, qué se conserva (nombre, logo, colores, reconocimiento), restricciones, para qué se va a usar el kit y quién aprueba (por defecto, el usuario). No presupongas que toda empresa tiene comunidad ni que necesita todas las redes.

### Preguntas de arranque (obligatorias, siempre las primeras)

Antes de cualquier otra pregunta, y antes de producir nada, haz estas cinco en una sola tanda con la herramienta de preguntas (opciones concretas y respuesta libre). Sus respuestas deciden qué módulos lleva el kit, además de la base obligatoria de `plano.md`:

1. **Redes sociales:** ¿la marca va a necesitar piezas para redes? ¿En qué canales? (multiselección: Instagram, X, LinkedIn perfil, LinkedIn página, YouTube, TikTok, Facebook, otras, ninguna)
2. **Material impreso:** ¿se va a imprimir algo más allá de la papelería básica? (cartelería, folletos, packaging, rotulación, ninguno)
3. **Presentaciones:** ¿se van a hacer presentaciones con frecuencia? (comerciales, formación, eventos)
4. **App o producto digital:** ¿hay o habrá web, app o producto digital propio? Si sí, los componentes de interfaz se amplían más allá de los básicos.
5. **Submarcas:** ¿existen o habrá productos, servicios o líneas con nombre propio? (p. ej. «Marca chat»)

Si alguna queda sin responder, no la supongas: el kit sale con la base obligatoria y **sin** los módulos que dependen de esa respuesta, y queda anotada con `estado.py pendiente` para añadirlos después con `/branding-cambio`. No inventes canales. Lo que ya se ve en los materiales (p. ej. un logo de submarca) sí cuenta como respuesta, pero confírmalo.

### Resto de preguntas

Pregunta lo que falte con la herramienta de preguntas (si no hay, en la conversación), en tandas de máximo 4 preguntas con opciones concretas y respuesta libre. Nunca pidas lo que ya se ve en los archivos. Total orientativo: unas 12–15 preguntas en Exprés y no más de 20 en Completa, repartidas entre fases.

- **Esencia:** nombre y eslogan (si no hay eslogan, ofrécete a proponer 3); qué hace, en una frase; para quién; referencias que le gustan y que no; idioma y tratamiento (tú / usted).
- **Encargo:** marca nueva, rebranding o solo identidad visual; el nombre se conserva, hay que crearlo o hay que cambiarlo (si se conserva, H03_N no aplica).
- **Usos:** a partir de los canales de la pregunta de arranque 1, los formatos de contenido que se repiten (p. ej. lanzamiento de producto, caso de cliente, consejo semanal); de aquí salen plantillas y etiquetas.
- **Perfiles con banner** (solo si hay redes): de los canales anteriores, qué perfiles existen o se van a abrir, porque cada uno lleva su banner: canal de YouTube, X, LinkedIn (perfil personal de quien da la cara, página de empresa o ambos), Facebook (página o grupo), Bluesky, Twitch, Discord, plataforma de comunidad o cursos (Skool, Whop…) y cabecera de newsletter. Ofrécelos como multiselección con los canales ya mencionados marcados; Instagram, TikTok y Threads no tienen banner. Para las plataformas con medida «verificar» del catálogo (`banners.py lista`), pide el tamaño que muestra su pantalla de subida o anótalo como pendiente. La lista de banners entra en los entregables del alcance.
- **Datos de empresa:** la papelería, la presentación y el one pager son base obligatoria (ver `plano.md`); pregunta si hay datos reales para tarjeta, membrete, firma y one pager o se usan de ejemplo, y si se necesitan plantillas de factura o presupuesto.
- **Modo B — Lo que existe:** logo en SVG (si solo hay PNG/JPG, avisa: se vectoriza con vtracer/potrace si están, o se redibuja a mano si es sencillo; los ilustrados o con degradados pierden calidad y se usan como PNG); colores en HEX (si no hay, se extraen del logo); tipografías y su licencia; restricciones (colores de la competencia, elementos obligatorios).

**H00:** presenta el alcance en 5–8 líneas, con la base obligatoria y los módulos activados por las preguntas de arranque (y los que quedan fuera por falta de respuesta), y registra la aprobación con `estado.py`. En Exprés va dentro del brief (fase 02).

## Fase 01 — Descubrir (solo Completa)

- **Público:** qué intenta conseguir y qué alternativa usa hoy; qué le atrae, qué le cuesta y qué le haría rechazar la oferta; qué necesita entender antes de comprar. Pregunta a la persona lo que sabe; no lo inventes.
- **Interno:** qué problema cree resolver la empresa y qué capacidad lo hace creíble, qué compromisos mantendría aunque le costaran una oportunidad y qué promesas actuales contradicen su comportamiento. Mantén separadas la visión de la empresa y la del público antes de sintetizar: un desacuerdo es información, no ruido.
- **Categoría:** encarga al agente `investigador-de-categoria` 3–6 competidores directos y 1–2 referencias de otras categorías (si no hay agentes, hazlo tú con búsqueda web). Por cada uno: público, promesa, lenguaje, códigos visuales (color dominante, tipo de logo, tipografía) y fecha de la observación. Resume qué códigos comparte la categoría (sirven para que se la reconozca) y dónde hay espacio para diferenciarse; un hueco en el mapa no prueba que haya demanda. Los colores dominantes de los competidores directos pasan a restricciones.
- **Datos reales del cliente** (reseñas, encuestas, entrevistas): úsalos citando la fuente, la muestra y sus límites, y calcula con código. Si no hay, entrega un diagnóstico provisional con las preguntas o el plan para conseguirlos; no simules respuestas.

Guarda el diagnóstico en `expediente/diagnostico.md`.

**H01 Diagnóstico:** problema reformulado, hallazgos con fuente y límites, tensiones, hipótesis que perdieron fuerza, 2–3 posiciones posibles y tu recomendación. Aprueba una base de trabajo; no convierte las hipótesis en hechos.

## Fase 02 — Definir la plataforma

Redáctala tú a partir de lo recogido. Usa solo los elementos que produzcan decisiones distintas; dos campos con la misma frase sobran.

| Elemento | Para qué sirve | Prueba de que es útil |
|---|---|---|
| Propósito | La contribución que justifica que exista | Orienta una renuncia real |
| Propuesta de valor | Necesidad + diferencia + razón para creer | El público prioritario la reconoce como suya |
| Atributos | Capacidades verificables hoy | Separa hechos de compromisos futuros |
| Valores | Pautas de conducta | Se traducen en comportamientos concretos |
| Personalidad y voz | Cómo habla y cómo se reconoce | Produce elecciones de tono y contraejemplos |
| Idea de marca | El principio que organiza todas las expresiones | Permite rutas distintas que siguen emparentadas |
| Relato | La historia corta que hace creíble la promesa | No inventa historia ni pruebas |

- **Personalidad:** 3–5 rasgos expresados como polos (cercana/institucional, técnica/divulgativa, sobria/vibrante, seria/juguetona u otros pertinentes), explicando qué significa cada extremo, y lo que la marca NO es. Nada de escalas numéricas sin interpretación.
- **Voz:** tono en 3–5 líneas, tratamiento y longitud de frase; 3–4 frases que la marca diría y otras tantas que no, con el porqué; titulares tipo; formato fijo de etiquetas por cada formato recurrente (p. ej. `<CATEGORÍA> · #01`); palabras prohibidas; emojis (sí / no / solo en canales informales). Los ejemplos los propones tú y se marcan como propuesta.
- Por cada elemento central: de dónde sale, qué decisión permite juzgar y qué consecuencia verbal o visual tiene.
- Pruébala con mensajes posibles e imposibles y di qué alternativa descarta. Si todo pasa el filtro, los criterios son demasiado vagos: concrétalos.

Guarda la plataforma en `expediente/plataforma-v<n>.md`; al publicar, la versión aprobada pasa a `project/plataforma.md`.

**H02 Plataforma** (Completa). En Exprés, presenta un **brief de una página** que reúne H00 y H02: nombre, eslogan, propósito, público, promesa, personalidad, voz, idea de marca, dirección de color y tipografía, `SIGLA` de los archivos, nombre de los dos temas (uno para el claro y otro para el oscuro, sacados de la paleta), fondos de marca (de ellos salen las versiones `-sobre-<fondo>`, los avatares y los iconos) y la lista de archivos que se van a producir (el plano filtrado por usos y módulos). En Completa, esos últimos datos técnicos se fijan en H03_S. No avances sin confirmación.
