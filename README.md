# Branding Builder

Plugin para Claude que crea o renueva la marca de una empresa con un método de agencia y la entrega lista para usar: un **Design System** con el manual de marca navegable, los tokens, las fuentes, el registro de decisiones y todos los assets descargables (logos, iconos, piezas de redes, patrones, mockups y manual en PDF), más un **ZIP** con los editables.

Este repositorio es un catálogo de plugins (marketplace) llamado `afmanu-branding`. Contiene un plugin: `branding-builder`.

## Instalación

> El repositorio es privado: para instalarlo necesitas acceso a él en GitHub (pide que te inviten como colaborador).

### En la app de Claude (web, escritorio y Cowork)

1. Abre **Customize** → **Plugins**.
2. Añade un marketplace desde GitHub con `afmanu/branding-builder` (o `https://github.com/afmanu/branding-builder`). Como el repositorio es privado, Claude puede pedirte que conectes tu cuenta de GitHub.
3. Instala **branding-builder**.

El plugin se guarda en tu cuenta y sus skills funcionan en el chat, en Cowork y en Claude Code. Los agentes (investigador y revisor) solo se ejecutan en Cowork y Claude Code; en el chat, el método hace su trabajo directamente.

### En Claude Code

```
/plugin marketplace add afmanu/branding-builder
/plugin install branding-builder@afmanu-branding
```

Desde la versión 2.1.275 de Claude Code también se puede en un solo paso:

```
/plugin install branding-builder --marketplace afmanu/branding-builder
```

Para un repositorio privado, tu equipo necesita credenciales de GitHub guardadas: una clave SSH cargada en `ssh-agent`, o `gh auth login` seguido de `gh auth setup-git`. Sin clave SSH, define `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`.

### Actualizaciones

Cada versión nueva sube el número de `version` del plugin. En Claude Code, ejecuta `/plugin marketplace update afmanu-branding` o activa la actualización automática del marketplace en `/plugin` → **Marketplaces**.

## Uso

| Comando | Para qué |
|---|---|
| `/branding-nuevo` | Empezar una marca nueva (p. ej. `/branding-nuevo Acme Estudio, estudio de arquitectura en Valencia`) |
| `/branding-retomar` | Seguir un proyecto a medias desde su expediente |
| `/branding-cambio` | Cambiar o ampliar un kit ya publicado |
| `/branding-check` | Comprobar las herramientas y ver qué instalar |

También funciona pidiéndolo con tus palabras: «quiero crear la marca de mi empresa».

Hay dos profundidades: **Completa** (investigación, plataforma, rutas visuales y naming; 6–7 aprobaciones) y **Exprés** (unas 3 aprobaciones, sin investigación ni naming).

## Requisitos

La estrategia (alcance, diagnóstico, plataforma) no necesita nada. Para producir las piezas:

| Herramienta | Para qué | Prioridad |
|---|---|---|
| Python 3.9+, fontTools, Pillow | Scripts, fuentes, iconos | Imprescindible |
| Playwright + Chromium | Piezas a tamaño exacto y PDF | Imprescindible |
| brotli | Fuentes en woff2 | Recomendada |
| Node.js | Fuentes de Google | Recomendada |
| vtracer o potrace | Vectorizar un logo en PNG | Solo si traes el logo en PNG |

`/branding-check` detecta lo que falta y da el comando para macOS, Linux o Windows. No instala nada sin tu permiso.

El resultado usa el tipo de artifact **Design System**. Si tu cuenta no lo tiene, el plugin publica la marca como una página web con las mismas descargas.

## Contenido

```
.claude-plugin/marketplace.json      catálogo (marketplace afmanu-branding)
plugins/branding-builder/
  .claude-plugin/plugin.json
  skills/branding-builder/            el método: SKILL.md, referencias por fase, scripts y plantillas
  skills/branding-nuevo|retomar|cambio|check/
  agents/investigador-de-categoria.md
  agents/revisor-de-marca.md
```

## Licencia

MIT. Método basado en el sistema «crear-branding» de Manuel Álvarez, adaptado a Claude y ampliado con la producción del kit.
