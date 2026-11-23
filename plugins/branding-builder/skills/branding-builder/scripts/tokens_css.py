#!/usr/bin/env python3
"""Genera brand.css a partir de project/tokens.json para que las plantillas usen los tokens reales.

Uso:
  python3 tokens_css.py project/tokens.json editables/brand.css

Crea:
  - @font-face de cada fuente de type.fonts (rutas relativas desde el CSS)
  - :root con todos los tokens del primer tema (--bg, --ink…), colores de marca, spacing, radius
    y cualquier otra familia (--angle-cut…), más --font-display / --font-sans / --font-mono
  - [data-theme="<id>"] y .tema-<id> para los demás temas
  - clases .t-<estilo> para cada estilo tipográfico (p. ej. .t-display-xl)
Los nombres de variables coinciden con los del Design System, así que las piezas se ven igual en ambos sitios.
"""
import json
import os
import sys


def valor_css(v):
    if isinstance(v, str) and v.startswith("{") and v.endswith("}"):
        return f"var(--{v[1:-1]})"
    return v


def formato(ruta):
    ext = os.path.splitext(ruta)[1].lower().lstrip(".")
    return {"woff2": "woff2", "woff": "woff", "ttf": "truetype", "otf": "opentype"}.get(ext, ext)


def generar(ruta_tokens, ruta_css):
    with open(ruta_tokens, encoding="utf-8") as f:
        t = json.load(f)
    base_proyecto = os.path.dirname(os.path.abspath(ruta_tokens))
    base_css = os.path.dirname(os.path.abspath(ruta_css))
    lineas = [f"/* {t.get('name', 'Marca')} — generado desde tokens.json con tokens_css.py */"]

    tipo = t.get("type", {})
    for fnt in tipo.get("fonts", []):
        archivo = os.path.join(base_proyecto, fnt["file"])
        rel = os.path.relpath(archivo, base_css).replace(os.sep, "/")
        estilo = fnt.get("style", "normal")
        lineas.append(
            "@font-face { font-family: \"%s\"; src: url(\"%s\") format(\"%s\"); font-weight: %s; font-style: %s; font-display: swap; }"
            % (fnt["family"], rel, formato(rel), fnt.get("weight", "400"), estilo)
        )

    color = t.get("color", {})
    temas = [x["id"] for x in color.get("themes", [])] or ["light"]
    principal = temas[0]
    raiz = []
    otros = {tema: [] for tema in temas[1:]}
    for tok in color.get("tokens", []):
        v = tok.get("value")
        if isinstance(v, dict):
            base = v.get(principal) or next(iter(v.values()))
            raiz.append(f"  --{tok['name']}: {valor_css(base)};")
            for tema in temas[1:]:
                if tema in v:
                    otros[tema].append(f"  --{tok['name']}: {valor_css(v[tema])};")
        else:
            raiz.append(f"  --{tok['name']}: {valor_css(v)};")
    for familia, contenido in t.items():
        if familia in ("name", "version", "color", "type", "meta") or not isinstance(contenido, dict):
            continue
        for tok in contenido.get("tokens", []):
            raiz.append(f"  --{tok['name']}: {valor_css(tok['value'])};")
    for clave, pila in tipo.get("families", {}).items():
        raiz.append(f"  --font-{clave}: {pila};")
    lineas.append(":root {\n" + "\n".join(raiz) + "\n}")
    for tema, decl in otros.items():
        if decl:
            lineas.append(f"[data-theme=\"{tema}\"], .tema-{tema} {{\n" + "\n".join(decl) + "\n}")

    for grupo in tipo.get("groups", []):
        fam = grupo.get("family", "sans")
        for e in grupo.get("styles", []):
            props = [f"font-family: var(--font-{fam})"]
            if "fontSize" in e:
                props.append(f"font-size: {e['fontSize']}")
            if "lineHeight" in e:
                props.append(f"line-height: {e['lineHeight']}")
            if "fontWeight" in e:
                props.append(f"font-weight: {e['fontWeight']}")
            if "letterSpacing" in e:
                props.append(f"letter-spacing: {e['letterSpacing']}")
            if e.get("textTransform"):
                props.append(f"text-transform: {e['textTransform']}")
            lineas.append(f".t-{e['name']} {{ " + "; ".join(props) + "; }")

    os.makedirs(base_css, exist_ok=True)
    with open(ruta_css, "w", encoding="utf-8") as f:
        f.write("\n".join(lineas) + "\n")
    print(f"brand.css escrito en {ruta_css} ({len(raiz)} variables, {len(tipo.get('fonts', []))} fuentes)")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    generar(sys.argv[1], sys.argv[2])
