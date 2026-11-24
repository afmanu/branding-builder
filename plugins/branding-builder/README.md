# Branding Builder

Plugin para crear o renovar la marca de una empresa con un método de agencia y entregarla lista para usar: un **Design System** con el manual de marca navegable, los tokens, las fuentes, la portada, el registro de decisiones y todos los assets descargables (logos, iconos, piezas de redes, banners de cada perfil social, patrones, mockups y manual en PDF), más un **ZIP** con los editables y el `favicon.ico`.

## Qué hace

1. **Alcance:** qué hace la empresa, para quién, qué se conserva, para qué se va a usar el kit y qué perfiles sociales tiene (cada uno lleva su banner).
2. **Descubrir** (profundidad Completa): público, visión interna y competidores con fuentes y fechas.
3. **Plataforma:** propósito, promesa, personalidad, voz e idea de marca. La redacta Claude y tú decides.
4. **Identidad:** naming si hace falta, 2–3 rutas visuales comparables, logo con su regla geométrica, color con contraste comprobado, tipografía con archivos reales y licencia, y 3 piezas de muestra antes de producir todo.
5. **Producción y entrega:** todas las piezas a tamaño exacto (también los banners de YouTube, X, LinkedIn, Facebook, Bluesky, Twitch, Discord, Skool, Whop, Pinterest y newsletter, con su zona segura y lo que tapa la foto de perfil), revisión independiente, Design System publicado y ZIP.

Hay dos profundidades: **Completa** (6–7 aprobaciones, para una empresa real o un rebranding) y **Exprés** (unas 3 aprobaciones, sin investigación ni naming). Cada aprobación queda registrada con su versión.

## Componentes

| Tipo | Nombre | Para qué |
|---|---|---|
| Skill | `branding-builder` | El método completo, con referencias por fase, scripts y plantillas |
| Skill | `/branding-nuevo` | Empezar una marca nueva |
| Skill | `/branding-retomar` | Seguir un proyecto a medias desde su expediente |
| Skill | `/branding-cambio` | Cambiar o ampliar un kit ya publicado |
| Skill | `/branding-check` | Comprobar herramientas y recomendar qué instalar |
| Agente | `investigador-de-categoria` | Competidores y códigos de la categoría, con fuentes |
| Agente | `revisor-de-marca` | Revisión independiente del kit antes de entregarlo |

Scripts incluidos (Python, en la skill principal): comprobación del entorno, estado y registro de decisiones, contraste WCAG, conversión de fuentes, tokens a CSS, render a PNG y PDF, iconos, banners de perfil (catálogo de medidas por red revisado en noviembre de 2026, comprobación de tamaño y peso, y simulación de lo que tapa la interfaz), índice del Design System, libro de marca alternativo y ZIP.

## Requisitos

- **Imprescindible para producir:** Python 3.9+, fontTools, Pillow, Playwright con Chromium.
- **Recomendado:** brotli (fuentes woff2), Node.js (fuentes de Google). **Solo para logos en PNG:** vtracer o potrace.
- `/branding-check` detecta lo que falta y da el comando exacto para macOS, Linux o Windows. Nunca instala nada sin permiso.
- La estrategia (alcance, diagnóstico, plataforma) no necesita ninguna herramienta.
- El resultado principal usa el tipo de artifact **Design System**. Si tu cuenta no lo tiene, el plugin publica un libro de marca en una página web con las mismas descargas.

## Uso

- `/branding-nuevo Acme Estudio, estudio de arquitectura en Valencia` y responde a las preguntas.
- O pídelo con tus palabras: «quiero crear la marca de mi empresa».
- Si lo dejas a medias, guarda el expediente que te entrega y retómalo con `/branding-retomar`.

## Banners de perfil

El catálogo `templates/piezas/banners-formatos.js` guarda por red el tamaño, la zona segura, lo que tapa la interfaz, lo que recorta el móvil, el peso máximo y la fuente con su fiabilidad. Las redes cambian estas medidas: cuando pase, se corrige ese archivo y la plantilla y los scripts lo recogen solos. Las plataformas marcadas «verificar» (Skool, Whop, Twitch, Discord, Pinterest) se comprueban en su pantalla de subida antes de producir.

## Créditos

Método basado en el sistema «crear-branding» de Manuel Álvarez (fases, puntos de validación y validador de estado), adaptado a Claude y ampliado con la producción del kit.
