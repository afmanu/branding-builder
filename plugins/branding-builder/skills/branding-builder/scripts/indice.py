#!/usr/bin/env python3
"""Construye project/design-system.json (el índice del Design System) a partir de los assets subidos.

Uso (sistema nuevo):
  python3 indice.py --project <kit>/project --blobs blobs.json --titulo "Acme Estudio" \
      --autor "Nombre" --nota "v1.0: primera versión del sistema."
Uso (revisión de un sistema publicado):
  python3 indice.py --project <kit>/project --blobs blobs.json --existente design-system-leido.json \
      --autor "Nombre" --nota "v1.1: añadidos colores de acento."

blobs.json relaciona cada archivo de project/assets/ con lo que devolvió la subida:
  {"Logos/ACME-logo-negro.svg": "/_blob/2e1c…", "Iconos/favicon.svg": "43ff…"}
Acepta la URL /_blob/<id> o solo el id.

Comprueba que cada archivo binario de assets/ tiene su subida (si no, sale con código 1; usa
--permitir-pendientes para generar igualmente un borrador). Con --existente conserva todas las claves,
el título y el orden del índice leído, y añade al final de cada grupo lo nuevo.
"""
import argparse
import datetime as dt
import json
import mimetypes
import os
import re
import sys

ORDEN_GRUPOS = ["Logos", "Iconos", "Redes", "Banners", "Patrones", "Mockups", "Manual", "Papeleria", "Presentaciones", "OnePager"]
TESELAS = {"Logos": "l", "Iconos": "m", "Redes": "l", "Banners": "l", "Patrones": "m", "Mockups": "l", "Manual": "s",
           "Papeleria": "m", "Presentaciones": "l", "OnePager": "m"}
RANGOS = {
    "Logos": [r"-logo-[^-_.]+\.svg$", r"-logo-[^-_.]+_\d+px\.png$", r"-logo-.+-sobre-.+\.svg$", r"-construccion\.svg$",
              r"-lockup-horizontal-sobre-", r"-lockup-horizontal-", r"-lockup-vertical-"],
    "Iconos": [r"-app-icon-[^_]+\.svg$", r"^favicon\.svg$", r"-app-icon-.+_1024\.png$", r"^apple-touch-icon", r"^android-chrome"],
    "Redes": [r"^avatar-", r"^Instagram-post-", r"^Instagram-story", r"^YouTube-miniatura", r"^OG-",
              r"^X-", r"^YouTube-", r"^LinkedIn-"],
    "Banners": [r"^YouTube-banner", r"^X-cabecera", r"^LinkedIn-perfil", r"^LinkedIn-pagina", r"^Facebook-portada",
                r"^Facebook-grupo", r"^Bluesky-", r"^Twitch-", r"^Discord-", r"^Skool-", r"^Whop-", r"^Pinterest-",
                r"^Newsletter-"],
    "Patrones": [r"-patron-(?!logos).+\.svg$", r"-patron-(?!logos).+_\d+\.png$", r"-patron-logos-", r"-fondo-.+_1920x1080\.png$"],
    "Mockups": [r"^mockup-", r"^tarjeta-visita-anverso", r"^tarjeta-visita-reverso"],
    "Manual": [r"\.pdf$"],
    "OnePager": [r"-one-pager-.+\.pdf$", r"-one-pager-.+_preview\.png$"],
}
TEXTO = {".md", ".json", ".csv", ".txt", ".js", ".css"}
EXTRA_MIME = {".svg": "image/svg+xml", ".woff2": "font/woff2", ".woff": "font/woff", ".webp": "image/webp"}


def ahora():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def clave(nombre):
    salida = []
    for car in nombre:
        if re.fullmatch(r"[A-Za-z0-9_./-]", car):
            salida.append(car)
        else:
            salida.extend("~%02x" % b for b in car.encode("utf-8"))
    return "".join(salida)


def tipo(nombre):
    ext = os.path.splitext(nombre)[1].lower()
    return EXTRA_MIME.get(ext) or mimetypes.guess_type(nombre)[0] or "application/octet-stream"


def rango(grupo, nombre):
    for i, patron in enumerate(RANGOS.get(grupo, [])):
        if re.search(patron, nombre):
            return i
    return len(RANGOS.get(grupo, []))


def id_blob(valor):
    if isinstance(valor, dict):
        valor = valor.get("blob") or valor.get("url") or ""
    m = re.search(r"/_blob/([^/?#]+)", valor)
    return m.group(1) if m else valor.strip()


def espacio_de_nombres(titulo):
    partes = re.findall(r"[A-Za-z0-9]+", titulo)
    ns = "".join(p[:1].upper() + p[1:] for p in partes) or "Marca"
    return ns if ns[0].isalpha() else "M" + ns


