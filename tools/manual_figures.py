"""Ilustraciones del manual generadas con Pillow.

Todas las figuras se crean a 300 ppp equivalentes para que se vean nítidas
al insertarlas en el documento de Word.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W = 2400  # ancho base de las figuras

NAVY = (7, 31, 51)
NAVY_2 = (10, 53, 89)
BLUE = (11, 92, 173)
BLUE_LIGHT = (46, 125, 201)
CYAN = (53, 182, 166)
AMBER = (230, 168, 58)
GREEN = (26, 127, 55)
RED = (176, 0, 32)
TEXT = (28, 43, 58)
MUTED = (90, 107, 125)
BORDER = (201, 213, 227)
PANEL = (255, 255, 255)
BG = (242, 245, 250)
ZEBRA = (244, 248, 252)

FONT_DIRS = [
    Path("/System/Library/Fonts/Supplemental"),
    Path("/System/Library/Fonts"),
    Path("/Library/Fonts"),
    Path("C:/Windows/Fonts"),
]


def _font_path(name: str) -> str | None:
    for folder in FONT_DIRS:
        candidate = folder / name
        if candidate.exists():
            return str(candidate)
    return None


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["Arial Bold.ttf", "Arial.ttf"] if bold else ["Arial.ttf", "Arial Bold.ttf"]
    for name in names:
        path = _font_path(name)
        if path:
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def mono(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    names = ["Menlo Bold.ttf", "Menlo.ttc", "Courier New Bold.ttf", "Courier New.ttf"]
    if not bold:
        names = ["Menlo.ttc", "Courier New.ttf", "Menlo Bold.ttf"]
    for name in names:
        path = _font_path(name)
        if path:
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def gradient(size: tuple[int, int], start: tuple[int, int, int], end: tuple[int, int, int]) -> Image.Image:
    width, height = size
    image = Image.new("RGB", size)
    draw = ImageDraw.Draw(image)
    for y in range(height):
        t = y / max(height - 1, 1)
        # curva suave para evitar bandas
        t = t * t * (3 - 2 * t)
        color = tuple(int(start[i] + (end[i] - start[i]) * t) for i in range(3))
        draw.line([(0, y), (width, y)], fill=color)
    return image


def text_width(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> int:
    box = draw.textbbox((0, 0), text, font=f)
    return box[2] - box[0]


def wrap(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        trial = f"{current} {word}".strip()
        if text_width(draw, trial, f) <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_lp_glyph(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Dibuja un pequeño gráfico de programación lineal decorativo."""
    x0, y0, x1, y1 = box
    width, height = x1 - x0, y1 - y0

    def px(x: float) -> float:
        return x0 + 70 + x / 6.2 * (width - 140)

    def py(y: float) -> float:
        return y1 - 60 - y / 6.2 * (height - 110)

    # Rejilla
    for i in range(1, 6):
        gx = x0 + 70 + i / 6 * (width - 140)
        gy = y1 - 60 - i / 6 * (height - 110)
        draw.line([(gx, py(0)), (gx, py(6.2))], fill=(255, 255, 255, 18), width=1)
        draw.line([(px(0), gy), (px(6.2), gy)], fill=(255, 255, 255, 18), width=1)

    polygon = [(0, 0), (4, 0), (4, 3), (2, 6), (0, 6)]
    points = [(px(x), py(y)) for x, y in polygon]
    draw.polygon(points, fill=(53, 182, 166, 70), outline=(53, 182, 166, 255), width=4)

    # Restricciones
    lines = [((0, 6), (6.2, 6)), ((6.2, -3.1), (6.2, 6.2)), ((-1, 9.3), (3.1, 0))]
    for (ax, ay), (bx, by) in lines:
        draw.line([(px(ax), py(ay)), (px(bx), py(by))], fill=(255, 255, 255, 120), width=3)

    # Recta objetivo
    draw.line([(px(-1), py(8.4)), (px(5.2), py(-0.72))], fill=(230, 168, 58, 230), width=4)

    # Vértices y óptimo
    for x, y in polygon[1:]:
        draw.ellipse([px(x) - 7, py(y) - 7, px(x) + 7, py(y) + 7], fill=(255, 255, 255, 230))
    ox, oy = px(2), py(6)
    draw.ellipse([ox - 14, oy - 14, ox + 14, oy + 14], fill=(230, 168, 58, 255))
    draw.ellipse([ox - 6, oy - 6, ox + 6, oy + 6], fill=NAVY)


