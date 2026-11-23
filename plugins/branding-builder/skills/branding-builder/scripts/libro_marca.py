#!/usr/bin/env python3
"""Libro de marca en una página web: la alternativa cuando la cuenta no tiene el tipo Design System.

Uso:
  python3 libro_marca.py --project <kit>/project --salida <kit>/libro

Crea <salida>/index.html con el README, la plataforma y las decisiones, muestras de color de cada tema,
la escala tipográfica con las fuentes reales y una galería de assets con enlaces de descarga, y copia
assets/ y fonts/ al lado. Se publica como artifact hecho a mano (index.html + sus archivos).
Usa el módulo markdown si está instalado; si no, un conversor sencillo incluido.
"""
import argparse
import html
import json
import os
import re
import shutil

IMG = {".svg", ".png", ".jpg", ".jpeg", ".webp", ".gif"}


def md_simple(texto):
    """Markdown básico: títulos, párrafos, listas, tablas, código, negrita, cursiva y enlaces."""
    def linea(t):
        t = html.escape(t, quote=False)
        t = re.sub(r"`([^`]+)`", r"<code>\1</code>", t)
        t = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<![*\w])\*([^*]+)\*(?!\w)", r"<em>\1</em>", t)
        t = re.sub(r"~~([^~]+)~~", r"<del>\1</del>", t)
        t = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', t)
        return t

    out, bloque, i = [], [], 0
    filas = texto.splitlines()

    def cerrar_parrafo():
        if bloque:
            out.append("<p>" + " ".join(linea(x) for x in bloque) + "</p>")
            bloque.clear()

    while i < len(filas):
        f = filas[i]
        if f.startswith("```"):
            cerrar_parrafo()
            j = i + 1
            codigo = []
            while j < len(filas) and not filas[j].startswith("```"):
                codigo.append(filas[j])
                j += 1
            out.append("<pre><code>" + html.escape("\n".join(codigo)) + "</code></pre>")
            i = j + 1
            continue
        m = re.match(r"(#{1,4})\s+(.*)", f)
        if m:
            cerrar_parrafo()
            n = len(m.group(1))
            out.append(f"<h{n}>{linea(m.group(2))}</h{n}>")
        elif f.strip().startswith("|") and i + 1 < len(filas) and re.match(r"\s*\|[\s:|-]+\|\s*$", filas[i + 1]):
            cerrar_parrafo()
            cab = [c.strip() for c in f.strip().strip("|").split("|")]
            out.append("<table><thead><tr>" + "".join(f"<th>{linea(c)}</th>" for c in cab) + "</tr></thead><tbody>")
            i += 2
            while i < len(filas) and filas[i].strip().startswith("|"):
                celdas = [c.strip() for c in filas[i].strip().strip("|").split("|")]
                out.append("<tr>" + "".join(f"<td>{linea(c)}</td>" for c in celdas) + "</tr>")
                i += 1
            out.append("</tbody></table>")
            continue
        elif re.match(r"\s*[-*]\s+", f) or re.match(r"\s*\d+\.\s+", f):
            cerrar_parrafo()
            ordenada = bool(re.match(r"\s*\d+\.\s+", f))
            etiqueta = "ol" if ordenada else "ul"
            items = []
            while i < len(filas) and (re.match(r"\s*[-*]\s+", filas[i]) or re.match(r"\s*\d+\.\s+", filas[i])):
                items.append(re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", filas[i]))
                i += 1
            out.append(f"<{etiqueta}>" + "".join(f"<li>{linea(x)}</li>" for x in items) + f"</{etiqueta}>")
            continue
        elif not f.strip():
            cerrar_parrafo()
        else:
            bloque.append(f.strip())
        i += 1
    cerrar_parrafo()
    return "\n".join(out)


def a_html(texto):
    try:
        import markdown
        return markdown.markdown(texto, extensions=["tables", "fenced_code"])
    except ImportError:
        return md_simple(texto)


def leer(ruta):
    return open(ruta, encoding="utf-8").read() if os.path.exists(ruta) else ""


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--project", required=True)
    p.add_argument("--salida", required=True)
    a = p.parse_args()

    tokens = json.loads(leer(os.path.join(a.project, "tokens.json")) or "{}")
    nombre = tokens.get("name", "Marca")
    os.makedirs(a.salida, exist_ok=True)
    for carpeta in ("assets", "fonts"):
        origen = os.path.join(a.project, carpeta)
        if os.path.isdir(origen):
            shutil.copytree(origen, os.path.join(a.salida, carpeta), dirs_exist_ok=True)

    color = tokens.get("color", {})
    temas = color.get("themes", []) or [{"id": "light", "name": "Claro"}]
    css_vars = {t["id"]: [] for t in temas}
    muestras = []
    for tok in color.get("tokens", []):
        v = tok.get("value")
        for t in temas:
            val = v.get(t["id"], v.get(temas[0]["id"])) if isinstance(v, dict) else v
            if isinstance(val, str) and val.startswith("{"):
                val = f"var(--{val[1:-1]})"
            css_vars[t["id"]].append(f"--{tok['name']}: {val};")
        valores = " · ".join(f"{t['name']}: {v.get(t['id'], '')}" for t in temas) if isinstance(v, dict) else v
        muestras.append(
            f'<div class="muestra"><div class="chip" style="background:var(--{tok["name"]})"></div>'
            f'<strong>{html.escape(tok["name"])}</strong><code>{html.escape(str(valores))}</code>'
            f'<span>{html.escape(tok.get("usage", ""))}</span></div>')
    fuentes = []
    tipo = tokens.get("type", {})
    for f in tipo.get("fonts", []):
        fuentes.append("@font-face{font-family:\"%s\";src:url(\"%s\");font-weight:%s;font-style:%s}"
                       % (f["family"], f["file"], f.get("weight", "400"), f.get("style", "normal")))
    familias = "".join(f"--font-{k}:{v};" for k, v in tipo.get("families", {}).items())
    escala = []
    for g in tipo.get("groups", []):
        for e in g.get("styles", []):
            estilo = (f"font-family:var(--font-{g.get('family', 'sans')});font-size:{e.get('fontSize')};"
                      f"line-height:{e.get('lineHeight')};font-weight:{e.get('fontWeight')};letter-spacing:{e.get('letterSpacing', 'normal')}")
            escala.append(f'<div class="estilo"><small>{html.escape(e["name"])} · {e.get("fontSize")}</small>'
                          f'<div style="{estilo}">{html.escape(e.get("sample", nombre))}</div></div>')
    galeria = []
    dir_assets = os.path.join(a.project, "assets")
    if os.path.isdir(dir_assets):
        for grupo in sorted(os.listdir(dir_assets)):
            ruta = os.path.join(dir_assets, grupo)
            if not os.path.isdir(ruta):
                continue
            nota = a_html(leer(os.path.join(ruta, "README.md")))
            piezas = []
            for n in sorted(os.listdir(ruta)):
                ext = os.path.splitext(n)[1].lower()
                if n == "README.md" or n.startswith("."):
                    continue
                href = f"assets/{grupo}/{n}"
                vista = f'<img src="{href}" alt="{html.escape(n)}" loading="lazy">' if ext in IMG else '<div class="doc">PDF</div>'
                piezas.append(f'<a class="pieza" href="{href}" download>{vista}<span>{html.escape(n)}</span></a>')
            galeria.append(f'<section><h2>{html.escape(grupo)}</h2>{nota}<div class="rejilla">{"".join(piezas)}</div></section>')

    secciones = [a_html(leer(os.path.join(a.project, "README.md")))]
    for extra in ("plataforma.md", "decisiones.md"):
        t = leer(os.path.join(a.project, extra))
        if t:
            secciones.append(a_html(t))
    principal = temas[0]["id"]
    bloques_tema = "".join(
        f'[data-theme="{t["id"]}"]{{{"".join(css_vars[t["id"]])}}}' for t in temas)
    botones = "".join(f'<button onclick="document.documentElement.dataset.theme=\'{t["id"]}\'">{html.escape(t["name"])}</button>'
                      for t in temas)
    pagina = f"""<!DOCTYPE html>
<html lang="es" data-theme="{principal}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(nombre)} · Libro de marca</title>
<style>
{"".join(fuentes)}
:root{{{familias}}}
{bloques_tema}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg,#fff);color:var(--ink,#111);font-family:var(--font-sans,system-ui,sans-serif);line-height:1.55}}
header{{display:flex;justify-content:space-between;align-items:center;gap:16px;padding:24px 40px;border-bottom:1px solid var(--border,#ddd);position:sticky;top:0;background:var(--bg,#fff)}}
header h1{{margin:0;font-family:var(--font-display,inherit);font-size:28px}}
header button{{font:inherit;padding:6px 14px;margin-left:6px;border:1px solid var(--border,#ccc);background:var(--surface,#fff);color:var(--ink,#111);border-radius:999px;cursor:pointer}}
main{{max-width:1100px;margin:0 auto;padding:40px}}
h1,h2,h3{{font-family:var(--font-display,inherit);line-height:1.1}}
h2{{margin-top:56px}}
table{{border-collapse:collapse;width:100%;margin:16px 0}}th,td{{border-bottom:1px solid var(--border,#ddd);padding:8px;text-align:left;vertical-align:top}}
code{{font-family:var(--font-mono,ui-monospace,monospace);font-size:.9em}}
pre{{background:var(--surface,#f5f5f5);padding:16px;overflow:auto;border-radius:8px}}
.muestras{{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:16px}}
.muestra{{display:flex;flex-direction:column;gap:4px;font-size:14px}}.muestra span{{color:var(--ink-muted,#666)}}
.chip{{height:72px;border-radius:8px;border:1px solid var(--border,#ddd)}}
.estilo{{padding:16px 0;border-bottom:1px solid var(--border,#ddd)}}.estilo small{{color:var(--ink-muted,#666);font-family:var(--font-mono,monospace)}}
.rejilla{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}}
.pieza{{display:flex;flex-direction:column;gap:8px;color:inherit;text-decoration:none;font-size:13px}}
.pieza img,.doc{{width:100%;aspect-ratio:4/3;object-fit:contain;background:repeating-conic-gradient(#0001 0 25%,#0000 0 50%) 0 0/16px 16px;border-radius:8px;border:1px solid var(--border,#ddd)}}
.doc{{display:grid;place-items:center;font-weight:600}}
</style>
</head>
<body>
<header><h1>{html.escape(nombre)}</h1><div>{botones}</div></header>
<main>
{''.join(f'<section>{s}</section>' for s in secciones)}
<section><h2>Colores</h2><div class="muestras">{''.join(muestras)}</div></section>
<section><h2>Escala tipográfica</h2>{''.join(escala)}</section>
<section><h2>Descargas</h2></section>
{''.join(galeria)}
</main>
</body>
</html>
"""
    with open(os.path.join(a.salida, "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina)
    total = sum(len(fs) for _, _, fs in os.walk(a.salida))
    print(f"✔ {a.salida}/index.html ({total} archivos en total, listos para publicar)")


if __name__ == "__main__":
    main()
