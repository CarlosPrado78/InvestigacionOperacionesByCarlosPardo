#!/usr/bin/env python3
"""Renombra el .exe de Windows al nombre visible de la aplicación.

El nombre se escribe en este archivo UTF-8, por lo que no depende de la
codificación de la consola (cmd, PowerShell o GitHub Actions).
"""
import os
import sys

OLD = os.path.join("dist", "InvestigacionOperaciones.exe")
NEW = os.path.join("dist", "Investigación de Operaciones By Carlos Pardo.exe")


def main() -> int:
    if not os.path.exists(OLD):
        print(f"No se encontro: {OLD}", file=sys.stderr)
        return 1
    os.replace(OLD, NEW)
    print("Listo:", NEW)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