def make_cover(path: Path) -> None:
    img = gradient((W, 1180), (6, 27, 45), (11, 82, 148)).convert("RGBA")
    draw = ImageDraw.Draw(img, "RGBA")

    # Retícula tenue
    for x in range(0, W, 80):
        draw.line([(x, 0), (x, 1180)], fill=(255, 255, 255, 10), width=1)
    for y in range(0, 1180, 80):
        draw.line([(0, y), (W, y)], fill=(255, 255, 255, 10), width=1)

    # Círculos decorativos
    for radius, alpha in ((620, 14), (470, 18), (330, 22)):
        draw.ellipse([W - 150 - radius, 1180 - 120 - radius, W - 150 + radius, 1180 - 120 + radius],
                     outline=(255, 255, 255, alpha), width=3)

    draw_lp_glyph(draw, (1430, 90, 2280, 780))

    # Etiqueta superior
    label = "S U I T E   D E   C Á L C U L O   ·   1 0 0 %   L O C A L"
    draw.text((170, 150), label, font=font(30, True), fill=(148, 214, 234, 235))

    # Título
    draw.text((164, 270), "Investigación de", font=font(126, True), fill=(255, 255, 255, 255))
    draw.text((164, 410), "Operaciones", font=font(126, True), fill=(255, 255, 255, 255))

    # Línea de acento
    draw.rounded_rectangle([170, 600, 500, 610], radius=5, fill=CYAN)

    draw.text((170, 650), "By Carlos Pardo", font=font(66, True), fill=(230, 244, 252, 255))
    draw.text((170, 760), "Manual de usuario", font=font(46), fill=(196, 221, 238, 255))

    # Pie
    draw.text((170, 1010), "Versión 1.0  ·  Noviembre de 2026", font=font(30), fill=(170, 200, 221, 255))
    draw.text((W - 760, 1010), "macOS  ·  Windows", font=font(30, True), fill=(170, 200, 221, 255))

    img.convert("RGB").save(path, quality=95)


def make_flow(path: Path) -> None:
    width, height = W, 720
    img = Image.new("RGB", (width, height), (247, 250, 253))
    draw = ImageDraw.Draw(img)

    steps = [
        ("1", "Elija el módulo", "Identifique el tipo de problema y abra la pestaña correspondiente.", BLUE),
        ("2", "Cargue o escriba", "Use «Ejemplo» para ver el formato o introduzca sus propios datos.", NAVY_2),
        ("3", "Resuelva", "Presione «Resolver» o use Cmd/Ctrl + Enter.", CYAN),
        ("4", "Analice y guarde", "Lea el desarrollo, interprete y guarde el informe .txt.", GREEN),
    ]
    card_w, gap = 500, 60
    start_x = (width - (card_w * 4 + gap * 3)) / 2
    top = 120

    for i, (number, title, body, color) in enumerate(steps):
        x = start_x + i * (card_w + gap)
        # Sombra
        draw.rounded_rectangle([x + 6, top + 8, x + card_w + 6, top + 430 + 8], radius=26, fill=(223, 231, 240))
        draw.rounded_rectangle([x, top, x + card_w, top + 430], radius=26, fill=PANEL, outline=BORDER, width=2)
        draw.rounded_rectangle([x, top, x + card_w, top + 12], radius=6, fill=color)
        # Número
        draw.ellipse([x + 40, top + 50, x + 132, top + 142], fill=color)
        nf = font(52, True)
        nb = draw.textbbox((0, 0), number, font=nf)
        draw.text((x + 86 - (nb[2] - nb[0]) / 2, top + 96 - (nb[3] - nb[1]) / 2 - 8), number, font=nf, fill="white")
        # Título y texto
        draw.text((x + 160, top + 66), title, font=font(38, True), fill=TEXT)
        lines = wrap(draw, body, font(30), card_w - 80)
        y = top + 180
        for line in lines:
            draw.text((x + 40, y), line, font=font(30), fill=MUTED)
            y += 44

        if i < 3:
            ax = x + card_w + 12
            ay = top + 215
            draw.line([(ax, ay), (ax + gap - 24, ay)], fill=(160, 180, 201), width=4)
            draw.polygon([(ax + gap - 24, ay - 10), (ax + gap - 6, ay), (ax + gap - 24, ay + 10)], fill=(160, 180, 201))

    draw.text((start_x, 40), "Flujo de trabajo recomendado", font=font(46, True), fill=NAVY)
    draw.text((start_x, 620), "Cada módulo conserva sus datos mientras la aplicación permanece abierta.",
              font=font(28), fill=MUTED)
    img.save(path, quality=95)


