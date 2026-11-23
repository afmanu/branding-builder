#!/usr/bin/env python3
"""Comprueba qué herramientas hay para crear un brand kit y qué alternativa se usará si falta algo.

Uso:
  python3 check_env.py            # resumen legible
  python3 check_env.py --json     # resultado en JSON
  python3 check_env.py --sin-red  # no prueba la conexión a los registros de paquetes

No instala nada. Da el comando de instalación adecuado para el sistema operativo detectado.
"""
import importlib.util
import json
import os
import platform
import shutil
import subprocess
import sys
import urllib.request

SO = {"Darwin": "macos", "Linux": "linux", "Windows": "windows"}.get(platform.system(), "linux")
PY = "python" if SO == "windows" else "python3"


def tiene_modulo(nombre):
    return importlib.util.find_spec(nombre) is not None


def tiene_binario(nombre):
    return shutil.which(nombre) is not None


def ejecutar(cmd, timeout=60):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode == 0, (r.stdout or r.stderr or "").strip()
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)


def chromium_funciona():
    if not tiene_modulo("playwright"):
        return False
    codigo = (
        "from playwright.sync_api import sync_playwright\n"
        "with sync_playwright() as p:\n"
        "    b = p.chromium.launch(); b.close()\n"
        "print('ok')"
    )
    ok, salida = ejecutar([sys.executable, "-c", codigo], timeout=90)
    return ok and salida.endswith("ok")


def hay_red(url, timeout=8):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:  # noqa: S310
            return 200 <= r.status < 400
    except Exception:  # noqa: BLE001
        return False


def en_entorno_virtual():
    return sys.prefix != getattr(sys, "base_prefix", sys.prefix) or bool(os.environ.get("VIRTUAL_ENV"))


PIP = {
    "macos": "pip install {p}",
    "linux": "pip install {p}",
    "windows": "pip install {p}",
}
SISTEMA = {
    "node": {
        "macos": "brew install node",
        "linux": "sudo apt install nodejs npm",
        "windows": "winget install OpenJS.NodeJS.LTS",
    },
    "potrace": {
        "macos": "brew install potrace",
        "linux": "sudo apt install potrace",
        "windows": "Descarga potrace desde su web oficial (o usa vtracer con pip)",
    },
    "svg": {
        "macos": "brew install resvg librsvg",
        "linux": "sudo apt install librsvg2-bin",
        "windows": "Opcional: descarga resvg desde sus versiones publicadas en GitHub",
    },
    "python": {
        "macos": "brew install python",
        "linux": "sudo apt install python3 python3-venv",
        "windows": "winget install Python.Python.3.12",
    },
}


