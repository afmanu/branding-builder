#!/usr/bin/env python3
"""Banners de perfil: catálogo de medidas, lote de renderizado, comprobación y simulación.

El catálogo vive en templates/piezas/banners-formatos.js (la misma fuente que usa banner.html).

Uso:
  python3 banners.py lista [--redes youtube,x,linkedin-perfil]
  python3 banners.py lote --redes youtube,x,linkedin-perfil --plantilla editables/banner.html \\
      --dir project/assets/Banners [--tamano whop=3000x640] [--param tema=dark] [--guias DIR] --salida lote.json
  python3 banners.py comprobar project/assets/Banners [--redes youtube,x] [--tamano whop=3000x640]
  python3 banners.py simular project/assets/Banners --salida expediente/banners-simulacion.png [--avatar <avatar.png>]

lote escribe un manifiesto para `render.py lote`. Con --guias DIR añade una copia de cada banner con las
zonas visibles en DIR (para revisar, no para entregar).
comprobar sale con código 1 si un archivo falta, no mide lo que dice su nombre o el catálogo, no tiene la
proporción de su red o pesa más de lo que admite la plataforma; avisa (sin fallar) de formatos por verificar,
pesos por encima de lo recomendado y detalle dentro de las zonas que tapa la interfaz.
simular dibuja cada banner con lo que recorta cada dispositivo y lo que tapa la interfaz (foto de perfil,
logo de la página…), con el avatar real si se da, para revisarlo de un vistazo.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CATALOGO = AQUI.parent / "templates" / "piezas" / "banners-formatos.js"


def cargar():
    texto = CATALOGO.read_text(encoding="utf-8")
    cuerpo = texto.split("=", 1)[1].strip().rstrip(";")
    return json.loads(cuerpo)


def tamanos(pares):
    salida = {}
    for p in pares or []:
        m = re.fullmatch(r"([\w-]+)=(\d+)x(\d+)", p.strip())
        if not m:
            sys.exit(f"--tamano mal escrito: {p} (forma: whop=3000x640)")
        salida[m.group(1)] = (int(m.group(2)), int(m.group(3)))
    return salida


def elegir(cat, redes):
    F = cat["formatos"]
    if not redes:
        return list(F)
    claves = [r.strip() for r in redes.split(",") if r.strip()]
    malas = [c for c in claves if c not in F]
    if malas:
        sys.exit("Formatos desconocidos: " + ", ".join(malas) + ". Mira `banners.py lista`.")
    return claves


def nombre_archivo(f, w, h):
    return f"{f['archivo']}_{w}x{h}.png"


def cmd_lista(a):
    cat = cargar()
    print(f"Catálogo revisado en {cat['revisado']}. Fiabilidad: oficial · medida · verificar · convencion\n")
    print(f"{'clave':17} {'red':10} {'pieza':32} {'tamaño':>11}  {'peso máx':>9}  fiabilidad")
    for c in elegir(cat, a.redes):
        f = cat["formatos"][c]
        peso = f"{f['peso_max'] / 1e6:.0f} MB" if f.get("peso_max") else "—"
        print(f"{c:17} {f['red']:10} {f['pieza']:32} {f['w']:>5}×{f['h']:<5}  {peso:>9}  {f['fiabilidad']}")
    print("\nArchivo: <archivo>_<ancho>x<alto>.png · grupo Banners (OG en Redes). Detalle y fuentes: banners-formatos.js")


def cmd_lote(a):
    cat = cargar()
    extra = tamanos(a.tamano)
    params = dict(p.split("=", 1) for p in (a.param or []))
    tareas = []
    for c in elegir(cat, a.redes):
        f = cat["formatos"][c]
        w, h = extra.get(c, (f["w"], f["h"]))
        if f["fiabilidad"] == "verificar" and c not in extra:
            print(f"Aviso: {c} es «verificar»: comprueba la pantalla de subida y, si difiere, pásalo con --tamano {c}=<W>x<H>.", file=sys.stderr)
        p = {"f": c, **params}
        if (w, h) != (f["w"], f["h"]):
            p.update({"w": str(w), "h": str(h)})
        grupo_dir = a.dir if f["grupo"] == "Banners" else os.path.join(os.path.dirname(a.dir.rstrip("/")), f["grupo"])
        # Rutas absolutas: render.py resuelve las relativas desde la carpeta del manifiesto.
        plantilla = os.path.abspath(a.plantilla)
        tareas.append({"entrada": plantilla, "salida": os.path.abspath(os.path.join(grupo_dir, nombre_archivo(f, w, h))), "ancho": w, "alto": h, "params": p})
        if a.guias:
            tareas.append({"entrada": plantilla, "salida": os.path.abspath(os.path.join(a.guias, f"{f['archivo']}-guias_{w}x{h}.png")),
                           "ancho": w, "alto": h, "params": {**p, "guias": "1"}})
    with open(a.salida, "w", encoding="utf-8") as fh:
        json.dump(tareas, fh, ensure_ascii=False, indent=1)
    print(f"✔ {a.salida}: {len(tareas)} renders. Siguiente: python3 render.py lote {a.salida}")


def detalle_en_zona(im, r):
    """Fracción de píxeles que se apartan del tono dominante de la zona (texto, logo o trama)."""
    x, y, w, h = [int(v) for v in r]
    x0, y0, x1, y1 = max(0, x), max(0, y), min(im.width, x + w), min(im.height, y + h)
    if x1 <= x0 or y1 <= y0:
        return 0.0
    zona = im.crop((x0, y0, x1, y1)).convert("L").resize((max(1, (x1 - x0) // 4), max(1, (y1 - y0) // 4)))
    datos = list(zona.tobytes())
    datos.sort()
    mediana = datos[len(datos) // 2]
    return sum(1 for v in datos if abs(v - mediana) > 40) / len(datos)


def indice_por_archivo(cat):
    return {f["archivo"]: (c, f) for c, f in cat["formatos"].items()}


def cmd_comprobar(a):
    try:
        from PIL import Image
    except ImportError:
        sys.exit("Falta Pillow (pip install pillow).")
    cat = cargar()
    extra = tamanos(a.tamano)
    por_archivo = indice_por_archivo(cat)
    errores, avisos, vistos = [], [], set()
    carpeta = Path(a.carpeta)
    for ruta in sorted(carpeta.glob("*")):
        if ruta.suffix.lower() not in (".png", ".jpg", ".jpeg"):
            continue
        m = re.fullmatch(r"(.+)_(\d+)x(\d+)", ruta.stem)
        if not m or m.group(1) not in por_archivo:
            avisos.append(f"{ruta.name}: no está en el catálogo (¿nombre <archivo>_<W>x<H>?).")
            continue
        c, f = por_archivo[m.group(1)]
        vistos.add(c)
        wn, hn = int(m.group(2)), int(m.group(3))
        im = Image.open(ruta)
        if im.size != (wn, hn):
            errores.append(f"{ruta.name}: mide {im.size[0]}×{im.size[1]}, no {wn}×{hn} como dice su nombre.")
        esperado = extra.get(c, (f["w"], f["h"]))
        if (wn, hn) != esperado:
            if abs(wn / hn - f["w"] / f["h"]) > 0.01 and c not in extra:
                errores.append(f"{ruta.name}: proporción {wn / hn:.2f}, {f['red']} espera {f['w'] / f['h']:.2f} ({f['w']}×{f['h']}). "
                               f"Si lo comprobaste en la plataforma, pásalo con --tamano {c}={wn}x{hn}.")
            else:
                avisos.append(f"{ruta.name}: tamaño distinto del catálogo ({f['w']}×{f['h']}).")
        if "minimo" in f and (wn < f["minimo"][0] or hn < f["minimo"][1]):
            errores.append(f"{ruta.name}: por debajo del mínimo de {f['red']} ({f['minimo'][0]}×{f['minimo'][1]}).")
        tipo = "jpg" if ruta.suffix.lower() in (".jpg", ".jpeg") else "png"
        if tipo not in f["tipos"]:
            errores.append(f"{ruta.name}: {f['red']} no admite {tipo}.")
        peso = ruta.stat().st_size
        if f.get("peso_max") and peso > f["peso_max"]:
            errores.append(f"{ruta.name}: pesa {peso / 1e6:.2f} MB y {f['red']} admite {f['peso_max'] / 1e6:.0f} MB.")
        elif f.get("peso_recomendado") and peso > f["peso_recomendado"]:
            avisos.append(f"{ruta.name}: pesa {peso / 1e3:.0f} KB; se recomiendan menos de {f['peso_recomendado'] / 1e3:.0f} KB (prueba en JPG).")
        if f["fiabilidad"] == "verificar":
            avisos.append(f"{ruta.name}: medida por verificar en la pantalla de subida de {f['red']}.")
        k = wn / f["w"]
        for t in f.get("tapado", []):
            frac = detalle_en_zona(im.convert("RGB"), [v * k for v in t[1:5]])
            if frac > 0.04:
                avisos.append(f"{ruta.name}: hay detalle ({frac:.0%}) en «{t[5]}»: ¿texto o logo que quedará tapado?")
    if a.redes:
        for c in elegir(cat, a.redes):
            if c not in vistos and cat["formatos"][c]["grupo"] == "Banners":
                errores.append(f"Falta el banner de {c} ({cat['formatos'][c]['archivo']}_<W>x<H>.png).")
    for e in errores:
        print("✘ " + e)
    for v in avisos:
        print("· " + v)
    print(f"{len(vistos)} banners revisados: {len(errores)} errores, {len(avisos)} avisos.")
    sys.exit(1 if errores else 0)


def cmd_simular(a):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        sys.exit("Falta Pillow (pip install pillow).")
    cat = cargar()
    por_archivo = indice_por_archivo(cat)
    ancho = a.ancho
    filas = []
    for ruta in sorted(Path(a.carpeta).glob("*.png")) + sorted(Path(a.carpeta).glob("*.jpg")):
        m = re.fullmatch(r"(.+)_(\d+)x(\d+)", ruta.stem)
        if m and m.group(1) in por_archivo:
            filas.append((ruta, *por_archivo[m.group(1)]))
    if not filas:
        sys.exit("No hay banners del catálogo en " + a.carpeta)
    orden = list(cat["formatos"])
    filas.sort(key=lambda t: orden.index(t[1]))
    avatar = Image.open(a.avatar).convert("RGBA") if a.avatar else None
    try:
        letra = ImageFont.truetype("DejaVuSans.ttf", 18)
    except OSError:
        letra = ImageFont.load_default()
    piezas = []
    for ruta, c, f in filas:
        im = Image.open(ruta).convert("RGBA")
        esc = ancho / im.width
        k = im.width / f["w"]
        vista = im.resize((ancho, round(im.height * esc)))
        capa = Image.new("RGBA", vista.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(capa)
        R = lambda r: [round(r[0] * k * esc), round(r[1] * k * esc), round((r[0] + r[2]) * k * esc), round((r[1] + r[3]) * k * esc)]
        for r in f.get("recortes", []):
            # Rayado claro y oscuro: se distingue igual sobre fondos negros que blancos.
            x0, y0, x1, y1 = R(r)
            if x1 <= x0 or y1 <= y0:
                continue
            trama = Image.new("RGBA", (x1 - x0, y1 - y0), (128, 128, 128, 90))
            dt = ImageDraw.Draw(trama)
            alto_t = y1 - y0
            for i in range(-alto_t, x1 - x0, 12):
                dt.line([i, alto_t, i + alto_t, 0], fill=(255, 255, 255, 110), width=3)
                dt.line([i + 6, alto_t, i + 6 + alto_t, 0], fill=(0, 0, 0, 90), width=3)
            capa.alpha_composite(trama, (x0, y0))
        for t in f.get("tapado", []):
            caja = R(t[1:5])
            if t[0] == "circulo" and avatar is not None:
                lado = caja[2] - caja[0]
                av = avatar.resize((lado, lado))
                mascara = Image.new("L", (lado, lado), 0)
                ImageDraw.Draw(mascara).ellipse([0, 0, lado - 1, lado - 1], fill=255)
                borde = max(2, lado // 40)
                ImageDraw.Draw(capa).ellipse([caja[0] - borde, caja[1] - borde, caja[2] + borde, caja[3] + borde], fill=(255, 255, 255, 255))
                capa.paste(av, (caja[0], caja[1]), mascara)
            elif t[0] == "circulo":
                d.ellipse(caja, fill=(255, 0, 170, 110), outline=(255, 0, 170, 255), width=3)
            else:
                d.rectangle(caja, fill=(255, 0, 170, 110), outline=(255, 0, 170, 255), width=3)
        s = R(f["seguro"])
        for i in range(s[0], s[2], 14):
            d.line([i, s[1], min(i + 7, s[2]), s[1]], fill=(0, 255, 255, 255), width=2)
            d.line([i, s[3], min(i + 7, s[2]), s[3]], fill=(0, 255, 255, 255), width=2)
        for j in range(s[1], s[3], 14):
            d.line([s[0], j, s[0], min(j + 7, s[3])], fill=(0, 255, 255, 255), width=2)
            d.line([s[2], j, s[2], min(j + 7, s[3])], fill=(0, 255, 255, 255), width=2)
        compuesto = Image.alpha_composite(vista, capa)
        titulo = f"{f['red']} · {f['pieza']} · {im.width}×{im.height} · {f['fiabilidad']}"
        lienzo = Image.new("RGB", (ancho, compuesto.height + 40), (245, 245, 245))
        ImageDraw.Draw(lienzo).text((0, 10), titulo, fill=(20, 20, 20), font=letra)
        lienzo.paste(compuesto.convert("RGB"), (0, 40))
        piezas.append(lienzo)
    alto = sum(p.height for p in piezas) + 30 * (len(piezas) + 1)
    hoja = Image.new("RGB", (ancho + 60, alto + 50), (245, 245, 245))
    ImageDraw.Draw(hoja).text((30, 14), "Rayado: se recorta · Magenta o avatar: lo tapa la interfaz · Cian: zona segura",
                              fill=(90, 90, 90), font=letra)
    y = 50
    for p in piezas:
        hoja.paste(p, (30, y))
        y += p.height + 30
    Path(a.salida).parent.mkdir(parents=True, exist_ok=True)
    hoja.save(a.salida)
    print(f"✔ {a.salida} ({len(piezas)} banners)")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("lista"); s.add_argument("--redes")
    s = sub.add_parser("lote")
    s.add_argument("--redes", required=True); s.add_argument("--plantilla", required=True); s.add_argument("--dir", required=True)
    s.add_argument("--tamano", action="append"); s.add_argument("--param", action="append"); s.add_argument("--guias")
    s.add_argument("--salida", required=True)
    s = sub.add_parser("comprobar"); s.add_argument("carpeta"); s.add_argument("--redes"); s.add_argument("--tamano", action="append")
    s = sub.add_parser("simular"); s.add_argument("carpeta"); s.add_argument("--salida", required=True)
    s.add_argument("--avatar"); s.add_argument("--ancho", type=int, default=1200)
    a = p.parse_args()
    {"lista": cmd_lista, "lote": cmd_lote, "comprobar": cmd_comprobar, "simular": cmd_simular}[a.cmd](a)


if __name__ == "__main__":
    main()
