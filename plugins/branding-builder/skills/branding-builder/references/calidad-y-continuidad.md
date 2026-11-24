# Estado, cambios, calidad y entrega

`$S` = la carpeta `scripts/` de esta skill.

## Estado del proyecto y registro de decisiones

Un solo archivo guarda el estado: `expediente/project-state.json`. `decisiones.md` se genera a partir de él, así que nunca hay dos registros que se contradigan.

```bash
python3 $S/estado.py init expediente/project-state.json --empresa "<Empresa>" --objetivo "<objetivo>" \
    --profundidad completa|expres --naming retain|create|change|undecided [--nombre-existente "<Nombre>"] --entregable "<…>"
python3 $S/estado.py preparar expediente/project-state.json H02 --salida "expediente/plataforma-v1.md"
python3 $S/estado.py aprobar  expediente/project-state.json H02 --ref "mensaje del usuario en el chat, <fecha>"
python3 $S/estado.py cambios  expediente/project-state.json H02 --ref "…" --nota "qué pidió cambiar"
python3 $S/estado.py nueva-version expediente/project-state.json H02 --motivo "…"   # marca los derivados como pendientes de revisión
python3 $S/estado.py pendiente expediente/project-state.json "Registro de marca sin comprobar"
python3 $S/estado.py alcance expediente/project-state.json --anadir-entregable "Banners de perfil: X y LinkedIn"   # --entregable sustituye la lista
python3 $S/estado.py mantenimiento expediente/project-state.json --responsable "<quién>" --cambios "<qué necesita nueva aprobación>"
python3 $S/estado.py validar expediente/project-state.json [--punto H03_S]
python3 $S/estado.py md expediente/project-state.json --salida project/decisiones.md
```

- `preparar` exige que las dependencias estén aceptadas; `aprobar` exige que el punto esté preparado con su paquete.
- Al aprobar H00 en Exprés, H01 y H03_N pasan solos a «No aplica»; en Completa, H03_N también si se conserva el nombre.
- Registra como aprobado solo lo que la persona aprobó de verdad, con la referencia a su mensaje; nunca tu propia recomendación. Una aprobación parcial cubre solo lo que nombró. El script comprueba la estructura, no la autenticidad ni la calidad.
- Si `python3` no estuviera disponible, lleva el mismo registro a mano en `decisiones.md` y dilo.

## Continuidad entre sesiones

- Antes de publicar, el trabajo vive en la carpeta de trabajo y no pasa a otra conversación. Si la sesión termina con el proyecto a medias, guarda `expediente/` (con el estado), las láminas y los SVG de trabajo en la carpeta conectada o envíalos como ZIP, y di cuál es la siguiente decisión pendiente.
- Al retomar: pide el expediente o el enlace del Design System, ejecuta `estado.py validar`, lee `decisiones.md`, resume en dos líneas qué está resuelto y qué toca ahora, y sigue desde ahí sin repetir lo aprobado.

## Cambios y feedback

Clasifica el feedback antes de tocar nada y cambia solo el nivel afectado:

| El feedback trata de… | Vuelve a… |
|---|---|
| Promesa, público o capacidad real | Plataforma (H02; H01 si cambia el diagnóstico) |
| Concepto, territorio o nombre | Ruta visual o naming (H03_V / H03_N) |
| Ejecución, composición o una pieza concreta | Sistema aplicado (H03_S) |
| Archivos, entrega o mantenimiento | Entrega (H04) |

Si cambia un nivel alto, `estado.py nueva-version` marca lo que depende de él como pendiente de revisión; revísalo antes de darlo por bueno. Lo aprobado antes no se hereda a una versión distinta.

## Revisión de calidad antes de entregar

Si hay agentes disponibles, encarga la revisión al agente `revisor-de-marca` (no ha visto cómo se hizo el kit, así que el trabajo no se califica a sí mismo) y corrige lo que encuentre. Si no, hazla tú con estos criterios, sin inventar una puntuación global:

- **Coherencia:** promesa, voz y forma se sostienen entre piezas, y cada decisión central tiene su racional escrito en el README.
- **Pertinencia:** la identidad se diferencia de los códigos observados en la categoría. Si no hubo investigación (Exprés), queda escrito como límite.
- **Acabado y legibilidad:** todas las piezas revisadas a su tamaño de uso. Banners: `banners.py comprobar` sin errores y la simulación revisada (nada importante bajo la foto de perfil ni en lo que recorta el móvil; la misma regla de composición en todos).
- **Archivos utilizables:** abre cada exportación y comprueba nombres y tamaños, que los SVG son vectores reales (sin imágenes incrustadas) y que el PDF y el ZIP abren. Un archivo que falta o no abre es una carencia, no un detalle.
- **Repetibilidad:** crea una pieza nueva usando solo el README y los assets (p. ej. un formato que no esté incluido). Si falta una regla, añádela al README. Es una prueba hecha por Claude, no una validación con personas: preséntala así.
- **Estado honesto:** separa lo listo, lo de ejemplo y lo pendiente. Si falta algo necesario para los usos acordados, la entrega es parcial y se dice.

## Cierre (H04)

- Entrega el artifact y el ZIP (o la carpeta conectada).
- Cierra con: qué se construyó a partir de qué, qué se asumió o tiene datos de ejemplo, qué queda pendiente (según `decisiones.md`), qué queda fuera del artifact y una oferta de siguiente paso (acentos de color, más piezas o componentes web). Si la herramienta muestra una tarjeta con el enlace, no lo repitas.
- **H04:** la persona acepta el paquete con sus pendientes. Aceptar la entrega no autoriza a publicar en redes, contactar a terceros ni registrar nada.

## Checklist final

- [ ] Profundidad acordada; cada punto de validación aprobado de forma explícita y registrado (`estado.py validar` sin errores).
- [ ] Completa: diagnóstico con fuentes y límites; nada inventado.
- [ ] La plataforma justifica las decisiones visuales y aparece resumida en el README.
- [ ] Rutas o variantes con mecanismos distintos, en láminas comparables.
- [ ] Sistema aplicado aprobado antes de la producción completa.
- [ ] Modo B: logo original respetado; diferencias de vectorización avisadas.
- [ ] Los grupos, nombres de archivo y teselas siguen el plano (más los módulos pedidos).
- [ ] `contraste.py` sin fallos obligatorios en ambos temas, con cifras en el README.
- [ ] Fuentes reales con licencia que permita incluirlas, y su archivo de licencia.
- [ ] `tokens.json` en listas, con nota de uso en cada token; cada grupo de assets con README.
- [ ] Todas las piezas a tamaño exacto y revisadas visualmente.
- [ ] One pager A4 en PDF y PNG, con textos de la plataforma y el contacto marcado si es de ejemplo.
- [ ] Redes y Banners solo si la persona dijo que necesita elementos para redes sociales.
- [ ] Un banner por cada perfil del alcance; `banners.py comprobar --redes …` sin errores; simulación revisada; medidas «verificar» comprobadas o anotadas como pendientes.
- [ ] Textos y datos de ejemplo señalados como tales.
- [ ] Sin tópicos de IA en lo visual.
- [ ] Revisión independiente hecha y prueba de repetibilidad con reglas que faltaban añadidas.
- [ ] Manual PDF coherente con el README y con la misma versión.
- [ ] Índice generado con `indice.py` y escrito en la última llamada.
- [ ] ZIP con `favicon.ico`, licencias y editables entregado fuera del artifact.