def escanear(dir_assets):
    grupos = {}
    for grupo in sorted(os.listdir(dir_assets)):
        ruta = os.path.join(dir_assets, grupo)
        if not os.path.isdir(ruta) or grupo.startswith("."):
            continue
        archivos = []
        for raiz, _, nombres in os.walk(ruta):
            for n in nombres:
                if n.startswith(".") or os.path.splitext(n)[1].lower() in TEXTO:
                    continue
                completo = os.path.join(raiz, n)
                archivos.append(os.path.relpath(completo, ruta).replace(os.sep, "/"))
        grupos[grupo] = archivos
    return grupos


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--project", required=True)
    p.add_argument("--blobs", required=True)
    p.add_argument("--titulo")
    p.add_argument("--existente")
    p.add_argument("--autor", default="Claude")
    p.add_argument("--via", default="Claude (chat)")
    p.add_argument("--nota", default="v1.0: primera versión del sistema.")
    p.add_argument("--salida")
    p.add_argument("--permitir-pendientes", action="store_true")
    a = p.parse_args()

    dir_assets = os.path.join(a.project, "assets")
    with open(a.blobs, encoding="utf-8") as f:
        blobs = {k.replace("\\", "/").removeprefix("assets/"): id_blob(v) for k, v in json.load(f).items()}
    encontrados = escanear(dir_assets)

    if a.existente:
        with open(a.existente, encoding="utf-8") as f:
            indice = json.load(f)
        if not (indice.get("createdOnFiles") or indice.get("convertedFrom")):
            sys.exit("El índice leído no tiene la marca createdOnFiles/convertedFrom: no es un índice válido. No se escribe nada.")
        if a.titulo and a.titulo != indice.get("title"):
            print(f"Aviso: se conserva el título existente «{indice.get('title')}».", file=sys.stderr)
    else:
        if not a.titulo:
            sys.exit("Falta --titulo para un sistema nuevo.")
        indice = {
            "v": 3, "layout": "files", "createdOnFiles": {"v": 1, "at": ahora()},
            "title": a.titulo, "namespace": espacio_de_nombres(a.titulo), "libraries": [],
            "sections": {}, "groups": [], "assetGroups": {}, "blobs": {},
            "docs": {"readme": "project/README.md", "sections": []},
        }

    pendientes = []
    grupos_idx = indice.setdefault("assetGroups", {})
    for grupo, archivos in encontrados.items():
        if not archivos and grupo not in grupos_idx:
            continue  # un grupo sin archivos no se publica
        g = grupos_idx.setdefault(grupo, {"name": grupo, "tile": TESELAS.get(grupo, "m"), "order": [], "files": {}})
        orden_previo = list(g.get("order", []))
        nuevos = []
        for nombre in sorted(archivos, key=lambda n: (rango(grupo, n), n.lower())):
            k = clave(nombre)
            ruta = os.path.join(dir_assets, grupo, nombre)
            blob = blobs.get(f"{grupo}/{nombre}")
            if blob:
                g["files"][k] = {"name": nombre, "blob": blob, "size": os.path.getsize(ruta), "type": tipo(nombre)}
            elif k not in g["files"]:
                pendientes.append(f"{grupo}/{nombre}")
                continue
            if nombre not in orden_previo:
                nuevos.append(nombre)
        g["order"] = orden_previo + nuevos
        g["order"] = [n for n in g["order"] if clave(n) in g["files"]]

    grupos = list(indice.get("groups", []))
    for grupo in ORDEN_GRUPOS + sorted(encontrados):
        if grupo in grupos_idx and grupo not in grupos:
            # Un grupo nuevo del plano (p. ej. Banners en un kit anterior) va tras el anterior que ya exista.
            previos = ORDEN_GRUPOS[:ORDEN_GRUPOS.index(grupo)] if grupo in ORDEN_GRUPOS else []
            pos = max([grupos.index(g) + 1 for g in previos if g in grupos], default=len(grupos) if not previos else 0)
            grupos.insert(pos, grupo)
    indice["groups"] = grupos
    indice["lastChange"] = {"by": a.autor, "at": ahora(), "via": a.via, "note": a.nota}

    sobrantes = [k for k in blobs if k.split("/", 1)[0] not in encontrados or
                 k.split("/", 1)[1] not in encontrados.get(k.split("/", 1)[0], [])]
    for s in sobrantes:
        print(f"Aviso: {s} está en blobs.json pero no existe en assets/.", file=sys.stderr)
    if pendientes:
        print("Falta subir: " + ", ".join(pendientes), file=sys.stderr)
        if not a.permitir_pendientes:
            sys.exit(1)

    salida = a.salida or os.path.join(a.project, "design-system.json")
    with open(salida, "w", encoding="utf-8") as f:
        json.dump(indice, f, ensure_ascii=False, indent=1)
        f.write("\n")
    total = sum(len(g["order"]) for g in grupos_idx.values())
    print(f"✔ {salida}: {len(grupos)} grupos, {total} assets" + (f", {len(pendientes)} pendientes" if pendientes else ""))


if __name__ == "__main__":
    main()
