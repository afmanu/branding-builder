#!/usr/bin/env python3
"""Fuentes para el brand kit: buscar las instaladas, convertirlas a fuente web y pasar texto a trazados SVG.

Uso:
  python3 fuentes.py buscar "Space Grotesk"
  python3 fuentes.py convertir <archivo.ttf|otf> --familia "Space Grotesk" --peso 700 --salida project/fonts
        [--estilo normal|italic] [--formato auto|woff2|woff] [--completa]
  python3 fuentes.py texto-svg <archivo.ttf|otf> "Texto" --tamano 120 [--tracking 0] [--color "#000000"] [--salida texto.svg]

`convertir` hace un subconjunto latino (salvo --completa), fija el peso si la fuente es variable
e imprime la entrada lista para `type.fonts` de tokens.json.
`texto-svg` no aplica kerning GPOS: revisa siempre el resultado a ojo.
"""
import argparse
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys

UNICODES_LATIN = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD"
CARPETAS = [
    "/usr/share/fonts", "/usr/local/share/fonts", os.path.expanduser("~/.fonts"),
    os.path.expanduser("~/.local/share/fonts"), "/Library/Fonts", os.path.expanduser("~/Library/Fonts"),
    "/System/Library/Fonts", "C:\\Windows\\Fonts",
]


def requiere_fonttools():
    if importlib.util.find_spec("fontTools") is None:
        sys.exit("Falta fontTools: pip install fonttools")


def kebab(texto):
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-")


def info_fuente(ruta):
    from fontTools.ttLib import TTFont
    try:
        f = TTFont(ruta, fontNumber=0, lazy=True)
    except Exception:  # noqa: BLE001
        return None
    nombre = f["name"]
    familia = nombre.getDebugName(16) or nombre.getDebugName(1) or ""
    sub = nombre.getDebugName(17) or nombre.getDebugName(2) or ""
    peso = getattr(f["OS/2"], "usWeightClass", 400) if "OS/2" in f else 400
    variable = "fvar" in f
    italica = "italic" in sub.lower() or "oblique" in sub.lower()
    return {"archivo": ruta, "familia": familia, "subfamilia": sub, "peso": peso,
            "estilo": "italic" if italica else "normal", "variable": variable}


def buscar(familia):
    requiere_fonttools()
    rutas = set()
    if shutil.which("fc-list"):
        out = subprocess.run(["fc-list", ":", "file", "family"], capture_output=True, text=True).stdout
        for linea in out.splitlines():
            archivo, _, fam = linea.partition(":")
            if familia.lower() in fam.lower():
                rutas.add(archivo.strip())
    else:
        for carpeta in CARPETAS:
            for ext in ("ttf", "otf", "TTF", "OTF"):
                rutas.update(glob.glob(os.path.join(carpeta, "**", f"*.{ext}"), recursive=True))
    encontradas = []
    for ruta in sorted(rutas):
        i = info_fuente(ruta)
        if i and familia.lower() in i["familia"].lower():
            encontradas.append(i)
    print(json.dumps(encontradas, ensure_ascii=False, indent=2))
    if not encontradas:
        sys.exit(f"No hay ninguna fuente instalada de la familia «{familia}».")