def comprobar(con_red=True):
    r = {"sistema": SO, "python": platform.python_version(), "entorno_virtual": en_entorno_virtual()}
    py_ok = sys.version_info >= (3, 9)
    fonttools = tiene_modulo("fontTools")
    pillow = tiene_modulo("PIL")
    brotli = tiene_modulo("brotli")
    playwright = tiene_modulo("playwright")
    chromium = chromium_funciona() if playwright else False
    node = tiene_binario("node")
    npm = tiene_binario("npm")
    vtracer = tiene_modulo("vtracer") or tiene_binario("vtracer")
    potrace = tiene_binario("potrace")
    resvg = tiene_binario("resvg")
    rsvg = tiene_binario("rsvg-convert")
    fc_list = tiene_binario("fc-list")
    red_npm = hay_red("https://registry.npmjs.org/@fontsource%2finter") if con_red else None
    red_pypi = hay_red("https://pypi.org/simple/brotli/") if con_red else None

    items = []

    def item(clave, nombre, ok, prioridad, para, sin, instalar):
        items.append({
            "clave": clave, "nombre": nombre, "ok": ok, "prioridad": prioridad,
            "para": para, "si_falta": sin, "instalar": instalar,
        })

    item("python", "Python 3.9 o superior", py_ok, "imprescindible",
         "Ejecutar todos los scripts del plugin", "No funciona ningún script", SISTEMA["python"][SO])
    item("fonttools", "fontTools", fonttools, "imprescindible",
         "Convertir fuentes y pasar texto a trazados", "No hay fuentes web propias ni lockups en SVG",
         PIP[SO].format(p="fonttools"))
    item("pillow", "Pillow", pillow, "imprescindible",
         "favicon.ico, iconos derivados y comprobación de tamaños", "Sin favicon.ico ni iconos derivados",
         PIP[SO].format(p="pillow"))
    item("playwright", "Playwright + Chromium", playwright and chromium, "imprescindible",
         "Renderizar piezas a tamaño exacto y generar los PDF",
         "Solo SVG sueltos con resvg/rsvg-convert; sin piezas HTML ni manual PDF",
         PIP[SO].format(p="playwright") + f" && {PY} -m playwright install" + (" --with-deps" if SO == "linux" else "") + " chromium")
    item("brotli", "brotli", brotli, "recomendada",
         "Fuentes en woff2", "Las fuentes salen en woff (algo más pesadas)", PIP[SO].format(p="brotli"))
    item("node", "Node.js y npm", node and npm, "recomendada",
         "Descargar fuentes de Google con @fontsource", "Solo se pueden usar fuentes instaladas en el equipo",
         SISTEMA["node"][SO])
    item("vectorizar", "vtracer o potrace", vtracer or potrace, "solo modo B",
         "Vectorizar un logo que llega en PNG", "Se redibuja a mano si es sencillo, o hay que pedir el SVG",
         PIP[SO].format(p="vtracer") + "   (o: " + SISTEMA["potrace"][SO] + ")")
    item("svg", "resvg o rsvg-convert", resvg or rsvg, "opcional",
         "Convertir SVG a PNG más rápido", "Se usa el navegador (más lento)", SISTEMA["svg"][SO])
    if con_red:
        item("red", "Acceso a los registros de paquetes", bool(red_npm or red_pypi), "recomendada",
             "Instalar lo que falte y descargar fuentes",
             "Solo se puede usar lo ya instalado",
             "En la nube de Claude: permite la instalación de paquetes en los ajustes de red (se aplica en chats nuevos). "
             "En tu equipo: comprueba la conexión o el proxy.")

    capacidades = {
        "render_html": chromium,
        "render_svg": chromium or resvg or rsvg,
        "pdf": chromium,
        "fuentes": "woff2" if (fonttools and brotli) else ("woff" if fonttools else "no"),
        "fuentes_google": bool(npm and red_npm),
        "buscar_fuentes_instaladas": fonttools,
        "lista_fuentes_sistema": fc_list,
        "vectorizar_png": vtracer or potrace,
        "iconos": pillow,
        "estado_y_decisiones": py_ok,
    }
    faltan_imprescindibles = [i["nombre"] for i in items if i["prioridad"] == "imprescindible" and not i["ok"]]
    limitaciones = []
    if capacidades["fuentes"] == "woff":
        limitaciones.append("las fuentes saldrán en woff en lugar de woff2")
    if not capacidades["fuentes_google"]:
        limitaciones.append("solo se podrán usar fuentes instaladas o que aportes tú")
    if not capacidades["vectorizar_png"]:
        limitaciones.append("si traes el logo en PNG, se redibuja a mano o se pide el SVG")
    if faltan_imprescindibles:
        veredicto = "Falta lo imprescindible: " + ", ".join(faltan_imprescindibles) + "."
        nivel = "bloqueado"
    elif limitaciones:
        veredicto = "Puedes hacer el kit, con estas limitaciones: " + "; ".join(limitaciones) + "."
        nivel = "con_limitaciones"
    else:
        veredicto = "Puedes hacer el kit completo."
        nivel = "completo"
    r.update({"nivel": nivel, "veredicto": veredicto, "capacidades": capacidades, "herramientas": items})
    if not en_entorno_virtual() and SO in ("macos", "linux") and any(not i["ok"] and i["instalar"].startswith("pip") for i in items):
        r["aviso_pip"] = (
            "Antes de usar pip, crea un entorno virtual: "
            "python3 -m venv ~/.branding-env && source ~/.branding-env/bin/activate"
        )
    elif SO == "windows" and any(not i["ok"] and i["instalar"].startswith("pip") for i in items):
        r["aviso_pip"] = (
            "Antes de usar pip, crea un entorno virtual: "
            "python -m venv %USERPROFILE%\\.branding-env && %USERPROFILE%\\.branding-env\\Scripts\\activate"
        )
    return r


def imprimir(r):
    marca = {True: "✔", False: "✘"}
    print(f"Sistema: {r['sistema']} · Python {r['python']}")
    print(r["veredicto"])
    print()
    for i in r["herramientas"]:
        print(f"{marca[bool(i['ok'])]} {i['nombre']} ({i['prioridad']}) — {i['para']}")
        if not i["ok"]:
            print(f"    Si falta: {i['si_falta']}")
            print(f"    Instalar: {i['instalar']}")
    if r.get("aviso_pip"):
        print()
        print(r["aviso_pip"])


def main():
    con_red = "--sin-red" not in sys.argv
    r = comprobar(con_red=con_red)
    if "--json" in sys.argv:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        imprimir(r)
    sys.exit(1 if r["nivel"] == "bloqueado" else 0)


if __name__ == "__main__":
    main()
