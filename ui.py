"""Componentes reutilizables de la interfaz Tkinter."""

from __future__ import annotations

import os
import re
import sys
import tkinter as tk
import tkinter.font as tkfont
from tkinter import filedialog, messagebox, ttk


# ---------------------------------------------------------------------------
# Formato y lectura de datos
# ---------------------------------------------------------------------------

def fmt(x: float | int | None, dec: int = 4) -> str:
    """Formatea números sin ceros innecesarios."""
    if x is None:
        return "—"
    try:
        value = float(x)
    except (TypeError, ValueError):
        return str(x)
    if abs(value) < 1e-10:
        return "0"
    if abs(value) >= 1e7 or abs(value) < 1e-4:
        return f"{value:.4e}"
    text = f"{value:.{dec}f}".rstrip("0").rstrip(".")
    return text if text not in ("", "-") else "0"


def parse_numbers(text: str) -> list[float]:
    """Lee números separados por espacios, comas o punto y coma."""
    clean = text.replace(",", " ").replace(";", " ").strip()
    if not clean:
        return []
    return [float(token) for token in clean.split()]


def parse_matrix(text: str) -> list[list[float]]:
    """Lee una matriz con una fila por línea."""
    rows: list[list[float]] = []
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        line = line.replace(",", " ").replace(";", " ")
        try:
            rows.append([float(token) for token in line.split()])
        except ValueError as exc:
            raise ValueError(f"Fila {line_no}: no se pudo interpretar un número.") from exc
    if not rows:
        raise ValueError("La matriz está vacía.")
    width = len(rows[0])
    if width == 0 or any(len(row) != width for row in rows):
        raise ValueError("Todas las filas de la matriz deben tener la misma cantidad de columnas.")
    return rows


def parse_names(text: str, default: list[str]) -> list[str]:
    """Lee nombres separados por comas o espacios; usa los valores por defecto si está vacío."""
    clean = text.strip()
    if not clean:
        return default[:]
    names = [n.strip() for n in re.split(r"[,;]+|\s{2,}", clean) if n.strip()]
    if len(names) == 1:
        names = clean.split()
    return names


def parse_constraints(text: str) -> list[tuple[float, float, str, float]]:
    """Lee restricciones de la forma: a1 a2 <= b."""
    constraints: list[tuple[float, float, str, float]] = []
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        line = (
            line.replace("≤", "<=")
            .replace("≥", ">=")
            .replace("=<", "<=")
            .replace("=>", ">=")
        )
        line = re.sub(r"(<=|>=|=)", r" \1 ", line)
        line = line.replace(",", " ").replace(";", " ")
        tokens = line.split()
        if len(tokens) != 4:
            raise ValueError(
                f"Línea {line_no}: use el formato 'coef1 coef2 <= valor' "
                f"(también >= o =)."
            )
        try:
            a1, a2 = float(tokens[0]), float(tokens[1])
            rhs = float(tokens[3])
        except ValueError as exc:
            raise ValueError(f"Línea {line_no}: coeficientes o valor no numéricos.") from exc
        op = tokens[2]
        if op not in ("<=", ">=", "="):
            raise ValueError(f"Línea {line_no}: operador no válido '{op}'.")
        constraints.append((a1, a2, op, rhs))
    if not constraints:
        raise ValueError("Debe ingresar al menos una restricción.")
    return constraints


def parse_lp_constraints(
    text: str, n_vars: int
) -> tuple[list[list[float]], list[str], list[float]]:
    """Lee restricciones para n variables: a1 ... an <= b."""
    A: list[list[float]] = []
    ops: list[str] = []
    b: list[float] = []
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        line = (
            line.replace("≤", "<=")
            .replace("≥", ">=")
            .replace("=<", "<=")
            .replace("=>", ">=")
        )
        line = re.sub(r"(<=|>=|=)", r" \1 ", line)
        line = line.replace(",", " ").replace(";", " ")
        tokens = line.split()
        if len(tokens) != n_vars + 2:
            raise ValueError(
                f"Línea {line_no}: se esperaban {n_vars} coeficientes, un operador y el valor."
            )
        try:
            coefficients = [float(t) for t in tokens[:n_vars]]
            rhs = float(tokens[-1])
        except ValueError as exc:
            raise ValueError(f"Línea {line_no}: coeficientes o valor no numéricos.") from exc
        op = tokens[n_vars]
        if op not in ("<=", ">=", "="):
            raise ValueError(f"Línea {line_no}: operador no válido '{op}'.")
        A.append(coefficients)
        ops.append(op)
        b.append(rhs)
    if not A:
        raise ValueError("Debe ingresar al menos una restricción.")
    return A, ops, b


# ---------------------------------------------------------------------------
# Tablas de texto
# ---------------------------------------------------------------------------

