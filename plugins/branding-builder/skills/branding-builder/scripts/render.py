#!/usr/bin/env python3
"""Renderiza piezas HTML o SVG a PNG al tamaño exacto, y páginas HTML a PDF.

Uso:
  python3 render.py png <entrada.html|svg> <salida.png> [--ancho W --alto H] [--param clave=valor ...] [--transparente]
  python3 render.py lote <manifiesto.json>
  python3 render.py pdf <entrada.html> <salida.pdf>

Tamaño: si no se indica, se toma del nombre de salida (…_1080x1080.png, …_1000.png, …_4000px.png),
de <meta name="lienzo" content="1080x1920"> en el HTML o del viewBox del SVG.
Con un SVG y solo --ancho, el alto sale de la proporción del viewBox.
--param añade parámetros a la URL (p. ej. --param f=youtube --param guias=1).
Manifiesto de lote: [{"entrada": "...", "salida": "...", "ancho": 1080, "alto": 1080, "params": {"f": "x"}, "transparente": false}]
El PDF respeta @page del HTML (las plantillas de manual y membrete ya lo traen).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import urllib.parse
from pathlib import Path


def tamano_desde_nombre(salida):
    nombre = Path(salida).stem
    m = re.search(r"_(\d+)x(\d+)(?:mm)?$", nombre)
    if m and not nombre.endswith("mm"):
        return int(m.group(1)), int(m.group(2))
    m = re.search(r"_(\d+)(?:px)?$", nombre)
    if m:
        n = int(m.group(1))
        return n, n
    return None


def viewbox(ruta_svg):
    texto = Path(ruta_svg).read_text(encoding="utf-8", errors="ignore")[:5000]
    m = re.search(r'viewBox="\s*([-\d.]+)[ ,]+([-\d.]+)[ ,]+([\d.]+)[ ,]+([\d.]+)\s*"', texto)
    if m:
        return float(m.group(3)), float(m.group(4))
    w = re.search(r'\swidth="([\d.]+)', texto)
    h = re.search(r'\sheight="([\d.]+)', texto)
    if w and h:
        return float(w.group(1)), float(h.group(1))
    return None


def lienzo_meta(ruta_html):
    texto = Path(ruta_html).read_text(encoding="utf-8", errors="ignore")[:5000]
    m = re.search(r'<meta\s+name="lienzo"\s+content="(\d+)x(\d+)"', texto)
    return (int(m.group(1)), int(m.group(2))) if m else None


def resolver_tamano(entrada, salida, ancho, alto):
    es_svg = entrada.lower().endswith(".svg")
    if ancho and alto:
        return ancho, alto
    if es_svg:
        vb = viewbox(entrada)
        desde_nombre = tamano_desde_nombre(salida)
        if ancho and vb:
            return ancho, round(ancho * vb[1] / vb[0])
        if alto and vb:
            return round(alto * vb[0] / vb[1]), alto
        if desde_nombre and vb:
            # «_4000px» fija el lado mayor
            lado = desde_nombre[0]
            if vb[0] >= vb[1]:
                return lado, round(lado * vb[1] / vb[0])
            return round(lado * vb[0] / vb[1]), lado
        if vb:
            return round(vb[0]), round(vb[1])
    else:
        t = tamano_desde_nombre(salida) or lienzo_meta(entrada)
        if t:
            return t
    sys.exit(f"No sé a qué tamaño renderizar {entrada}: indica --ancho y --alto.")


def url_de(entrada, params):
    url = Path(entrada).resolve().as_uri()
    if params:
        url += "?" + urllib.parse.urlencode(params)
    return url


def con_playwright(tareas):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav = p.chromium.launch()
        for t in tareas:
            entrada, salida = t["entrada"], t["salida"]
            ancho, alto = resolver_tamano(entrada, salida, t.get("ancho"), t.get("alto"))
            pagina = nav.new_page(viewport={"width": ancho, "height": alto}, device_scale_factor=1)
            if entrada.lower().endswith(".svg"):
                html = (f'<html><body style="margin:0;background:transparent">'
                        f'<img src="{Path(entrada).resolve().as_uri()}" style="display:block;width:{ancho}px;height:{alto}px">'
                        f'</body></html>')
                pagina.set_content(html)
                pagina.wait_for_load_state("networkidle")
            else:
                pagina.goto(url_de(entrada, t.get("params")))
                pagina.wait_for_load_state("networkidle")
            pagina.evaluate("document.fonts ? document.fonts.ready.then(() => true) : true")
            pagina.wait_for_timeout(150)
            Path(salida).parent.mkdir(parents=True, exist_ok=True)
            pagina.screenshot(path=salida, clip={"x": 0, "y": 0, "width": ancho, "height": alto},
                              omit_background=bool(t.get("transparente")))
            pagina.close()
            print(f"✔ {salida} ({ancho}×{alto})")
        nav.close()


def svg_sin_navegador(t):
    entrada, salida = t["entrada"], t["salida"]
    ancho, alto = resolver_tamano(entrada, salida, t.get("ancho"), t.get("alto"))
    if shutil.which("resvg"):
        cmd = ["resvg", "-w", str(ancho), "-h", str(alto), entrada, salida]
    elif shutil.which("rsvg-convert"):
        cmd = ["rsvg-convert", "-w", str(ancho), "-h", str(alto), "-o", salida, entrada]
    else:
        sys.exit("No hay Playwright ni resvg/rsvg-convert para renderizar SVG.")
    Path(salida).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(cmd, check=True)
    print(f"✔ {salida} ({ancho}×{alto}, sin navegador)")


def renderizar(tareas):
    try:
        import playwright  # noqa: F401
        con_playwright(tareas)
    except ImportError:
        html = [t for t in tareas if not t["entrada"].lower().endswith(".svg")]
        if html:
            sys.exit("Las piezas HTML necesitan Playwright: pip install playwright && python3 -m playwright install chromium")
        for t in tareas:
            svg_sin_navegador(t)


def pdf(entrada, salida):
    from playwright.sync_api import sync_playwright
    with sync_playwright() as p:
        nav = p.chromium.launch()
        pagina = nav.new_page()
        pagina.goto(url_de(entrada, None))
        pagina.wait_for_load_state("networkidle")
        pagina.evaluate("document.fonts ? document.fonts.ready.then(() => true) : true")
        Path(salida).parent.mkdir(parents=True, exist_ok=True)
        pagina.pdf(path=salida, print_background=True, prefer_css_page_size=True)
        nav.close()
    print(f"✔ {salida} ({os.path.getsize(salida) // 1024} KB)")


def main():
    a = sys.argv[1:]
    if not a:
        sys.exit(__doc__)
    if a[0] == "png" and len(a) >= 3:
        t = {"entrada": a[1], "salida": a[2], "params": {}}
        resto = a[3:]
        while resto:
            op = resto.pop(0)
            if op == "--ancho":
                t["ancho"] = int(resto.pop(0))
            elif op == "--alto":
                t["alto"] = int(resto.pop(0))
            elif op == "--param":
                k, _, v = resto.pop(0).partition("=")
                t["params"][k] = v
            elif op == "--transparente":
                t["transparente"] = True
            else:
                sys.exit(f"Opción desconocida: {op}")
        renderizar([t])
    elif a[0] == "lote" and len(a) == 2:
        with open(a[1], encoding="utf-8") as f:
            tareas = json.load(f)
        base = os.path.dirname(os.path.abspath(a[1]))
        for t in tareas:
            for k in ("entrada", "salida"):
                if not os.path.isabs(t[k]):
                    t[k] = os.path.join(base, t[k])
        renderizar(tareas)
    elif a[0] == "pdf" and len(a) == 3:
        pdf(a[1], a[2])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main()