def convertir(a):
    requiere_fonttools()
    from fontTools import subset
    from fontTools.ttLib import TTFont

    formato = a.formato
    if formato == "auto":
        formato = "woff2" if importlib.util.find_spec("brotli") else "woff"
    if formato == "woff2" and importlib.util.find_spec("brotli") is None:
        sys.exit("woff2 necesita brotli (pip install brotli). Usa --formato woff.")
    fuente = TTFont(a.archivo)
    if "fvar" in fuente:
        from fontTools.varLib import instancer
        ejes = {e.axisTag: (e.minValue, e.maxValue) for e in fuente["fvar"].axes}
        fijar = {}
        if "wght" in ejes:
            lo, hi = ejes["wght"]
            fijar["wght"] = max(lo, min(hi, a.peso))
        if "ital" in ejes:
            fijar["ital"] = 1 if a.estilo == "italic" else 0
        # Los demás ejes (opsz, wdth…) se fijan en su valor por defecto para obtener una fuente estática.
        for eje in fuente["fvar"].axes:
            fijar.setdefault(eje.axisTag, eje.defaultValue)
        try:
            fuente = instancer.instantiateVariableFont(fuente, fijar, updateFontNames=True)
        except Exception:  # noqa: BLE001  (sin tabla STAT no se pueden renombrar las instancias)
            fuente = instancer.instantiateVariableFont(TTFont(a.archivo), fijar)
    if not a.completa:
        opciones = subset.Options()
        opciones.layout_features = ["*"]
        opciones.name_IDs = ["*"]
        opciones.name_languages = ["*"]
        opciones.notdef_outline = True
        sub = subset.Subsetter(options=opciones)
        sub.populate(unicodes=subset.parse_unicodes(UNICODES_LATIN))
        sub.subset(fuente)
    fuente.flavor = formato
    os.makedirs(a.salida, exist_ok=True)
    nombre = f"{kebab(a.familia)}-latin-{a.peso}-{a.estilo}.{formato}" if not a.completa \
        else f"{kebab(a.familia)}-{a.peso}-{a.estilo}.{formato}"
    destino = os.path.join(a.salida, nombre)
    fuente.save(destino)
    relativa = "fonts/" + nombre
    entrada = {"family": a.familia, "file": relativa, "weight": str(a.peso)}
    if a.estilo == "italic":
        entrada["style"] = "italic"
    # Copia la licencia que acompañe a la fuente (OFL.txt, LICENSE…): las fuentes libres exigen distribuirla con ellas.
    licencia = None
    carpeta = os.path.dirname(os.path.abspath(a.archivo))
    for candidato in ("OFL.txt", "LICENSE.txt", "LICENSE", "OFL", "license.txt"):
        origen = os.path.join(carpeta, candidato)
        if os.path.isfile(origen):
            licencia = os.path.join(a.salida, f"{kebab(a.familia)}-LICENCIA.txt")
            shutil.copyfile(origen, licencia)
            break
    resultado = {"archivo": destino, "bytes": os.path.getsize(destino), "token": entrada, "licencia": licencia}
    if not licencia:
        resultado["aviso"] = "No se encontró el archivo de licencia junto a la fuente: confirma que permite incluirla en el kit."
    print(json.dumps(resultado, ensure_ascii=False, indent=2))


def texto_svg(a):
    requiere_fonttools()
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont

    f = TTFont(a.archivo)
    glifos = f.getGlyphSet()
    cmap = f.getBestCmap()
    upm = f["head"].unitsPerEm
    escala = a.tamano / upm
    asc = f["hhea"].ascent
    desc = f["hhea"].descent
    x = 0.0
    trazos = []
    for car in a.texto:
        g = cmap.get(ord(car))
        if g is None:
            print(f"Aviso: «{car}» no existe en la fuente; se omite.", file=sys.stderr)
            continue
        pen = SVGPathPen(glifos)
        glifos[g].draw(TransformPen(pen, (escala, 0, 0, -escala, x, asc * escala)))
        d = pen.getCommands()
        if d:
            trazos.append(d)
        x += glifos[g].width * escala + a.tracking * a.tamano
    if a.texto:
        x -= a.tracking * a.tamano
    ancho = max(1, round(x))
    alto = round((asc - desc) * escala)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {ancho} {alto}" width="{ancho}" height="{alto}">'
           f'<path fill="{a.color}" d="{" ".join(trazos)}"/></svg>\n')
    if a.salida:
        with open(a.salida, "w", encoding="utf-8") as fh:
            fh.write(svg)
        print(json.dumps({"archivo": a.salida, "ancho": ancho, "alto": alto}, ensure_ascii=False))
    else:
        sys.stdout.write(svg)
    print("Aviso: sin kerning GPOS; revisa el espaciado a ojo.", file=sys.stderr)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    b = sp.add_parser("buscar")
    b.add_argument("familia")
    c = sp.add_parser("convertir")
    c.add_argument("archivo")
    c.add_argument("--familia", required=True)
    c.add_argument("--peso", type=int, default=400)
    c.add_argument("--estilo", choices=["normal", "italic"], default="normal")
    c.add_argument("--formato", choices=["auto", "woff2", "woff"], default="auto")
    c.add_argument("--salida", default="project/fonts")
    c.add_argument("--completa", action="store_true", help="sin subconjunto latino")
    t = sp.add_parser("texto-svg")
    t.add_argument("archivo")
    t.add_argument("texto")
    t.add_argument("--tamano", type=float, default=100)
    t.add_argument("--tracking", type=float, default=0, help="en em, p. ej. -0.02")
    t.add_argument("--color", default="#000000")
    t.add_argument("--salida")
    a = p.parse_args()
    if a.cmd == "buscar":
        buscar(a.familia)
    elif a.cmd == "convertir":
        convertir(a)
    else:
        texto_svg(a)


if __name__ == "__main__":
    main()
