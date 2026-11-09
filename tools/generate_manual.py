#!/usr/bin/env python3
"""Genera el manual de usuario en Word y sus ilustraciones.

Uso (desde la carpeta del proyecto):

    .venv-build/bin/python tools/generate_manual.py

Requiere: python-docx y pillow (solo para generar el documento).
"""

from __future__ import annotations

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from manual_style import Manual  # noqa: E402
from manual_figures import make_cover, make_flow, make_general_ui  # noqa: E402
from manual_mockups import build_all  # noqa: E402
import manual_ch1  # noqa: E402
import manual_ch2  # noqa: E402
import manual_ch3  # noqa: E402
import manual_ch4  # noqa: E402

ASSETS = BASE / "docs" / "assets"
OUTPUT = BASE / "docs" / "Manual de Usuario - Investigación de Operaciones By Carlos Pardo.docx"


def build_assets() -> None:
    ASSETS.mkdir(parents=True, exist_ok=True)
    make_cover(ASSETS / "portada.png")
    make_flow(ASSETS / "flujo_trabajo.png")
    make_general_ui(ASSETS / "interfaz_general.png")
    build_all(ASSETS)


def main() -> None:
    print("Generando ilustraciones…")
    build_assets()

    print("Creando documento…")
    manual = Manual()
    manual_ch1.add_chapters(manual, ASSETS)
    manual_ch2.add_chapters(manual, ASSETS)
    manual_ch3.add_chapters(manual, ASSETS)
    manual_ch4.add_chapters(manual, ASSETS)

    print("Guardando…")
    manual.save(OUTPUT)
    size_mb = OUTPUT.stat().st_size / (1024 * 1024)
    print(f"Listo: {OUTPUT}")
    print(f"Tamaño: {size_mb:.2f} MB")
    print(f"Tablas: {manual.table_no} · Figuras: {manual.figure_no}")


if __name__ == "__main__":
    main()
