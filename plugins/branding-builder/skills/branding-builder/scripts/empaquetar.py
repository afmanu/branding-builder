#!/usr/bin/env python3
"""Empaqueta el kit en un ZIP para entregarlo fuera del artifact.

Uso:
  python3 empaquetar.py --kit <marca>-kit --sigla ACME [--salida <marca>-kit/extra/ACME-brand-kit.zip]

Incluye: assets/, fonts/, editables/, favicon.ico (de extra/), README.md, plataforma.md,
decisiones.md y tokens.json. Deja fuera expediente/, archivos ocultos y temporales.
"""
import argparse
import os
import zipfile

EXCLUIR = {".DS_Store", "Thumbs.db", "__pycache__"}


def anadir(z, ruta, destino):
    if os.path.isfile(ruta):
        z.write(ruta, destino)
        return 1
    n = 0
    for raiz, dirs, archivos in os.walk(ruta):
        dirs[:] = [d for d in dirs if d not in EXCLUIR and not d.startswith(".")]
        for a in archivos:
            if a in EXCLUIR or a.startswith("."):
                continue
            completo = os.path.join(raiz, a)
            z.write(completo, os.path.join(destino, os.path.relpath(completo, ruta)))
            n += 1
    return n


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--kit", required=True)
    p.add_argument("--sigla", required=True)
    p.add_argument("--salida")
    a = p.parse_args()
    salida = a.salida or os.path.join(a.kit, "extra", f"{a.sigla}-brand-kit.zip")
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    proyecto = os.path.join(a.kit, "project")
    piezas = [
        (os.path.join(proyecto, "assets"), "assets"),
        (os.path.join(proyecto, "fonts"), "fonts"),
        (os.path.join(a.kit, "editables"), "editables"),
        (os.path.join(a.kit, "extra", "favicon.ico"), "assets/Iconos/favicon.ico"),
    ] + [(os.path.join(proyecto, n), n) for n in ("README.md", "plataforma.md", "decisiones.md", "tokens.json")]
    total = 0
    faltan = []
    with zipfile.ZipFile(salida, "w", zipfile.ZIP_DEFLATED) as z:
        for origen, destino in piezas:
            if os.path.exists(origen):
                total += anadir(z, origen, destino)
            elif destino in ("assets", "fonts", "README.md", "tokens.json", "assets/Iconos/favicon.ico"):
                faltan.append(destino)
    print(f"✔ {salida}: {total} archivos, {os.path.getsize(salida) // 1024} KB")
    if faltan:
        print("Aviso: no se encontró " + ", ".join(faltan))


if __name__ == "__main__":
    main()
