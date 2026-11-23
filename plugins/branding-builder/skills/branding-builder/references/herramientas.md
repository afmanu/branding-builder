# Herramientas recomendadas

`check_env.py` detecta todo esto y da el comando para el sistema operativo en uso. Nunca instales nada sin un sí explícito de la persona.

| Herramienta | Para qué sirve | Si no está | Prioridad |
|---|---|---|---|
| Python 3.9+ | Ejecutar los scripts del plugin | No funciona ningún script | Imprescindible |
| fontTools | Convertir fuentes y pasar texto a trazados | Sin fuentes web propias ni lockups en SVG | Imprescindible |
| Pillow | favicon.ico, iconos derivados, hojas de contacto | Sin favicon.ico ni iconos derivados | Imprescindible |
| Playwright + Chromium | Renderizar piezas a tamaño exacto y generar los PDF | Solo SVG sueltos; sin piezas HTML ni manual | Imprescindible para producir (no para la estrategia) |
| brotli | Fuentes en woff2 | Salen en woff, algo más pesadas | Recomendada |
| Node.js y npm | Fuentes de Google con `@fontsource` | Solo fuentes instaladas o aportadas | Recomendada |
| vtracer o potrace | Vectorizar un logo que llega en PNG | Se redibuja a mano si es sencillo, o se pide el SVG | Solo modo B |
| resvg o rsvg-convert | SVG a PNG más rápido | Se usa el navegador | Opcional |
| Inkscape o Figma | Retocar los SVG a mano después | Nada: es para la persona | Opcional |

## Comandos

```bash
# macOS (con Homebrew)
brew install python node potrace librsvg resvg
python3 -m venv ~/.branding-env && source ~/.branding-env/bin/activate
pip install fonttools brotli pillow playwright vtracer
python -m playwright install chromium

# Linux (Debian/Ubuntu)
sudo apt install python3-venv nodejs npm potrace librsvg2-bin
python3 -m venv ~/.branding-env && source ~/.branding-env/bin/activate
pip install fonttools brotli pillow playwright vtracer
python -m playwright install --with-deps chromium

# Windows (con winget)
winget install Python.Python.3.12 OpenJS.NodeJS.LTS
python -m venv %USERPROFILE%\.branding-env && %USERPROFILE%\.branding-env\Scripts\activate
pip install fonttools brotli pillow playwright vtracer
python -m playwright install chromium
```

El entorno virtual hace falta porque las versiones recientes de macOS y Ubuntu bloquean `pip install` fuera de uno. En Windows, potrace y resvg se descargan de sus webs; con vtracer basta.

## Según dónde se ejecute

- **En la nube de Claude:** Python, Node y Playwright suelen venir instalados. Si falta algo y no hay red, la persona puede permitir la instalación de paquetes en los ajustes de red de Claude; el cambio se aplica en chats nuevos, no en el abierto. Mientras tanto, sigue con las alternativas.
- **En el ordenador de la persona** (app de escritorio con carpeta conectada o Claude Code): puedes ejecutar los comandos por ella, pidiendo permiso antes de cada instalación.
- **Sin poder instalar:** la estrategia (fases 00–02) no necesita nada; avanza con ella y deja la producción para cuando haya lo imprescindible.