def table(
    headers: list[str],
    rows: list[list[object]],
    aligns: list[str] | None = None,
) -> str:
    """Construye una tabla alineada para mostrar en un Text monoespaciado."""
    if aligns is None:
        aligns = ["l"] + ["r"] * (len(headers) - 1)
    str_rows = [[str(cell) for cell in row] for row in rows]
    widths = []
    for i, header in enumerate(headers):
        widths.append(
            max(
                len(str(header)),
                max((len(row[i]) for row in str_rows if i < len(row)), default=0),
            )
        )

    def line_for(cells: list[str]) -> str:
        parts = []
        for i, cell in enumerate(cells):
            if i < len(widths):
                parts.append(cell.rjust(widths[i]) if aligns[i] == "r" else cell.ljust(widths[i]))
            else:
                parts.append(cell)
        return " | ".join(parts)

    out = [line_for([str(h) for h in headers])]
    out.append("-+-".join("-" * width for width in widths))
    out.extend(line_for(row) for row in str_rows)
    return "\n".join(out)


def matrix_table(
    matrix: list[list[float]],
    row_labels: list[str],
    col_labels: list[str],
    dec: int = 4,
) -> str:
    headers = [""] + col_labels
    rows = [
        [row_labels[i]] + [fmt(v, dec) for v in matrix[i]]
        for i in range(len(matrix))
    ]
    return table(headers, rows, ["l"] + ["r"] * len(col_labels))


# ---------------------------------------------------------------------------
# Fuentes y estilos
# ---------------------------------------------------------------------------

def choose_fonts(root: tk.Tk) -> tuple[tuple[str, int], tuple[str, int, str], tuple[str, int, str]]:
    families = set(tkfont.families(root))
    if sys.platform.startswith("win"):
        ui_candidates = ["Segoe UI", "Arial", "Helvetica"]
        mono_candidates = ["Cascadia Mono", "Consolas", "Courier New"]
    elif sys.platform == "darwin":
        ui_candidates = ["Helvetica Neue", "Helvetica", "Arial"]
        mono_candidates = ["Menlo", "SF Mono", "Monaco", "Courier New"]
    else:
        ui_candidates = ["DejaVu Sans", "Liberation Sans", "Arial"]
        mono_candidates = ["DejaVu Sans Mono", "Liberation Mono", "Courier New"]

    ui = next((f for f in ui_candidates if f in families), "TkDefaultFont")
    mono = next((f for f in mono_candidates if f in families), "TkFixedFont")
    return (ui, 12), (mono, 11), (mono, 11, "bold")


def setup_styles(root: tk.Tk, ui_name: str, mono_name: str) -> None:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    bg = "#f2f5fa"
    panel = "#ffffff"
    accent = "#0b5cad"
    text = "#1c2b3a"
    muted = "#5a6b7d"

    root.configure(bg=bg)
    style.configure(".", font=(ui_name, 12), background=bg, foreground=text)
    style.configure("TFrame", background=bg)
    style.configure("Panel.TFrame", background=panel)
    style.configure("TLabel", background=bg, foreground=text)
    style.configure("Panel.TLabel", background=panel, foreground=text)
    style.configure("Muted.TLabel", background=bg, foreground=muted)
    style.configure("PanelMuted.TLabel", background=panel, foreground=muted)
    style.configure("Title.TLabel", font=(ui_name, 25, "bold"), foreground="#0a3559", background=bg)
    style.configure("Subtitle.TLabel", font=(ui_name, 13), foreground=muted, background=bg)
    style.configure("Section.TLabel", font=(ui_name, 12, "bold"), foreground="#0a3559", background=bg)
    style.configure("TLabelframe", background=bg, bordercolor="#c9d5e3", relief="solid")
    style.configure(
        "TLabelframe.Label",
        background=bg,
        foreground="#0a3559",
        font=(ui_name, 11, "bold"),
    )
    style.configure("TButton", padding=(10, 7), font=(ui_name, 11))
    style.configure(
        "Accent.TButton",
        background=accent,
        foreground="white",
        font=(ui_name, 11, "bold"),
        padding=(14, 8),
    )
    style.map(
        "Accent.TButton",
        background=[("active", "#084a8a"), ("pressed", "#06376a")],
        foreground=[("disabled", "#d0d7e2")],
    )
    style.configure("TCheckbutton", background=bg, foreground=text)
    style.configure("TRadiobutton", background=bg, foreground=text)
    style.configure("TCombobox", padding=4)
    style.configure("TNotebook", background=bg, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        padding=(16, 8),
        font=(ui_name, 11),
        background="#dfe7f2",
        foreground="#33475b",
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", panel)],
        foreground=[("selected", accent)],
    )
    style.configure("TSeparator", background="#c9d5e3")


