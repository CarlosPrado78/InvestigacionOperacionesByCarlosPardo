"""Utilidades de formato para el manual en Word."""

from __future__ import annotations

import re
from pathlib import Path

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_ALIGN_VERTICAL, WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

APP_NAME = "Investigación de Operaciones By Carlos Pardo"
AUTHOR = "Carlos Pardo"
VERSION = "1.0"
DATE = "Noviembre de 2026"

NAVY = RGBColor(0x0B, 0x3A, 0x5B)
BLUE = RGBColor(0x0B, 0x5C, 0xAD)
BLUE_LIGHT = RGBColor(0x2E, 0x7D, 0xC9)
TEXT = RGBColor(0x24, 0x34, 0x44)
MUTED = RGBColor(0x5A, 0x6B, 0x7D)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
GREEN = RGBColor(0x1A, 0x7F, 0x37)
AMBER = RGBColor(0xA1, 0x5C, 0x00)
RED = RGBColor(0xB0, 0x00, 0x20)
PURPLE = RGBColor(0x5B, 0x3F, 0xA0)

BODY_FONT = "Calibri"
HEAD_FONT = "Calibri Light"
MONO_FONT = "Consolas"

CALL_OUTS = {
    "info": ("EAF3FB", "0B5CAD", "NOTA", BLUE),
    "tip": ("EAF7F0", "1A7F37", "CONSEJO", GREEN),
    "warning": ("FFF6E6", "A15C00", "IMPORTANTE", AMBER),
    "danger": ("FDECEE", "B00020", "CUIDADO", RED),
    "example": ("F3F0FA", "5B3FA0", "EJEMPLO", PURPLE),
}


# ---------------------------------------------------------------------------
# XML de bajo nivel
# ---------------------------------------------------------------------------

def shade(element, color: str) -> None:
    """Aplica sombreado a una celda o párrafo."""
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), color)
    element.append(shd)


def set_cell_shading(cell, color: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shade(tc_pr, color)


def set_cell_margins(cell, top: int = 70, bottom: int = 70, left: int = 110, right: int = 110) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for tag, value in (("top", top), ("start", left), ("bottom", bottom), ("end", right)):
        node = OxmlElement(f"w:{tag}")
        node.set(qn("w:w"), str(value))
        node.set(qn("w:type"), "dxa")
        mar.append(node)
    tc_pr.append(mar)


def set_cell_borders(cell, color: str = "C9D5E3", size: int = 4, edges: str = "tblr") -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        if edge[0] not in edges and edge not in edges:
            continue
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), str(size))
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), color)
        borders.append(node)
    tc_pr.append(borders)


def set_table_borders(table, color: str = "C9D5E3", size: int = 4) -> None:
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "single")
        node.set(qn("w:sz"), str(size))
        node.set(qn("w:space"), "0")
        node.set(qn("w:color"), color)
        borders.append(node)
    tbl_pr.append(borders)


def no_table_borders(table) -> None:
    tbl_pr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        node = OxmlElement(f"w:{edge}")
        node.set(qn("w:val"), "nil")
        borders.append(node)
    tbl_pr.append(borders)