def make_general_ui(path: Path) -> None:
    width, height = W, 1720
    img = Image.new("RGB", (width, height), (247, 250, 253))
    draw = ImageDraw.Draw(img)

    draw.text((80, 46), "Anatomía de la ventana principal", font=font(48, True), fill=NAVY)
    draw.text((80, 108), "Todas las pestañas comparten la misma estructura: datos a la izquierda, resultados a la derecha.",
              font=font(30), fill=MUTED)

    # Ventana
    wx0, wy0, wx1, wy1 = 80, 190, 2320, 1480
    draw.rounded_rectangle([wx0 + 8, wy0 + 10, wx1 + 8, wy1 + 10], radius=22, fill=(220, 228, 238))
    draw.rounded_rectangle([wx0, wy0, wx1, wy1], radius=22, fill=PANEL, outline=BORDER, width=3)
    # Barra de título
    draw.rounded_rectangle([wx0, wy0, wx1, wy0 + 64], radius=22, fill=(232, 238, 246))
    draw.rectangle([wx0, wy0 + 42, wx1, wy0 + 64], fill=(232, 238, 246))
    for i, color in enumerate([(255, 95, 86), (255, 189, 46), (39, 201, 63)]):
        cx = wx0 + 28 + i * 30
        draw.ellipse([cx, wy0 + 21, cx + 18, wy0 + 39], fill=color)
    draw.text((wx0 + 520, wy0 + 17), "Investigación de Operaciones By Carlos Pardo · Solucionador",
              font=font(27, True), fill=TEXT)

    # Pestañas
    tabs = ["Inicio", "Método gráfico", "Simplex", "Transporte", "Asignación", "Colas", "Markov", "PERT / CPM", "Inventarios"]
    x = wx0 + 24
    ty = wy0 + 84
    for i, tab in enumerate(tabs):
        tw = 190 if i else 150
        active = i == 1
        if active:
            draw.rounded_rectangle([x, ty, x + tw, ty + 54], radius=10, fill=PANEL, outline=BORDER, width=2)
            draw.rounded_rectangle([x + 12, ty + 46, x + tw - 12, ty + 50], radius=2, fill=BLUE)
            color = BLUE
        else:
            draw.rounded_rectangle([x, ty, x + tw, ty + 54], radius=10, fill=(223, 231, 242))
            color = (51, 71, 91)
        draw.text((x + 24, ty + 12), tab, font=font(24, active), fill=color)
        x += tw + 8

    # Panel izquierdo
    lx0, ly0, lx1, ly1 = wx0 + 34, ty + 86, wx0 + 900, wy1 - 110
    draw.rounded_rectangle([lx0, ly0, lx1, ly1], radius=14, fill=(250, 252, 255), outline=BORDER, width=2)
    draw.text((lx0 + 30, ly0 + 24), "Función objetivo", font=font(28, True), fill=NAVY)
    draw.text((lx0 + 30, ly0 + 92), "Z =", font=font(30), fill=TEXT)
    draw.rounded_rectangle([lx0 + 90, ly0 + 80, lx0 + 290, ly0 + 132], radius=8, fill=PANEL, outline=BORDER, width=2)
    draw.text((lx0 + 108, ly0 + 88), "3", font=font(30), fill=TEXT)
    draw.text((lx0 + 310, ly0 + 92), "x1   +", font=font(30), fill=TEXT)
    draw.rounded_rectangle([lx0 + 440, ly0 + 80, lx0 + 640, ly0 + 132], radius=8, fill=PANEL, outline=BORDER, width=2)
    draw.text((lx0 + 458, ly0 + 88), "5", font=font(30), fill=TEXT)
    draw.text((lx0 + 660, ly0 + 92), "x2", font=font(30), fill=TEXT)
    draw.ellipse([lx0 + 90, ly0 + 168, lx0 + 112, ly0 + 190], outline=BLUE, width=3)
    draw.ellipse([lx0 + 94, ly0 + 172, lx0 + 108, ly0 + 186], fill=BLUE)
    draw.text((lx0 + 126, ly0 + 164), "Maximizar", font=font(26), fill=TEXT)
    draw.ellipse([lx0 + 310, ly0 + 168, lx0 + 332, ly0 + 190], outline=BLUE, width=3)
    draw.text((lx0 + 346, ly0 + 164), "Minimizar", font=font(26), fill=TEXT)

    draw.text((lx0 + 30, ly0 + 250), "Restricciones", font=font(28, True), fill=NAVY)
    draw.text((lx0 + 30, ly0 + 306), "Una por línea, por ejemplo:  3 2 <= 18", font=font(23), fill=MUTED)
    draw.rounded_rectangle([lx0 + 30, ly0 + 348, lx1 - 30, ly0 + 690], radius=10, fill=(251, 252, 254), outline=BORDER, width=2)
    for i, line in enumerate(["1 0 <= 4", "0 2 <= 12", "3 2 <= 18"]):
        draw.text((lx0 + 54, ly0 + 376 + i * 62), line, font=mono(30), fill=TEXT)

    # Botones
    by = ly1 - 100
    draw.rounded_rectangle([lx0 + 30, by, lx0 + 330, by + 66], radius=10, fill=BLUE)
    draw.text((lx0 + 128, by + 16), "Resolver", font=font(28, True), fill="white")
    draw.rounded_rectangle([lx0 + 348, by, lx0 + 520, by + 66], radius=10, fill=(230, 236, 244), outline=BORDER, width=2)
    draw.text((lx0 + 394, by + 16), "Ejemplo", font=font(27), fill=TEXT)
    draw.rounded_rectangle([lx0 + 538, by, lx0 + 710, by + 66], radius=10, fill=(230, 236, 244), outline=BORDER, width=2)
    draw.text((lx0 + 584, by + 16), "Limpiar", font=font(27), fill=TEXT)

    # Panel derecho: resultados
    rx0, ry0, rx1, ry1 = lx1 + 30, ly0, wx1 - 34, wy1 - 110
    draw.rounded_rectangle([rx0, ry0, rx1, ry1], radius=14, fill=PANEL, outline=BORDER, width=2)
    draw.text((rx0 + 28, ry0 + 20), "Resultados", font=font(27, True), fill=TEXT)
    draw.rounded_rectangle([rx1 - 220, ry0 + 16, rx1 - 24, ry0 + 64], radius=8, fill=(230, 236, 244), outline=BORDER, width=2)
    draw.text((rx1 - 196, ry0 + 26), "Guardar .txt", font=font(23), fill=TEXT)
    lines = [
        ("RESULTADO — MÉTODO GRÁFICO", BLUE, True),
        ("Función objetivo: Maximizar Z = 3 x1 + 5 x2", TEXT, False),
        ("Estado: ÓPTIMO", GREEN, True),
        ("Z óptimo = 36", TEXT, False),
        ("x1 = 2", TEXT, False),
        ("x2 = 6", TEXT, False),
        ("", TEXT, False),
        ("VÉRTICES Y EVALUACIÓN", BLUE, True),
        ("V1   0   0    0", TEXT, False),
        ("V2   0   6   30", TEXT, False),
        ("V3   2   6   36  ★", TEXT, False),
        ("V4   4   3   27", TEXT, False),
        ("V5   4   0   12", TEXT, False),
    ]
    y = ry0 + 100
    for line, color, bold in lines:
        draw.text((rx0 + 34, y), line, font=mono(28, bold), fill=color)
        y += 52

    # Pie
    draw.text((wx0 + 30, wy1 - 60), "Listo · Cmd+Enter (macOS) / Ctrl+Enter (Windows) resuelve la pestaña activa",
              font=font(23), fill=MUTED)
    draw.text((wx1 - 480, wy1 - 60), "Carlos Pardo · 100 % local · sin conexión", font=font(23), fill=MUTED)

    # Leyenda de llamadas
    legend_y = 1560
    items = [
        ("1", "Pestañas: un módulo por técnica", BLUE),
        ("2", "Panel de datos de entrada", NAVY_2),
        ("3", "Botones Resolver / Ejemplo / Limpiar", CYAN),
        ("4", "Resultados y desarrollo del algoritmo", GREEN),
        ("5", "Guardar el informe en .txt", AMBER),
    ]
    x = 100
    for number, text, color in items:
        draw.ellipse([x, legend_y, x + 42, legend_y + 42], fill=color)
        nb = draw.textbbox((0, 0), number, font=font(24, True))
        draw.text((x + 21 - (nb[2] - nb[0]) / 2, legend_y + 8), number, font=font(24, True), fill="white")
        draw.text((x + 56, legend_y + 4), text, font=font(24), fill=MUTED)
        x += 56 + text_width(draw, text, font(24)) + 55

    img.save(path, quality=95)