def make_text(
    parent: tk.Misc,
    height: int,
    width: int = 34,
    font: tuple | None = None,
) -> tk.Text:
    widget = tk.Text(
        parent,
        height=height,
        width=width,
        wrap="none",
        font=font,
        background="#fbfcfe",
        foreground="#1c2b3a",
        insertbackground="#1c2b3a",
        relief="flat",
        highlightthickness=1,
        highlightbackground="#c9d5e3",
        highlightcolor="#0b5cad",
        padx=8,
        pady=6,
        undo=True,
    )
    return widget


# ---------------------------------------------------------------------------
# Panel de resultados
# ---------------------------------------------------------------------------

class ResultBox(ttk.Frame):
    def __init__(self, master: tk.Misc, mono_font: tuple, default_name: str = "resultado_io.txt"):
        super().__init__(master, style="Panel.TFrame", padding=10)
        self.default_name = default_name

        head = ttk.Frame(self, style="Panel.TFrame")
        head.pack(fill="x", pady=(0, 6))
        ttk.Label(head, text="Resultados", style="Panel.TLabel").pack(side="left")
        ttk.Button(head, text="Guardar .txt", command=self.save).pack(side="right")

        body = ttk.Frame(self, style="Panel.TFrame")
        body.pack(fill="both", expand=True)
        body.rowconfigure(0, weight=1)
        body.columnconfigure(0, weight=1)

        self.text = tk.Text(
            body,
            wrap="none",
            font=mono_font,
            background="#ffffff",
            foreground="#1c2b3a",
            relief="flat",
            padx=10,
            pady=8,
            highlightthickness=0,
            state="disabled",
        )
        yscroll = ttk.Scrollbar(body, orient="vertical", command=self.text.yview)
        xscroll = ttk.Scrollbar(body, orient="horizontal", command=self.text.xview)
        self.text.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.text.grid(row=0, column=0, sticky="nsew")
        yscroll.grid(row=0, column=1, sticky="ns")
        xscroll.grid(row=1, column=0, sticky="ew")

        self.text.tag_configure("heading", font=(mono_font[0], mono_font[1] + 1, "bold"), foreground="#0b5cad")
        self.text.tag_configure("ok", foreground="#1a7f37", font=(mono_font[0], mono_font[1], "bold"))
        self.text.tag_configure("error", foreground="#b00020", font=(mono_font[0], mono_font[1], "bold"))
        self.text.tag_configure("warn", foreground="#a15c00", font=(mono_font[0], mono_font[1], "bold"))

        self.show("Los resultados aparecerán aquí.\n\nCargue un ejemplo o escriba sus datos y presione Resolver.")

    def show(self, content: str) -> None:
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        for raw in content.splitlines():
            if raw.startswith("§ "):
                self.text.insert("end", raw[2:] + "\n", "heading")
            elif raw.startswith("+ "):
                self.text.insert("end", raw[2:] + "\n", "ok")
            elif raw.startswith("! "):
                self.text.insert("end", raw[2:] + "\n", "error")
            elif raw.startswith("* "):
                self.text.insert("end", raw[2:] + "\n", "warn")
            else:
                self.text.insert("end", raw + "\n")
        self.text.configure(state="disabled")

    def save(self) -> None:
        path = filedialog.asksaveasfilename(
            title="Guardar resultados",
            defaultextension=".txt",
            initialfile=self.default_name,
            filetypes=[("Texto", "*.txt"), ("Todos los archivos", "*.*")],
        )
        if not path:
            return
        content = self.text.get("1.0", "end-1c")
        try:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(content)
        except OSError as exc:
            messagebox.showerror("No se pudo guardar", str(exc))
            return
        messagebox.showinfo("Guardado", f"Resultados guardados en:\n{path}")


# ---------------------------------------------------------------------------
# Pestaña base
# ---------------------------------------------------------------------------

class BaseTab(ttk.Frame):
    def __init__(self, master: tk.Misc, app: "App"):
        super().__init__(master, padding=16)
        self.app = app
        self._build()

    def _build(self) -> None:  # pragma: no cover - se implementa en cada pestaña
        raise NotImplementedError

    def split(self, left_width: int = 390) -> tuple[ttk.Frame, ttk.Frame]:
        self.columnconfigure(0, weight=0, minsize=left_width)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        left = ttk.Frame(self)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 14))
        right = ttk.Frame(self)
        right.grid(row=0, column=1, sticky="nsew")
        return left, right

    def button_bar(self, parent: tk.Misc, solve_cmd, example_cmd, clear_cmd) -> None:
        bar = ttk.Frame(parent)
        bar.pack(fill="x", pady=(12, 0))
        ttk.Button(bar, text="Resolver", style="Accent.TButton", command=solve_cmd).pack(
            side="left", fill="x", expand=True
        )
        ttk.Button(bar, text="Ejemplo", command=example_cmd).pack(side="left", padx=(6, 0))
        ttk.Button(bar, text="Limpiar", command=clear_cmd).pack(side="left", padx=(6, 0))

    def handle_error(self, exc: Exception) -> None:
        messagebox.showerror("Datos no válidos", str(exc))