def prevent_row_split(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    node = OxmlElement("w:cantSplit")
    node.set(qn("w:val"), "true")
    tr_pr.append(node)


def repeat_header(row) -> None:
    tr_pr = row._tr.get_or_add_trPr()
    node = OxmlElement("w:tblHeader")
    node.set(qn("w:val"), "true")
    tr_pr.append(node)


def paragraph_border(paragraph, edge: str, color: str, size: int = 8, space: int = 4) -> None:
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = p_pr.find(qn("w:pBdr"))
    if p_bdr is None:
        p_bdr = OxmlElement("w:pBdr")
        p_pr.append(p_bdr)
    node = OxmlElement(f"w:{edge}")
    node.set(qn("w:val"), "single")
    node.set(qn("w:sz"), str(size))
    node.set(qn("w:space"), str(space))
    node.set(qn("w:color"), color)
    p_bdr.append(node)


def keep_with_next(paragraph, value: bool = True) -> None:
    paragraph.paragraph_format.keep_with_next = value


def add_field(paragraph, instruction: str, placeholder: str = "1") -> None:
    run = paragraph.add_run()
    begin = OxmlElement("w:fldChar")
    begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = instruction
    separate = OxmlElement("w:fldChar")
    separate.set(qn("w:fldCharType"), "separate")
    text = OxmlElement("w:t")
    text.text = placeholder
    end = OxmlElement("w:fldChar")
    end.set(qn("w:fldCharType"), "end")
    for node in (begin, instr, separate, text, end):
        run._r.append(node)


TC_PR_ORDER = [
    "cnfStyle", "tcW", "gridSpan", "hMerge", "vMerge", "tcBorders", "shd", "noWrap",
    "tcMar", "textDirection", "tcFitText", "vAlign", "hideMark", "headers", "cellIns",
    "cellDel", "cellMerge", "tcPrChange",
]
TBL_PR_ORDER = [
    "tblStyle", "tblpPr", "tblOverlap", "bidiVisual", "tblStyleRowBandSize",
    "tblStyleColBandSize", "tblW", "jc", "tblCellSpacing", "tblInd", "tblBorders",
    "shd", "tblLayout", "tblCellMar", "tblLook", "tblCaption", "tblDescription",
    "tblPrChange",
]
PPR_ORDER = [
    "pStyle", "keepNext", "keepLines", "pageBreakBefore", "framePr", "widowControl",
    "numPr", "suppressLineNumbers", "pBdr", "shd", "tabs", "suppressAutoHyphens",
    "kinsoku", "wordWrap", "overflowPunct", "topLinePunct", "autoSpaceDE",
    "autoSpaceDN", "bidi", "adjustRightInd", "snapToGrid", "spacing", "ind",
    "contextualSpacing", "mirrorIndents", "suppressOverlap", "jc", "textDirection",
    "textAlignment", "textboxTightWrap", "outlineLvl", "divId", "cnfStyle", "rPr",
    "sectPr", "pPrChange",
]
BDR_ORDER = ["top", "left", "bottom", "right", "between", "bar", "start", "end"]
TR_PR_ORDER = [
    "cnfStyle", "divId", "gridBefore", "gridAfter", "wBefore", "wAfter", "cantSplit",
    "trHeight", "tblHeader", "tblCellSpacing", "jc", "hidden", "ins", "del",
    "trPrChange",
]


def _sort_children(parent, order: list[str]) -> None:
    index = {qn(f"w:{tag}"): i for i, tag in enumerate(order)}
    children = list(parent)
    ordered = sorted(children, key=lambda el: index.get(el.tag, len(order)))
    if ordered == children:
        return
    for child in children:
        parent.remove(child)
    for child in ordered:
        parent.append(child)


def normalize_document(doc) -> None:
    """Ordena los nodos XML según el esquema de OOXML para que Word los abra sin reparaciones."""
    parts = [doc.element.body]
    for section in doc.sections:
        parts.append(section.header._element)
        parts.append(section.footer._element)
    for part in parts:
        for element in part.iter():
            if element.tag == qn("w:tcPr"):
                _sort_children(element, TC_PR_ORDER)
            elif element.tag == qn("w:tblPr"):
                _sort_children(element, TBL_PR_ORDER)
            elif element.tag == qn("w:pPr"):
                _sort_children(element, PPR_ORDER)
            elif element.tag == qn("w:tcBorders") or element.tag == qn("w:tblBorders") or element.tag == qn("w:pBdr"):
                _sort_children(element, BDR_ORDER)
            elif element.tag == qn("w:trPr"):
                _sort_children(element, TR_PR_ORDER)


def page_number_start(section, start: int = 1) -> None:
    sect_pr = section._sectPr
    pg = sect_pr.find(qn("w:pgNumType"))
    if pg is None:
        pg = OxmlElement("w:pgNumType")
        sect_pr.append(pg)
    pg.set(qn("w:start"), str(start))


# ---------------------------------------------------------------------------
# Texto enriquecido
# ---------------------------------------------------------------------------

TOKEN = re.compile(r"(\*\*.+?\*\*|`.+?`|__.+?__)")


def add_rich(paragraph, text: str, size: float | None = None, color: RGBColor | None = None) -> None:
    """Agrega texto con **negrita**, `código` y __cursiva__."""
    for part in TOKEN.split(text):
        if not part:
            continue
        if part.startswith("**") and part.endswith("**"):
            run = paragraph.add_run(part[2:-2])
            run.bold = True
        elif part.startswith("`") and part.endswith("`"):
            run = paragraph.add_run(part[1:-1])
            run.font.name = MONO_FONT
            run._element.rPr.rFonts.set(qn("w:eastAsia"), MONO_FONT)
            run.font.size = Pt((size or 10.5) - 0.8)
            run.font.color.rgb = NAVY
        elif part.startswith("__") and part.endswith("__"):
            run = paragraph.add_run(part[2:-2])
            run.italic = True
        else:
            run = paragraph.add_run(part)
        if size:
            run.font.size = Pt(size)
        if color is not None:
            run.font.color.rgb = color


def style_run(run, *, bold=False, italic=False, size=None, color=None, font=None) -> None:
    if bold:
        run.bold = True
    if italic:
        run.italic = True
    if size:
        run.font.size = Pt(size)
    if color is not None:
        run.font.color.rgb = color
    if font:
        run.font.name = font


# ---------------------------------------------------------------------------
# Documento
# ---------------------------------------------------------------------------

class Manual:
    """Envoltorio del documento con numeración automática de tablas y figuras."""

    def __init__(self) -> None:
        self.doc = Document()
        self.table_no = 0
        self.figure_no = 0
        self._setup_properties()
        self._setup_page()
        self._setup_styles()
        self._cover_section = self.doc.sections[0]
        self._configure_cover_section()
        self._add_cover()
        # Sección principal
        section = self.doc.add_section(WD_SECTION.NEW_PAGE)
        self.section = section
        self._configure_main_section(section)
        page_number_start(section, 1)
        self._add_header_footer(section)
        settings = self.doc.settings.element
        update = OxmlElement("w:updateFields")
        update.set(qn("w:val"), "true")
        settings.append(update)
        self._add_front_matter()

    # ----------------------------- configuración -----------------------------

    def _setup_properties(self) -> None:
        props = self.doc.core_properties
        props.title = f"Manual de usuario — {APP_NAME}"
        props.subject = "Guía completa de los módulos de Investigación de Operaciones"
        props.author = AUTHOR
        props.last_modified_by = AUTHOR
        props.category = "Manual de usuario"
        props.comments = "Manual de la aplicación de escritorio para macOS y Windows."
        props.keywords = "investigación de operaciones, simplex, transporte, colas, Markov, PERT, EOQ"
        props.language = "es-MX"

    def _setup_page(self) -> None:
        section = self.doc.sections[0]
        section.page_width = Cm(21.59)
        section.page_height = Cm(27.94)

    def _setup_styles(self) -> None:
        styles = self.doc.styles
        normal = styles["Normal"]
        normal.font.name = BODY_FONT
        normal.font.size = Pt(10.5)
        normal.font.color.rgb = TEXT
        normal.paragraph_format.space_after = Pt(6)
        normal.paragraph_format.line_spacing = 1.18
        rpr = normal.element.get_or_add_rPr()
        lang = OxmlElement("w:lang")
        lang.set(qn("w:val"), "es-MX")
        lang.set(qn("w:eastAsia"), "es-MX")
        rpr.append(lang)

        for name, size, color, before, after, bold in (
            ("Heading 1", 20, NAVY, 0, 14, True),
            ("Heading 2", 13.5, BLUE, 16, 6, True),
            ("Heading 3", 11.5, NAVY, 12, 4, True),
        ):
            style = styles[name]
            style.font.name = HEAD_FONT
            style.font.size = Pt(size)
            style.font.bold = bold
            style.font.color.rgb = color
            style.paragraph_format.space_before = Pt(before)
            style.paragraph_format.space_after = Pt(after)
            style.paragraph_format.keep_with_next = True
            style.paragraph_format.line_spacing = 1.05
            if name == "Heading 1":
                style.paragraph_format.page_break_before = True

        caption = styles["Caption"]
        caption.font.name = BODY_FONT
        caption.font.size = Pt(8.5)
        caption.font.italic = True
        caption.font.color.rgb = MUTED
        caption.paragraph_format.space_before = Pt(4)
        caption.paragraph_format.space_after = Pt(10)
        caption.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.CENTER

        for name in ("List Bullet", "List Bullet 2"):
            style = styles[name]
            style.font.name = BODY_FONT
            style.font.size = Pt(10.5)
            style.paragraph_format.space_after = Pt(3)
            style.paragraph_format.line_spacing = 1.15

        # Estilo de código
        from docx.enum.style import WD_STYLE_TYPE

        code = styles.add_style("Código", WD_STYLE_TYPE.PARAGRAPH)
        code.base_style = styles["Normal"]
        code.font.name = MONO_FONT
        code.font.size = Pt(9)
        code.font.color.rgb = NAVY
        code.paragraph_format.left_indent = Cm(0.35)
        code.paragraph_format.space_before = Pt(4)
        code.paragraph_format.space_after = Pt(4)
        code.paragraph_format.line_spacing = 1.05

        # Estilo para el título del índice (no debe aparecer en el propio índice)
        index = styles.add_style("Índice título", WD_STYLE_TYPE.PARAGRAPH)
        index.base_style = styles["Normal"]
        index.font.name = HEAD_FONT
        index.font.size = Pt(24)
        index.font.bold = True
        index.font.color.rgb = NAVY
        index.paragraph_format.space_before = Pt(18)
        index.paragraph_format.space_after = Pt(10)

    def _configure_cover_section(self) -> None:
        section = self._cover_section
        section.top_margin = Cm(1.25)
        section.bottom_margin = Cm(1.25)
        section.left_margin = Cm(1.25)
        section.right_margin = Cm(1.25)
        section.header_distance = Cm(0.8)
        section.footer_distance = Cm(0.8)

    def _configure_main_section(self, section) -> None:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(1.9)
        section.left_margin = Cm(2.05)
        section.right_margin = Cm(2.05)
        section.header_distance = Cm(0.9)
        section.footer_distance = Cm(0.9)

    def _add_header_footer(self, section) -> None:
        section.header.is_linked_to_previous = False
        section.footer.is_linked_to_previous = False

        header = section.header
        p = header.paragraphs[0]
        p.text = ""
        p.paragraph_format.tab_stops.clear_all()
        p.paragraph_format.tab_stops.add_tab_stop(Cm(16.8), WD_TAB_ALIGNMENT.RIGHT)
        left = p.add_run(APP_NAME)
        left.font.size = Pt(8)
        left.font.color.rgb = MUTED
        right = p.add_run("\tManual de usuario · versión 1.0")
        right.font.size = Pt(8)
        right.font.color.rgb = MUTED
        paragraph_border(p, "bottom", "C9D5E3", 4, 2)

        footer = section.footer
        p = footer.paragraphs[0]
        p.text = ""
        p.paragraph_format.tab_stops.clear_all()
        p.paragraph_format.tab_stops.add_tab_stop(Cm(8.4), WD_TAB_ALIGNMENT.CENTER)
        p.paragraph_format.tab_stops.add_tab_stop(Cm(16.8), WD_TAB_ALIGNMENT.RIGHT)
        paragraph_border(p, "top", "C9D5E3", 4, 4)
        run = p.add_run(AUTHOR)
        run.font.size = Pt(8)
        run.font.color.rgb = MUTED
        run = p.add_run("\t")
        run = p.add_run("Página ")
        run.font.size = Pt(8)
        run.font.color.rgb = MUTED
        add_field(p, "PAGE", "1")
        run = p.add_run(" de ")
        run.font.size = Pt(8)
        run.font.color.rgb = MUTED
        add_field(p, "NUMPAGES", "1")
        for run in p.runs:
            if run.font.size is None:
                run.font.size = Pt(8)
            if run.font.color.rgb is None:
                run.font.color.rgb = MUTED

    # ----------------------------- portada -----------------------------

    def _add_cover(self) -> None:
        banner = Path(__file__).resolve().parent.parent / "docs" / "assets" / "portada.png"
        if banner.exists():
            paragraph = self.doc.add_paragraph()
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
            paragraph.paragraph_format.space_after = Pt(18)
            run = paragraph.add_run()
            run.add_picture(str(banner), width=Cm(19.0))

        title = self.doc.add_paragraph()
        title.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title.paragraph_format.space_before = Pt(8)
        title.paragraph_format.space_after = Pt(2)
        run = title.add_run("MANUAL DE USUARIO")
        style_run(run, bold=True, size=26, color=NAVY)

        subtitle = self.doc.add_paragraph()
        subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
        subtitle.paragraph_format.space_after = Pt(22)
        run = subtitle.add_run("Guía completa de todos los módulos")
        style_run(run, size=12.5, color=MUTED)

        line = self.doc.add_paragraph()
        line.alignment = WD_ALIGN_PARAGRAPH.CENTER
        line.paragraph_format.space_after = Pt(24)
        run = line.add_run("─" * 30)
        style_run(run, size=9, color=RGBColor(0x35, 0xB6, 0xA6))

        table = self.doc.add_table(rows=4, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        no_table_borders(table)
        table.autofit = False
        data = [
            ("Autor", AUTHOR),
            ("Versión", VERSION),
            ("Fecha", DATE),
            ("Plataformas", "macOS  ·  Windows"),
        ]
        for i, (label, value) in enumerate(data):
            table.columns[0].width = Cm(4.2)
            table.columns[1].width = Cm(8.5)
            c0, c1 = table.rows[i].cells
            c0.width = Cm(4.2)
            c1.width = Cm(8.5)
            p0 = c0.paragraphs[0]
            p0.alignment = WD_ALIGN_PARAGRAPH.RIGHT
            p0.paragraph_format.space_after = Pt(2)
            r = p0.add_run(label)
            style_run(r, bold=True, size=9, color=MUTED)
            p1 = c1.paragraphs[0]
            p1.paragraph_format.space_after = Pt(2)
            r = p1.add_run(value)
            style_run(r, size=9.5, color=TEXT)

        note = self.doc.add_paragraph()
        note.alignment = WD_ALIGN_PARAGRAPH.CENTER
        note.paragraph_format.space_before = Pt(60)
        run = note.add_run("Documento generado para acompañar la aplicación de escritorio.\nFunciona sin conexión: los datos nunca salen del computador.")
        style_run(run, size=8.5, italic=True, color=MUTED)

    # ----------------------------- preliminares -----------------------------

    def _add_front_matter(self) -> None:
        # Página de derechos y ficha
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(30)
        run = p.add_run("Ficha del documento")
        style_run(run, bold=True, size=18, color=NAVY)
        paragraph_border(p, "bottom", "35B6A6", 12, 6)

        self.p(
            "Este manual describe el uso de la aplicación **Investigación de Operaciones "
            "By Carlos Pardo**, una suite de escritorio para resolver, presentar y explicar "
            "problemas clásicos de Investigación de Operaciones.",
            space_after=10,
        )
        self.kv_table(
            [
                ("Título", f"Manual de usuario — {APP_NAME}"),
                ("Autor", AUTHOR),
                ("Versión de la aplicación", VERSION),
                ("Fecha de publicación", DATE),
                ("Idioma", "Español"),
                ("Plataformas", "macOS 10.15 o superior · Windows 10 u 11 (64 bits)"),
                ("Requisitos", "Ninguno adicional: la aplicación es autónoma y funciona sin conexión."),
                ("Audiencia", "Estudiantes, docentes y profesionales que aplican Investigación de Operaciones."),
            ],
            widths=[4.0, 12.4],
            first_col_bold=True,
        )
        self.callout(
            "info",
            "Cómo usar este manual",
            [
                "Puede leerlo de principio a fin o ir directamente al capítulo del módulo que necesita. "
                "Cada capítulo sigue la misma estructura: qué resuelve, qué elementos tiene la pantalla, "
                "paso a paso, un ejemplo guiado con los datos del botón «Ejemplo», cómo interpretar los "
                "resultados y los errores más frecuentes.",
                "Los ejemplos están calculados con la propia aplicación, de modo que puede reproducirlos "
                "y comparar sus resultados.",
            ],
        )

        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        run = p.add_run("Convenciones visuales")
        style_run(run, bold=True, size=12, color=NAVY)

        self.table(
            ["Recuadro", "Significado"],
            [
                ["NOTA", "Información complementaria o aclaración conceptual."],
                ["CONSEJO", "Recomendación para trabajar más rápido o evitar errores."],
                ["IMPORTANTE", "Advertencia que conviene leer antes de continuar."],
                ["CUIDADO", "Situación que puede producir un resultado incorrecto o un fallo."],
                ["EJEMPLO", "Caso práctico con datos que puede reproducir en la aplicación."],
            ],
            widths=[3.4, 13.0],
            first_col_bold=True,
            caption="Convenciones usadas en los recuadros del manual.",
        )

        self.p(
            "Los textos con `este aspecto` representan datos que se escriben en la aplicación. "
            "Los atajos se indican como **Cmd + Enter** en macOS y **Ctrl + Enter** en Windows.",
        )

        # Índice
        p = self.doc.add_paragraph(style="Índice título")
        p.paragraph_format.space_before = Pt(22)
        run = p.add_run("Índice")
        style_run(run, bold=True, size=24, color=NAVY)
        paragraph_border(p, "bottom", "35B6A6", 12, 6)

        note = self.doc.add_paragraph()
        run = note.add_run(
            "El índice es automático. Si al abrir el documento aparece vacío o desactualizado, "
            "haga clic dentro de él y presione F9 (o clic derecho → Actualizar campo → "
            "Actualizar toda la tabla)."
        )
        style_run(run, size=8.5, italic=True, color=MUTED)

        toc_p = self.doc.add_paragraph()
        add_field(toc_p, r'TOC \o "1-2" \h \z \u', "Haga clic derecho y actualice el índice.")

    # ----------------------------- bloques -----------------------------

    def h1(self, text: str, page_break: bool = True) -> None:
        p = self.doc.add_heading(text, level=1)
        if not page_break:
            p.paragraph_format.page_break_before = False
        # Línea de acento bajo el título
        paragraph_border(p, "bottom", "35B6A6", 10, 4)
        p.paragraph_format.space_after = Pt(14)

    def h2(self, text: str) -> None:
        self.doc.add_heading(text, level=2)

    def h3(self, text: str) -> None:
        self.doc.add_heading(text, level=3)

    def p(
        self,
        text: str = "",
        *,
        style: str | None = None,
        align: str | None = None,
        space_before: float | None = None,
        space_after: float | None = None,
        size: float | None = None,
        color: RGBColor | None = None,
        bold: bool = False,
        italic: bool = False,
        indent: float | None = None,
    ) -> None:
        paragraph = self.doc.add_paragraph(style=style)
        add_rich(paragraph, text, size=size, color=color)
        if bold or italic:
            for run in paragraph.runs:
                run.bold = run.bold or bold
                run.italic = run.italic or italic
        if align == "center":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        elif align == "right":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        elif align == "justify":
            paragraph.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        if space_before is not None:
            paragraph.paragraph_format.space_before = Pt(space_before)
        if space_after is not None:
            paragraph.paragraph_format.space_after = Pt(space_after)
        if indent is not None:
            paragraph.paragraph_format.left_indent = Cm(indent)

    def lead(self, text: str) -> None:
        """Párrafo de entrada, algo más grande y en color."""
        paragraph = self.doc.add_paragraph()
        add_rich(paragraph, text, size=11.5, color=RGBColor(0x33, 0x47, 0x5B))
        paragraph.paragraph_format.space_after = Pt(10)
        paragraph.paragraph_format.line_spacing = 1.22

    def bullets(self, items: list[str], level: int = 1) -> None:
        style = "List Bullet" if level == 1 else "List Bullet 2"
        for item in items:
            paragraph = self.doc.add_paragraph(style=style)
            add_rich(paragraph, item)
            paragraph.paragraph_format.line_spacing = 1.12
            paragraph.paragraph_format.space_after = Pt(3)

    def steps(self, items: list[str], start: int = 1) -> None:
        """Lista numerada con control exacto del reinicio."""
        for i, item in enumerate(items, start=start):
            paragraph = self.doc.add_paragraph()
            paragraph.paragraph_format.left_indent = Cm(0.85)
            paragraph.paragraph_format.first_line_indent = Cm(-0.85)
            paragraph.paragraph_format.space_after = Pt(5)
            paragraph.paragraph_format.line_spacing = 1.14

            number = paragraph.add_run(f"{i}.")
            number.bold = True
            number.font.color.rgb = BLUE
            number.font.size = Pt(10.5)
            paragraph.add_run("\t")
            add_rich(paragraph, item)

    def code(self, lines: str | list[str], *, caption: str | None = None) -> None:
        if isinstance(lines, list):
            text = "\n".join(lines)
        else:
            text = lines
        table = self.doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cell = table.rows[0].cells[0]
        cell.width = Cm(16.4)
        set_cell_shading(cell, "F3F5F8")
        set_cell_margins(cell, 110, 110, 160, 160)
        set_cell_borders(cell, "D6DEE8", 6)
        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        for i, line in enumerate(text.splitlines()):
            if i:
                p.add_run("\n")
            run = p.add_run(line)
            run.font.name = MONO_FONT
            run._element.rPr.rFonts.set(qn("w:eastAsia"), MONO_FONT)
            run.font.size = Pt(9)
            run.font.color.rgb = NAVY
        if caption:
            self.caption(caption)

    def caption(self, text: str, *, figure: bool = False) -> None:
        if figure:
            self.figure_no += 1
            prefix = f"Figura {self.figure_no}. "
        else:
            self.table_no += 1
            prefix = f"Tabla {self.table_no}. "
        paragraph = self.doc.add_paragraph(style="Caption")
        run = paragraph.add_run(prefix)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = MUTED
        add_rich(paragraph, text, size=8.5, color=MUTED)

    def figure(self, path: Path, caption: str, width: float = 16.2) -> None:
        paragraph = self.doc.add_paragraph()
        paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
        paragraph.paragraph_format.space_before = Pt(6)
        paragraph.paragraph_format.space_after = Pt(2)
        paragraph.paragraph_format.keep_with_next = True
        run = paragraph.add_run()
        run.add_picture(str(path), width=Cm(width))
        self.caption(caption, figure=True)

    def callout(self, kind: str, title: str, body: list[str] | str) -> None:
        fill, border, label, color = CALL_OUTS[kind]
        table = self.doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        cell = table.rows[0].cells[0]
        cell.width = Cm(16.4)
        set_cell_shading(cell, fill)
        set_cell_margins(cell, 120, 120, 170, 150)
        set_cell_borders(cell, border, 6)
        # Borde izquierdo grueso
        tc_pr = cell._tc.get_or_add_tcPr()
        borders = tc_pr.find(qn("w:tcBorders"))
        if borders is not None:
            left = borders.find(qn("w:left"))
            if left is not None:
                left.set(qn("w:sz"), "28")
                left.set(qn("w:color"), border)

        p = cell.paragraphs[0]
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(label)
        run.bold = True
        run.font.size = Pt(7.5)
        run.font.color.rgb = color
        run.font.name = BODY_FONT
        run = p.add_run("   " + title)
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = color

        items = [body] if isinstance(body, str) else body
        for i, item in enumerate(items):
            paragraph = cell.add_paragraph()
            paragraph.paragraph_format.space_after = Pt(0 if i == len(items) - 1 else 3)
            paragraph.paragraph_format.line_spacing = 1.1
            add_rich(paragraph, item, size=9.3, color=TEXT)
        self.spacer(2)

    def spacer(self, points: float = 6) -> None:
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.0
        run = p.add_run("")
        run.font.size = Pt(points)

    def page_break(self) -> None:
        from docx.enum.text import WD_BREAK

        paragraph = self.doc.add_paragraph()
        paragraph.paragraph_format.space_after = Pt(0)
        paragraph.add_run().add_break(WD_BREAK.PAGE)

    def table(
        self,
        headers: list[str],
        rows: list[list[str]],
        *,
        widths: list[float] | None = None,
        aligns: list[str] | None = None,
        caption: str | None = None,
        first_col_bold: bool = False,
        font_size: float = 8.8,
        header_bg: str = "0B3A5B",
        zebra: bool = True,
    ) -> None:
        count = len(headers)
        table = self.doc.add_table(rows=1, cols=count)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        set_table_borders(table, "C9D5E3", 4)

        if widths is None:
            widths = [16.4 / count] * count
        total = sum(widths)
        if abs(total - 16.4) > 0.01:
            widths = [w * 16.4 / total for w in widths]

        if aligns is None:
            aligns = ["l"] + ["c"] * (count - 1)

        for i, width in enumerate(widths):
            table.columns[i].width = Cm(width)

        header_cells = table.rows[0].cells
        for i, header in enumerate(headers):
            cell = header_cells[i]
            cell.width = Cm(widths[i])
            set_cell_shading(cell, header_bg)
            set_cell_margins(cell)
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.0
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER if aligns[i] != "l" else WD_ALIGN_PARAGRAPH.LEFT
            run = p.add_run(header)
            run.bold = True
            run.font.size = Pt(font_size)
            run.font.color.rgb = WHITE
        repeat_header(table.rows[0])
        prevent_row_split(table.rows[0])

        for r_idx, row in enumerate(rows):
            cells = table.add_row().cells
            prevent_row_split(table.rows[-1])
            for i, value in enumerate(row):
                cell = cells[i]
                cell.width = Cm(widths[i])
                if zebra and r_idx % 2 == 1:
                    set_cell_shading(cell, "F4F8FC")
                set_cell_margins(cell)
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                p = cell.paragraphs[0]
                p.paragraph_format.space_after = Pt(0)
                p.paragraph_format.line_spacing = 1.05
                if aligns[i] == "r":
                    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
                elif aligns[i] == "c":
                    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                else:
                    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                add_rich(p, str(value), size=font_size)
                if first_col_bold and i == 0:
                    for run in p.runs:
                        run.bold = True

        if caption:
            self.caption(caption)
        else:
            self.spacer(4)

    def kv_table(
        self,
        rows: list[tuple[str, str]],
        *,
        widths: list[float] | None = None,
        caption: str | None = None,
        first_col_bold: bool = True,
    ) -> None:
        widths = widths or [4.2, 12.2]
        table = self.doc.add_table(rows=0, cols=2)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        table.autofit = False
        set_table_borders(table, "C9D5E3", 4)
        table.columns[0].width = Cm(widths[0])
        table.columns[1].width = Cm(widths[1])
        for label, value in rows:
            cells = table.add_row().cells
            cells[0].width = Cm(widths[0])
            cells[1].width = Cm(widths[1])
            set_cell_shading(cells[0], "EEF4FA")
            set_cell_margins(cells[0])
            set_cell_margins(cells[1])
            p0 = cells[0].paragraphs[0]
            p0.paragraph_format.space_after = Pt(0)
            run = p0.add_run(label)
            run.bold = first_col_bold
            run.font.size = Pt(8.8)
            run.font.color.rgb = NAVY
            p1 = cells[1].paragraphs[0]
            p1.paragraph_format.space_after = Pt(0)
            add_rich(p1, value, size=8.8)
        if caption:
            self.caption(caption)
        else:
            self.spacer(4)

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        normalize_document(self.doc)
        self.doc.save(path)
