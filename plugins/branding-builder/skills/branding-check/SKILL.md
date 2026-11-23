---
name: branding-check
description: >
  Comprueba si el entorno tiene lo necesario para crear un brand kit con el plugin branding-builder
  y recomienda qué instalar. Se usa cuando el usuario escribe "/branding-check", "¿qué necesito
  instalar para el brand kit?", "comprueba mis herramientas de branding" o cuando otra skill del
  plugin necesita saber qué alternativa usar.
metadata:
  version: "0.1.0"
---

# Comprobar el entorno

1. Ejecuta `python3 ../branding-builder/scripts/check_env.py --json` (ruta completa desde la carpeta de esta skill; en Windows, `python`). Si Python no existe, dilo y da el comando de instalación de Python de `../branding-builder/references/herramientas.md` para el sistema de la persona.
2. Presenta el resultado en lenguaje llano:
   - una línea con el veredicto («Puedes hacer el kit completo», «Funciona con estas limitaciones…» o «Falta lo imprescindible…»);
   - una tabla corta con lo que falta: para qué sirve, qué pasa sin ello y el comando exacto para su sistema;
   - el aviso del entorno virtual si el script lo incluye.
3. Distingue dónde se ejecuta:
   - **Nube de Claude:** si no hay red, explica que puede permitir la instalación de paquetes en los ajustes de red de Claude y que el cambio se aplica en chats nuevos. Mientras, se usan las alternativas.
   - **Ordenador de la persona** (carpeta conectada con terminal, o Claude Code): ofrece ejecutar tú los comandos.
4. **Nunca instales nada sin un sí explícito**, y pide permiso de nuevo para cada comando que use `sudo` o cambie el sistema. Tras instalar, vuelve a ejecutar `check_env.py` y confirma el nuevo veredicto.
5. Recuerda que la estrategia (alcance, diagnóstico, plataforma) no necesita ninguna herramienta: si falta algo, el proyecto puede empezar igualmente.
