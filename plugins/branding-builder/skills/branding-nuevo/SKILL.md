---
name: branding-nuevo
description: >
  Empieza un proyecto de marca nuevo con el plugin branding-builder. Se usa cuando el usuario escribe
  "/branding-nuevo", "empieza una marca nueva", "quiero crear la marca de mi empresa desde cero" o
  "hazme un brand kit nuevo", con o sin el nombre de la empresa y un briefing.
metadata:
  version: "0.1.0"
---

# Nueva marca

Arranca un proyecto de marca nuevo con el método de la skill `branding-builder` de este plugin.

1. Localiza la skill principal: está en `../branding-builder/` respecto a la carpeta de esta skill. Lee su `SKILL.md` y sigue su flujo desde el paso 0; sus scripts están en `../branding-builder/scripts/`.
2. Ejecuta `python3 ../branding-builder/scripts/check_env.py` (con la ruta completa) y resume el veredicto en una línea. Si falta algo imprescindible, la estrategia puede avanzar igualmente; ofrece resolverlo antes de producir (ver `/branding-check`).
3. Usa lo que el usuario haya escrito junto al comando (nombre de la empresa, briefing, archivos adjuntos) para no preguntar lo que ya está dicho. Si adjunta logo, colores o una web, es modo B.
4. Si el modo o la profundidad (Completa o Exprés) no están claros, pregúntalos juntos en una sola pregunta, recomendando Completa para una empresa real o un rebranding y Exprés para pruebas o prisa.
5. Crea la carpeta `<marca>-kit/` y el estado con `estado.py init`, y empieza la fase 00 según `references/estrategia.md` de la skill principal.

No empieces a diseñar antes de que la persona apruebe el alcance (H00) y, en Exprés, el brief.
