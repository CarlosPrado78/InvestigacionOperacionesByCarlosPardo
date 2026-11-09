"""Mockups de cada módulo para el manual.

No son capturas reales: son reconstrucciones a escala de la interfaz con los
datos de los ejemplos del manual, para que el lector reconozca cada pantalla.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from manual_figures import (
    AMBER,
    BG,
    BLUE,
    BORDER,
    CYAN,
    GREEN,
    MUTED,
    NAVY,
    NAVY_2,
    PANEL,
    RED,
    TEXT,
    W,
    font,
    mono,
    text_width,
)

TABS = [
    "Inicio",
    "Método gráfico",
    "Simplex",
    "Transporte",
    "Asignación",
    "Colas",
    "Markov",
    "PERT / CPM",
    "Inventarios",
]


def _draw_tabs(draw: ImageDraw.ImageDraw, active: str, x0: int, y0: int, width: int) -> None:
    x = x0
    for tab in TABS:
        tw = text_width(draw, tab, font(23)) + 46
        is_active = tab == active
        if is_active:
            draw.rounded_rectangle([x, y0, x + tw, y0 + 50], radius=9, fill=PANEL, outline=BORDER, width=2)
            draw.rounded_rectangle([x + 10, y0 + 43, x + tw - 10, y0 + 47], radius=2, fill=BLUE)
            color = BLUE
        else:
            draw.rounded_rectangle([x, y0, x + tw, y0 + 50], radius=9, fill=(223, 231, 242))
            color = (51, 71, 91)
        draw.text((x + 22, y0 + 11), tab, font=font(23, is_active), fill=color)
        x += tw + 7
        if x > x0 + width - 60:
            break


def _entry(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, value: str, h: int = 52) -> None:
    draw.rounded_rectangle([x, y, x + w, y + h], radius=7, fill=PANEL, outline=BORDER, width=2)
    draw.text((x + 16, y + (h - 30) // 2 - 2), value, font=font(25), fill=TEXT)


def _textarea(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, h: int, lines: list[str]) -> None:
    draw.rounded_rectangle([x, y, x + w, y + h], radius=9, fill=(251, 252, 254), outline=BORDER, width=2)
    for i, line in enumerate(lines):
        draw.text((x + 20, y + 18 + i * 42), line, font=mono(26), fill=TEXT)


def _checkbox(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, checked: bool = False) -> None:
    draw.rounded_rectangle([x, y, x + 26, y + 26], radius=5, fill=PANEL, outline=(140, 158, 177), width=2)
    if checked:
        draw.line([(x + 6, y + 14), (x + 12, y + 20), (x + 21, y + 6)], fill=BLUE, width=4)
    draw.text((x + 38, y - 4), label, font=font(24), fill=TEXT)


def _radio(draw: ImageDraw.ImageDraw, x: int, y: int, label: str, selected: bool) -> None:
    draw.ellipse([x, y, x + 26, y + 26], outline=BLUE, width=3)
    if selected:
        draw.ellipse([x + 6, y + 6, x + 20, y + 20], fill=BLUE)
    draw.text((x + 38, y - 4), label, font=font(24), fill=TEXT)


def _combo(draw: ImageDraw.ImageDraw, x: int, y: int, w: int, value: str) -> None:
    draw.rounded_rectangle([x, y, x + w, y + 50], radius=7, fill=PANEL, outline=BORDER, width=2)
    draw.text((x + 16, y + 9), value, font=font(24), fill=TEXT)
    draw.polygon([(x + w - 30, y + 20), (x + w - 14, y + 20), (x + w - 22, y + 30)], fill=MUTED)


def _result_text(draw: ImageDraw.ImageDraw, x: int, y: int, lines: list[tuple[str, str]], max_width: int) -> None:
    for raw, kind in lines:
        color = {"h": BLUE, "ok": GREEN, "warn": AMBER, "err": RED}.get(kind, TEXT)
        bold = kind in ("h", "ok", "warn", "err")
        draw.text((x, y), raw, font=mono(25, bold), fill=color)
        y += 41


def _mini_plot(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle([x0, y0, x1, y1], radius=10, fill=(253, 254, 255), outline=BORDER, width=2)

    def px(x: float) -> float:
        return x0 + 52 + x / 5.2 * (x1 - x0 - 90)

    def py(y: float) -> float:
        return y1 - 46 - y / 7.5 * (y1 - y0 - 80)

    for i in range(1, 6):
        gx = x0 + 52 + i / 4.4 * (x1 - x0 - 90)
        gy = y1 - 46 - i / 4.4 * (y1 - y0 - 80)
        draw.line([(gx, py(0)), (gx, py(7.5))], fill=(231, 237, 245), width=2)
        draw.line([(px(0), gy), (px(5.2), gy)], fill=(231, 237, 245), width=2)
    draw.line([(px(0), py(0)), (px(5.2), py(0))], fill=(70, 88, 107), width=3)
    draw.line([(px(0), py(0)), (px(0), py(7.5))], fill=(70, 88, 107), width=3)
    draw.text((px(5.2) - 20, py(0) + 12), "x1", font=font(22, True), fill=(51, 71, 91))
    draw.text((px(0) - 36, py(7.5) - 10), "x2", font=font(22, True), fill=(51, 71, 91))

    polygon = [(0, 0), (4, 0), (4, 3), (2, 6), (0, 6)]
    points = [(px(x), py(y)) for x, y in polygon]
    draw.polygon(points, fill=(217, 242, 229), outline=(46, 139, 87), width=2)
    # restricciones
    draw.line([(px(0), py(6)), (px(5.2), py(6))], fill=(192, 57, 43), width=3)
    draw.line([(px(4), py(0)), (px(4), py(7.5))], fill=(36, 113, 163), width=3)
    draw.line([(px(0), py(9)), (px(3.1), py(0))], fill=(142, 68, 173), width=3)
    # objetivo
    draw.line([(px(0), py(12)), (px(5.2), py(1.2))], fill=RED, width=3)
    for x, y in polygon[1:]:
        draw.ellipse([px(x) - 5, py(y) - 5, px(x) + 5, py(y) + 5], fill=(36, 113, 163))
    draw.ellipse([px(2) - 10, py(6) - 10, px(2) + 10, py(6) + 10], fill=RED, outline="white", width=3)
    draw.text((px(2) + 16, py(6) - 34), "Óptimo (2, 6)", font=font(22, True), fill=RED)


def make_module(path: Path, config: dict) -> None:
    width, height = W, 1500
    img = Image.new("RGB", (width, height), (247, 250, 253))
    draw = ImageDraw.Draw(img)

    draw.text((80, 34), config.get("figure_title", ""), font=font(42, True), fill=NAVY)
    draw.text((80, 92), config.get("figure_subtitle", ""), font=font(26), fill=MUTED)

    wx0, wy0, wx1, wy1 = 80, 160, 2320, 1420
    draw.rounded_rectangle([wx0 + 8, wy0 + 10, wx1 + 8, wy1 + 10], radius=20, fill=(220, 228, 238))
    draw.rounded_rectangle([wx0, wy0, wx1, wy1], radius=20, fill=PANEL, outline=BORDER, width=3)
    draw.rounded_rectangle([wx0, wy0, wx1, wy0 + 58], radius=20, fill=(232, 238, 246))
    draw.rectangle([wx0, wy0 + 38, wx1, wy0 + 58], fill=(232, 238, 246))
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = wx0 + 24 + i * 27
        draw.ellipse([cx, wy0 + 19, cx + 16, wy0 + 35], fill=color)
    draw.text((wx0 + 430, wy0 + 14), "Investigación de Operaciones By Carlos Pardo · Solucionador",
              font=font(24, True), fill=TEXT)

    _draw_tabs(draw, config["active"], wx0 + 22, wy0 + 76, wx1 - wx0 - 44)

    lx0, ly0, lx1, ly1 = wx0 + 30, wy0 + 160, wx0 + 900, wy1 - 92
    draw.rounded_rectangle([lx0, ly0, lx1, ly1], radius=12, fill=(250, 252, 255), outline=BORDER, width=2)
    rx0, ry0, rx1, ry1 = lx1 + 28, ly0, wx1 - 30, ly1
    draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=12, fill=PANEL, outline=BORDER, width=2)

    # Contenido del panel izquierdo
    y = ly0 + 26
    for item in config["fields"]:
        kind = item["type"]
        if kind == "section":
            draw.text((lx0 + 26, y), item["text"], font=font(26, True), fill=NAVY)
            y += 44
        elif kind == "hint":
            for line in item["text"]:
                draw.text((lx0 + 26, y), line, font=font(21), fill=MUTED)
                y += 30
        elif kind == "label":
            draw.text((lx0 + 26, y + 4), item["text"], font=font(23), fill=TEXT)
            y += 36
            _entry(draw, lx0 + 26, y, lx1 - lx0 - 52, item["value"])
            y += 66
        elif kind == "entry":
            _entry(draw, lx0 + 26, y, lx1 - lx0 - 52, item["value"])
            y += 66
        elif kind == "combo":
            _combo(draw, lx0 + 26, y, lx1 - lx0 - 52, item["value"])
            y += 64
        elif kind == "text":
            _textarea(draw, lx0 + 26, y, lx1 - lx0 - 52, item.get("h", 160), item["lines"])
            y += item.get("h", 160) + 18
        elif kind == "check":
            _checkbox(draw, lx0 + 26, y, item["text"], item.get("checked", False))
            y += 42
        elif kind == "radio":
            xx = lx0 + 26
            for label, selected in item["options"]:
                _radio(draw, xx, y, label, selected)
                xx += text_width(draw, label, font(24)) + 80
            y += 44
        elif kind == "gap":
            y += item.get("h", 10)

    # Botones del panel izquierdo
    by = ly1 - 82
    draw.rounded_rectangle([lx0 + 26, by, lx0 + 300, by + 58], radius=9, fill=BLUE)
    draw.text((lx0 + 112, by + 13), "Resolver", font=font(26, True), fill="white")
    draw.rounded_rectangle([lx0 + 318, by, lx0 + 476, by + 58], radius=9, fill=(230, 236, 244), outline=BORDER, width=2)
    draw.text((lx0 + 358, by + 13), "Ejemplo", font=font(24), fill=TEXT)
    draw.rounded_rectangle([lx0 + 494, by, lx0 + 652, by + 58], radius=9, fill=(230, 236, 244), outline=BORDER, width=2)
    draw.text((lx0 + 534, by + 13), "Limpiar", font=font(24), fill=TEXT)

    # Panel de resultados
    draw.text((rx0 + 24, ry0 + 18), "Resultados", font=font(25, True), fill=TEXT)
    draw.rounded_rectangle([rx1 - 190, ry0 + 12, rx1 - 22, ry0 + 56], radius=8, fill=(230, 236, 244), outline=BORDER, width=2)
    draw.text((rx1 - 170, ry0 + 21), "Guardar .txt", font=font(21), fill=TEXT)
    if config.get("plot"):
        _mini_plot(draw, (rx0 + 24, ry0 + 72, rx1 - 24, ry0 + 640))
        _result_text(draw, rx0 + 28, ry0 + 666, config["results"], rx1 - rx0 - 56)
    else:
        _result_text(draw, rx0 + 28, ry0 + 82, config["results"], rx1 - rx0 - 56)

    # Pie
    draw.text((wx0 + 28, wy1 - 56), "Listo · Cmd+Enter (macOS) / Ctrl+Enter (Windows) resuelve la pestaña activa",
              font=font(21), fill=MUTED)
    draw.text((wx1 - 440, wy1 - 56), "Carlos Pardo · 100 % local · sin conexión", font=font(21), fill=MUTED)

    img.save(path, quality=95)


def build_all(assets: Path) -> dict[str, Path]:
    assets.mkdir(parents=True, exist_ok=True)
    out: dict[str, Path] = {}

    configs: dict[str, dict] = {
        "grafico": {
            "figure_title": "Método gráfico",
            "figure_subtitle": "Programación lineal de dos variables: datos, región factible y tabla de vértices.",
            "active": "Método gráfico",
            "plot": True,
            "fields": [
                {"type": "section", "text": "Función objetivo"},
                {"type": "hint", "text": ["Z = 3 x1 + 5 x2"]},
                {"type": "radio", "options": [("Maximizar", True), ("Minimizar", False)]},
                {"type": "gap", "h": 6},
                {"type": "section", "text": "Restricciones"},
                {"type": "hint", "text": ["Una por línea, por ejemplo:  3 2 <= 18"]},
                {"type": "text", "h": 180, "lines": ["1 0 <= 4", "0 2 <= 12", "3 2 <= 18"]},
                {"type": "hint", "text": ["x1 ≥ 0,  x2 ≥ 0"]},
            ],
            "results": [
                ("RESULTADO — MÉTODO GRÁFICO", "h"),
                ("Función objetivo: Maximizar Z = 3 x1 + 5 x2", ""),
                ("Estado: ÓPTIMO", "ok"),
                ("Z óptimo = 36", ""),
                ("x1 = 2      x2 = 6", ""),
                ("Vértice   x1   x2    Z", "h"),
                ("V1        0    0     0", ""),
                ("V2        0    6    30", ""),
                ("V3        2    6    36  ★", "ok"),
                ("V4        4    3    27", ""),
                ("V5        4    0    12", ""),
            ],
        },
        "simplex": {
            "figure_title": "Método Simplex",
            "figure_subtitle": "Tablas de las fases 1 y 2, solución óptima y detección de casos especiales.",
            "active": "Simplex",
            "fields": [
                {"type": "section", "text": "Función objetivo"},
                {"type": "hint", "text": ["Coeficientes (x1, x2, ...):"]},
                {"type": "entry", "value": "3 5"},
                {"type": "radio", "options": [("Maximizar", True), ("Minimizar", False)]},
                {"type": "gap", "h": 8},
                {"type": "section", "text": "Restricciones"},
                {"type": "hint", "text": ["coef1 coef2 ... <= | >= | = valor"]},
                {"type": "text", "h": 230, "lines": ["1 0 <= 4", "0 2 <= 12", "3 2 <= 18"]},
                {"type": "hint", "text": ["Variables no negativas.", "Se permiten RHS negativos."]},
            ],
            "results": [
                ("RESULTADO — MÉTODO SIMPLEX (DOS FASES)", "h"),
                ("Estado: ÓPTIMO", "ok"),
                ("Z* = 36", ""),
                ("x1 = 2      x2 = 6", ""),
                ("FASE 2 · TABLA 1", "h"),
                ("Base    x1   x2   s1   s2   s3   RHS", ""),
                ("s1       1    0    1    0    0     4", ""),
                ("s2       0    2    0    1    0    12", ""),
                ("s3       3    2    0    0    1    18", ""),
                ("Z       -3   -5    0    0    0     0", ""),
                ("FASE 2 · TABLA 2  (entra x1, sale s1)", "h"),
                ("x1       1    0    1    0    0     4", ""),
                ("s2       0    2    0    1    0    12", ""),
                ("s3       0    2   -3    0    1     6", ""),
                ("Z        0   -5    3    0    0    12", ""),
            ],
        },
        "transporte": {
            "figure_title": "Modelo de transporte",
            "figure_subtitle": "Matriz de costos, oferta, demanda, solución inicial y optimización MODI.",
            "active": "Transporte",
            "fields": [
                {"type": "section", "text": "Matriz de costos"},
                {"type": "hint", "text": ["Una fila por origen. Separe valores con espacios."]},
                {"type": "text", "h": 150, "lines": ["8  6 10  9", "9 12 13  7", "14 9 16  5"]},
                {"type": "section", "text": "Oferta y demanda"},
                {"type": "label", "text": "Oferta (una por fila):", "value": "35 50 40"},
                {"type": "label", "text": "Demanda (una por columna):", "value": "45 20 30 30"},
                {"type": "hint", "text": ["Método inicial:"]},
                {"type": "combo", "value": "Vogel"},
                {"type": "check", "text": "Maximizar ganancia", "checked": False},
            ],
            "results": [
                ("RESULTADO — MODELO DE TRANSPORTE", "h"),
                ("Estado: ÓPTIMO          Método: Vogel", "ok"),
                ("Costo total mínimo: 1020", ""),
                ("SOLUCIÓN FINAL", "h"),
                ("              C1    C2    C3    C4   Oferta", ""),
                ("Planta 1       0    10    25     0      35", ""),
                ("Planta 2      45     0     5     0      50", ""),
                ("Planta 3       0    10     0    30      40", ""),
                ("Demanda       45    20    30    30     125", ""),
                ("POTENCIALES Y COSTOS DE OPORTUNIDAD", "h"),
                ("u = [0, 3, 3]       v = [6, 6, 10, 2]", ""),
                ("Delta ≥ 0 en todas las celdas: solución óptima.", "ok"),
            ],
        },
        "asignacion": {
            "figure_title": "Problema de asignación",
            "figure_subtitle": "Algoritmo húngaro: matriz de costos, asignación óptima y costo total.",
            "active": "Asignación",
            "fields": [
                {"type": "section", "text": "Matriz de costos o beneficios"},
                {"type": "hint", "text": ["Filas = agentes, columnas = tareas."]},
                {"type": "text", "h": 230, "lines": ["9 2 7 8", "6 4 3 7", "5 8 1 8", "7 6 9 4"]},
                {"type": "check", "text": "Maximizar beneficio", "checked": False},
            ],
            "results": [
                ("RESULTADO — PROBLEMA DE ASIGNACIÓN", "h"),
                ("Estado: ÓPTIMO", "ok"),
                ("Costo mínimo: 13", ""),
                ("ASIGNACIÓN ÓPTIMA", "h"),
                ("Agente   Tarea   Costo", ""),
                ("A1       T2          2", ""),
                ("A2       T1          6", ""),
                ("A3       T3          1", ""),
                ("A4       T4          4", ""),
                ("MATRIZ CON LA ASIGNACIÓN (*)", "h"),
                ("       T1  T2  T3  T4", ""),
                ("A1      9   2*  7   8", ""),
                ("A2      6*  4   3   7", ""),
                ("A3      5   8   1*  8", ""),
                ("A4      7   6   9   4*", ""),
            ],
        },
        "colas": {
            "figure_title": "Teoría de colas",
            "figure_subtitle": "Modelos M/M/1, M/M/1/K, M/M/c, M/M/c/K y M/G/1 con todas las medidas.",
            "active": "Colas",
            "fields": [
                {"type": "section", "text": "Modelo de cola"},
                {"type": "hint", "text": ["Seleccione el modelo:"]},
                {"type": "combo", "value": "M/M/1"},
                {"type": "gap", "h": 8},
                {"type": "section", "text": "Parámetros"},
                {"type": "label", "text": "λ (tasa de llegada)", "value": "2"},
                {"type": "label", "text": "μ (tasa de servicio)", "value": "3"},
                {"type": "hint", "text": ["Las unidades de tiempo de λ y μ", "determinan las de W y Wq."]},
            ],
            "results": [
                ("RESULTADO — TEORÍA DE COLAS", "h"),
                ("Modelo: M/M/1      λ = 2;  μ = 3", ""),
                ("MEDIDAS DE DESEMPEÑO", "h"),
                ("ρ              utilización        0.666667", ""),
                ("P0             sistema vacío      0.333333", ""),
                ("L              en el sistema      2", ""),
                ("Lq             en la cola         1.333333", ""),
                ("W              en el sistema      1", ""),
                ("Wq             en la cola         0.666667", ""),
                ("P(espera)      probabilidad       0.666667", ""),
                ("λ efectiva     llegadas           2", ""),
                ("P(rechazo)     rechazo            0", ""),
                ("DISTRIBUCIÓN DEL NÚMERO DE CLIENTES", "h"),
                ("n     P(N=n)    P(N≤n)", ""),
                ("0     0.333333  0.333333", ""),
                ("1     0.222222  0.555556", ""),
                ("2     0.148148  0.703704", ""),
            ],
        },
        "markov": {
            "figure_title": "Cadenas de Markov",
            "figure_subtitle": "Matriz de transición, potencia n, estado estable y clasificación de estados.",
            "active": "Markov",
            "fields": [
                {"type": "section", "text": "Matriz de transición P"},
                {"type": "hint", "text": ["Una fila por estado. Cada fila debe sumar 1."]},
                {"type": "text", "h": 170, "lines": ["0.7 0.2 0.1", "0.3 0.4 0.3", "0.2 0.2 0.6"]},
                {"type": "section", "text": "Distribución inicial y pasos"},
                {"type": "label", "text": "Distribución inicial (opcional):", "value": "1 0 0"},
                {"type": "label", "text": "Número de pasos n:", "value": "3"},
            ],
            "results": [
                ("RESULTADO — CADENA DE MARKOV", "h"),
                ("Número de estados: 3", ""),
                ("DISTRIBUCIÓN ESTACIONARIA", "h"),
                ("E1   0.45", ""),
                ("E2   0.25", ""),
                ("E3   0.30", ""),
                ("Suma = 1", "ok"),
                ("CLASIFICACIÓN DE ESTADOS", "h"),
                ("Clase 1  {E1, E2, E3}  Recurrente  Período 1", ""),
                ("Cadena irreducible: sí      aperiódica: sí", ""),
                ("DISTRIBUCIÓN DESPUÉS DE 3 PASOS", "h"),
                ("E1   0.509", ""),
                ("E2   0.248", ""),
                ("E3   0.243", ""),
            ],
        },
        "pert": {
            "figure_title": "PERT / CPM",
            "figure_subtitle": "Duración esperada, ruta crítica, holguras y probabilidad de cumplir el plazo.",
            "active": "PERT / CPM",
            "fields": [
                {"type": "section", "text": "Actividades"},
                {"type": "hint", "text": ["Nombre, optimista, probable, pesimista, predecesores"]},
                {"type": "text", "h": 250, "lines": [
                    "A, 2, 4, 6, -",
                    "B, 3, 5, 8, A",
                    "C, 4, 6, 9, A",
                    "D, 2, 3, 5, B, C",
                ]},
                {"type": "section", "text": "Plazo objetivo (opcional)"},
                {"type": "label", "text": "Tiempo T para calcular P(terminar ≤ T):", "value": "16"},
            ],
            "results": [
                ("RESULTADO — PERT / CPM", "h"),
                ("Duración esperada: 13.3333", "ok"),
                ("Varianza: 1.3889      Desv. estándar: 1.1785", ""),
                ("Ruta crítica: A → C → D", "ok"),
                ("CRONOGRAMA", "h"),
                ("Act.    te    ES    EF    LS    LF  Holg.", ""),
                ("A     4.00  0.00  4.00  0.00  4.00   0.00", ""),
                ("B     5.17  4.00  9.17  5.00 10.17   1.00", ""),
                ("C     6.17  4.00 10.17  4.00 10.17   0.00", ""),
                ("D     3.17 10.17 13.33 10.17 13.33   0.00", ""),
                ("PROBABILIDAD DE CUMPLIR EL PLAZO", "h"),
                ("P(T ≤ 16) = 98.82 %", "ok"),
                ("z = (16 − 13.3333) / 1.1785 = 2.2627", ""),
            ],
        },
        "inventarios": {
            "figure_title": "Modelos de inventario",
            "figure_subtitle": "EOQ clásico, EOQ con faltantes y lote económico de producción (EPQ).",
            "active": "Inventarios",
            "fields": [
                {"type": "section", "text": "Modelo de inventario"},
                {"type": "hint", "text": ["Seleccione el modelo:"]},
                {"type": "combo", "value": "EOQ básico"},
                {"type": "gap", "h": 8},
                {"type": "section", "text": "Parámetros anuales"},
                {"type": "label", "text": "D (demanda anual)", "value": "1200"},
                {"type": "label", "text": "S (costo de ordenar)", "value": "50"},
                {"type": "label", "text": "H (costo de mantener)", "value": "2"},
            ],
            "results": [
                ("RESULTADO — MODELO DE INVENTARIO", "h"),
                ("Modelo: EOQ básico", ""),
                ("POLÍTICA ÓPTIMA", "h"),
                ("Cantidad óptima Q*          244.949", ""),
                ("Pedidos por año             4.89898", ""),
                ("Tiempo entre pedidos       0.204124 años", ""),
                ("Inventario máximo           244.949", ""),
                ("Faltante máximo             0", ""),
                ("Costo anual de ordenar      244.949", ""),
                ("Costo anual de mantener     244.949", ""),
                ("Costo total relevante       489.898", "ok"),
                ("FÓRMULAS", "h"),
                ("Q* = sqrt(2 D S / H)", ""),
                ("Costo total = D S / Q + H Q / 2", ""),
            ],
        },
    }

    for key, cfg in configs.items():
        target = assets / f"mod_{key}.png"
        make_module(target, cfg)
        out[key] = target
    return out
