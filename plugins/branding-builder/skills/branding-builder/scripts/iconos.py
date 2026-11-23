#!/usr/bin/env python3
"""Iconos derivados a partir de un icono cuadrado a sangre de 1024 px (sin esquinas redondeadas).

Uso:
  python3 iconos.py derivar <cuadrado_1024.png> --dir project/assets/Iconos --ico extra/favicon.ico
        → apple-touch-icon.png (180), android-chrome-512x512.png y favicon.ico (16, 32, 48)
  python3 iconos.py esquinas <cuadrado_1024.png> <salida_1024.png> [--radio 0.2237]
        → mismo icono con esquinas redondeadas al 22,37% y fondo transparente
  python3 iconos.py ico <imagen.png> <salida.ico>

iOS y Android aplican su propia máscara: apple-touch-icon y android-chrome van cuadrados, sin transparencia.
"""
import argparse
import os
import sys


def requiere_pillow():
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        sys.exit("Falta Pillow: pip install pillow")


def abrir(ruta):
    from PIL import Image
    img = Image.open(ruta).convert("RGBA")
    if img.width != img.height:
        sys.exit(f"{ruta} no es cuadrado ({img.width}×{img.height}).")
    return img


def guardar_ico(img, destino):
    os.makedirs(os.path.dirname(os.path.abspath(destino)), exist_ok=True)
    img.save(destino, format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print(f"✔ {destino} (16, 32, 48)")


def derivar(a):
    from PIL import Image
    img = abrir(a.origen)
    plano = Image.new("RGB", img.size, (255, 255, 255))
    plano.paste(img, mask=img.split()[3])
    os.makedirs(a.dir, exist_ok=True)
    for nombre, lado in (("apple-touch-icon.png", 180), ("android-chrome-512x512.png", 512)):
        destino = os.path.join(a.dir, nombre)
        plano.resize((lado, lado), Image.LANCZOS).save(destino, optimize=True)
        print(f"✔ {destino} ({lado}×{lado})")
    if a.ico:
        guardar_ico(img, a.ico)


def esquinas(a):
    from PIL import Image, ImageDraw
    img = abrir(a.origen)
    f = 4
    grande = (img.width * f, img.height * f)
    mascara = Image.new("L", grande, 0)
    ImageDraw.Draw(mascara).rounded_rectangle([0, 0, grande[0] - 1, grande[1] - 1],
                                              radius=round(grande[0] * a.radio), fill=255)
    mascara = mascara.resize(img.size, Image.LANCZOS)
    alfa = Image.composite(img.split()[3], Image.new("L", img.size, 0), mascara)
    img.putalpha(alfa)
    os.makedirs(os.path.dirname(os.path.abspath(a.salida)), exist_ok=True)
    img.save(a.salida, optimize=True)
    print(f"✔ {a.salida} (esquinas al {a.radio * 100:.2f}%)")


def main():
    requiere_pillow()
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sp = p.add_subparsers(dest="cmd", required=True)
    d = sp.add_parser("derivar")
    d.add_argument("origen")
    d.add_argument("--dir", required=True)
    d.add_argument("--ico")
    e = sp.add_parser("esquinas")
    e.add_argument("origen")
    e.add_argument("salida")
    e.add_argument("--radio", type=float, default=0.2237)
    i = sp.add_parser("ico")
    i.add_argument("origen")
    i.add_argument("salida")
    a = p.parse_args()
    if a.cmd == "derivar":
        derivar(a)
    elif a.cmd == "esquinas":
        esquinas(a)
    else:
        from PIL import Image
        guardar_ico(Image.open(a.origen).convert("RGBA"), a.salida)


if __name__ == "__main__":
    main()
