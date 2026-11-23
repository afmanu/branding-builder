#!/usr/bin/env python3
"""Calcula el contraste WCAG de los colores de una marca.

Uso:
  python3 contraste.py "#0a0a0b" "#ffffff"                 # una pareja
  python3 contraste.py --tokens project/tokens.json         # parejas semánticas en cada tema
  python3 contraste.py --tokens project/tokens.json --par acento bg 3
  añade --json para obtener el resultado en JSON

Umbrales: texto 4,5:1 (3:1 a 24 px o más), iconos y bordes de controles 3:1.
Sale con código 1 si alguna pareja obligatoria no pasa.
"""
import json
import re
import sys

PAREJAS = [
    ("ink", "bg", 4.5, "Texto principal sobre el fondo"),
    ("ink", "surface", 4.5, "Texto principal sobre tarjetas"),
    ("ink-muted", "bg", 4.5, "Texto secundario sobre el fondo"),
    ("ink-muted", "surface", 4.5, "Texto secundario sobre tarjetas"),
    ("on-action", "action", 4.5, "Texto sobre botones"),
    ("action", "bg", 3.0, "Botón frente al fondo"),
    ("border", "bg", None, "Bordes: 3:1 si delimitan controles; menos vale solo para divisores"),
]


def a_rgb(valor):
    v = valor.strip().lower()
    m = re.fullmatch(r"#([0-9a-f]{3,8})", v)
    if m:
        h = m.group(1)
        if len(h) in (3, 4):
            h = "".join(c * 2 for c in h[:3])
        if len(h) not in (6, 8):
            raise ValueError(f"HEX no válido: {valor}")
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
    m = re.fullmatch(r"rgba?\(([^)]+)\)", v)
    if m:
        partes = [p.strip() for p in re.split(r"[ ,/]+", m.group(1)) if p.strip()]
        return tuple(int(float(p.rstrip("%")) * (2.55 if p.endswith("%") else 1)) for p in partes[:3])
    raise ValueError(f"Formato no soportado (usa HEX o rgb()): {valor}")


def luminancia(rgb):
    c = [x / 255 for x in rgb]
    c = [x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4 for x in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]


def ratio(a, b):
    la, lb = sorted([luminancia(a_rgb(a)), luminancia(a_rgb(b))], reverse=True)
    return (la + 0.05) / (lb + 0.05)


def valores_por_tema(tokens):
    color = tokens.get("color", {})
    temas = [t["id"] for t in color.get("themes", [])] or ["light"]
    crudos = {t["name"]: t.get("value") for t in color.get("tokens", [])}

    def resolver(nombre, tema, visitados=()):
        v = crudos.get(nombre)
        if v is None:
            return None
        if isinstance(v, dict):
            v = v.get(tema, v.get(temas[0]))
        if isinstance(v, str) and v.startswith("{") and v.endswith("}"):
            destino = v[1:-1]
            if destino in visitados:
                return None
            return resolver(destino, tema, visitados + (nombre,))
        return v

    return temas, {tema: {n: resolver(n, tema) for n in crudos} for tema in temas}


def analizar(ruta, extra):
    with open(ruta, encoding="utf-8") as f:
        tokens = json.load(f)
    temas, valores = valores_por_tema(tokens)
    resultados = []
    for tema in temas:
        for fg, bg, umbral, uso in PAREJAS + extra:
            a, b = valores[tema].get(fg), valores[tema].get(bg)
            if not a or not b:
                continue
            try:
                r = ratio(a, b)
            except ValueError as exc:
                resultados.append({"tema": tema, "par": f"{fg}/{bg}", "error": str(exc)})
                continue
            ok = None if umbral is None else r >= umbral
            resultados.append({
                "tema": tema, "par": f"{fg} sobre {bg}", "colores": [a, b],
                "ratio": round(r, 2), "umbral": umbral, "ok": ok, "uso": uso,
            })
    return resultados


def main():
    args = sys.argv[1:]
    como_json = "--json" in args
    args = [a for a in args if a != "--json"]
    if args and args[0] == "--tokens":
        ruta = args[1]
        extra = []
        resto = args[2:]
        while resto and resto[0] == "--par":
            extra.append((resto[1], resto[2], float(resto[3]), "Pareja añadida"))
            resto = resto[4:]
        res = analizar(ruta, extra)
        if como_json:
            print(json.dumps(res, ensure_ascii=False, indent=2))
        else:
            for r in res:
                if "error" in r:
                    print(f"[{r['tema']}] {r['par']}: {r['error']}")
                    continue
                estado = "—" if r["ok"] is None else ("✔" if r["ok"] else "✘")
                umbral = "" if r["umbral"] is None else f" (mín. {r['umbral']}:1)"
                print(f"{estado} [{r['tema']}] {r['par']}: {r['ratio']}:1{umbral} · {r['uso']}")
        sys.exit(1 if any(r.get("ok") is False for r in res) else 0)
    if len(args) == 2:
        r = ratio(args[0], args[1])
        if como_json:
            print(json.dumps({"ratio": round(r, 2), "texto": r >= 4.5, "texto_grande_o_iconos": r >= 3}))
        else:
            print(f"{r:.2f}:1 · texto {'✔' if r >= 4.5 else '✘'} · texto grande e iconos {'✔' if r >= 3 else '✘'}")
        return
    print(__doc__)
    sys.exit(1)


if __name__ == "__main__":
    main()
