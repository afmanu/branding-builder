# Branding Builder

Plugin para crear o renovar la marca de una empresa con un método de agencia y entregarla lista para usar: un **Design System** con el manual de marca navegable, los tokens, las fuentes, la portada, el registro de decisiones y todos los assets descargables (logos, iconos, piezas de redes, patrones, mockups y manual en PDF), más un **ZIP** con los editables y el `favicon.ico`.

## Qué hace

1. **Alcance:** qué hace la empresa, para quién, qué se conserva y para qué se va a usar el kit.
2. **Descubrir** (profundidad Completa): público, visión interna y competidores con fuentes y fechas.
3. **Plataforma:** propósito, promesa, personalidad, voz e idea de marca. La redacta Claude y tú decides.
4. **Identidad:** naming si hace falta, 2–3 rutas visuales comparables, logo con su regla geométrica, color con contraste comprobado, tipografía con archivos reales y licencia, y 3 piezas de muestra antes de producir todo.
5. **Producción y entrega:** todas las piezas a tamaño exacto, revisión independiente, Design System publicado y ZIP.

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

Scripts incluidos (Python, en la skill principal): comprobación del entorno, estado y registro de decisiones, contraste WCAG, conversión de fuentes, tokens a CSS, render a PNG y PDF, iconos, índice del Design System, libro de marca alternativo y ZIP.

## Requisitos

- **Imprescindible para producir:** Python 3.9+, fontTools, Pillow, Playwright con Chromium.
- **Recomendado:** brotli (fuentes woff2), Node.js (fuentes de Google). **Solo para logos en PNG:** vtracer o potrace.
- `/branding-check` detecta lo que falta y da el comando exacto para macOS, Linux o Windows. Nunca instala nada sin permiso.
- La estrategia (alcance, diagnóstico, plataforma) no necesita ninguna herramienta.
- El resultado principal usa el tipo de artifact **Design System**. Si tu cuenta no lo tiene, el plugin publica un libro de marca en una página web con las mismas descargas.

## Instalación

En Claude Code, en un paso:

```
/plugin install branding-builder --marketplace afmanu/branding-builder
```

En la app de Claude, añade el marketplace `afmanu/branding-builder` en **Customize → Plugins** e instala **branding-builder**. Más detalles en el README del repositorio.

## Uso

- `/branding-nuevo Acme Estudio, estudio de arquitectura en Valencia` y responde a las preguntas.
- O pídelo con tus palabras: «quiero crear la marca de mi empresa».
- Si lo dejas a medias, guarda el expediente que te entrega y retómalo con `/branding-retomar`.

## Créditos

Método basado en el sistema «crear-branding» de Manuel Álvarez (fases, puntos de validación y validador de estado), adaptado a Claude y ampliado con la producción del kit.
