"""Investigación de Operaciones By Carlos Pardo — aplicación de escritorio.

Ejecutar con:  python3 main.py
Empaquetar con: build_macos.sh  o  build_windows.bat
"""

from __future__ import annotations

import math
import os
import re
import sys
import tkinter as tk
from tkinter import ttk

from orlib.graphic import solve_graphic
from orlib.simplex import simplex_solve
from orlib.transport import solve_transport
from orlib.assignment import hungarian
from orlib.queues import solve_queue
from orlib.markov import analyze
from orlib.pert import Activity, solve_pert
from orlib.inventory import solve_inventory

from ui import (
    BaseTab,
    ResultBox,
    choose_fonts,
    fmt,
    make_text,
    matrix_table,
    parse_constraints,
    parse_lp_constraints,
    parse_matrix,
    parse_names,
    parse_numbers,
    setup_styles,
    table,
)


APP_NAME = "Investigación de Operaciones By Carlos Pardo"
APP_AUTHOR = "Carlos Pardo"


# ---------------------------------------------------------------------------
# Utilidades de presentación
# ---------------------------------------------------------------------------

def linear_expr(coeffs: list[float]) -> str:
    parts: list[str] = []
    for i, c in enumerate(coeffs):
        term = f"{fmt(abs(c))} x{i + 1}"
        if not parts:
            parts.append(("-" if c < 0 else "") + term)
        else:
            parts.append((" - " if c < 0 else " + ") + term)
    return "".join(parts) if parts else "0"


def status_label(status: str) -> str:
    return {
        "optimo": "ÓPTIMO",
        "infactible": "INFACTIBLE",
        "no_acotado": "NO ACOTADO",
        "limite_iteraciones": "LÍMITE DE ITERACIONES",
        "error": "ERROR",
    }.get(status, status.upper())


def parse_activities(text: str) -> list[Activity]:
    activities: list[Activity] = []
    for line_no, raw in enumerate(text.splitlines(), start=1):
        line = raw.split("#", 1)[0].strip()
        if not line:
            continue
        parts = re.split(r"[,;]", line, maxsplit=4)
        if len(parts) < 4:
            parts = line.split(None, 4)
        if len(parts) < 4:
            raise ValueError(
                f"Línea {line_no}: use 'Nombre, optimista, probable, pesimista, predecesores'."
            )
        name = parts[0].strip()
        try:
            optimistic = float(parts[1])
            likely = float(parts[2])
            pessimistic = float(parts[3])
        except ValueError as exc:
            raise ValueError(f"Línea {line_no}: las duraciones deben ser numéricas.") from exc
        pred_text = parts[4].strip() if len(parts) >= 5 else ""
        predecessors = [
            p.strip()
            for p in re.split(r"[,;\s]+", pred_text)
            if p.strip() and p.strip() != "-"
        ]
        activities.append(Activity(name, optimistic, likely, pessimistic, predecessors))
    if not activities:
        raise ValueError("Debe ingresar al menos una actividad.")
    return activities


# ---------------------------------------------------------------------------
# Inicio
# ---------------------------------------------------------------------------

class InicioTab(BaseTab):
    def _build(self) -> None:
        ttk.Label(self, text=APP_NAME, style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            self,
            text="Suite de cálculo, presentación y análisis de resultados",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 18))

        modules = [
            ("Método gráfico", "Programación lineal con 2 variables: región factible, vértices y recta objetivo."),
            ("Simplex", "Método de dos fases con restricciones <=, >= e =. Tablas iteración por iteración."),
            ("Transporte", "Esquina noroeste, costo mínimo, Vogel y optimización MODI (u, v)."),
            ("Asignación", "Algoritmo húngaro para minimizar costos o maximizar beneficios."),
            ("Teoría de colas", "M/M/1, M/M/1/K, M/M/c, M/M/c/K y M/G/1 con todas las medidas."),
            ("Cadenas de Markov", "Potencia de la matriz, estado estable, clases, periodicidad y absorción."),
            ("PERT / CPM", "Ruta crítica, holguras y probabilidad de terminar en un plazo."),
            ("Inventarios", "EOQ, EOQ con faltantes y lote de producción EPQ."),
            ("100 % local", "Funciona sin internet. Los datos nunca salen de su computador."),
        ]
        grid = ttk.Frame(self)
        grid.pack(fill="x")
        for i, (title, description) in enumerate(modules):
            card = ttk.LabelFrame(grid, text=title, padding=10)
            card.grid(row=i // 3, column=i % 3, sticky="nsew", padx=5, pady=5)
            ttk.Label(
                card,
                text=description,
                style="Muted.TLabel",
                wraplength=270,
                justify="left",
            ).pack(anchor="w")
        for col in range(3):
            grid.columnconfigure(col, weight=1, uniform="cards")

        instructions = ttk.LabelFrame(self, text="Cómo usar", padding=12)
        instructions.pack(fill="both", expand=True, pady=(16, 0))
        text = tk.Text(
            instructions,
            wrap="word",
            font=(self.app.ui_font[0], 12),
            background="#fbfcfe",
            relief="flat",
            highlightthickness=0,
            padx=8,
            pady=6,
            height=10,
        )
        text.pack(fill="both", expand=True)
        text.insert(
            "1.0",
            "1. Elija una pestaña según el tipo de problema.\n"
            "2. Presione «Ejemplo» para cargar un caso resuelto y ver el formato de los datos.\n"
            "3. Edite los datos y presione «Resolver». También puede usar Cmd+Enter en macOS "
            "o Ctrl+Enter en Windows.\n"
            "4. Revise el desarrollo, los cálculos y la interpretación; guarde el informe con «Guardar .txt».\n\n"
            "Convenciones\n"
            "• Use punto decimal (por ejemplo 2.5) y separe valores con espacios o comas.\n"
            "• En programación lineal las variables son no negativas: x1, x2, ... ≥ 0.\n"
            "• Las unidades de tiempo de las colas son las mismas que las de λ y μ.\n"
            "• Las matrices de Markov deben tener filas que sumen 1.\n\n"
            "La aplicación incluye el desarrollo de los algoritmos, no solo la respuesta final, "
            "para que sirva como apoyo de estudio y presentación de trabajos.",
        )
        text.configure(state="disabled")


# ---------------------------------------------------------------------------
# Método gráfico
# ---------------------------------------------------------------------------

class GraphicTab(BaseTab):
    def _build(self) -> None:
        left, right = self.split(410)

        self.c1_var = tk.StringVar(value="3")
        self.c2_var = tk.StringVar(value="5")
        self.sense_var = tk.StringVar(value="max")

        objective = ttk.LabelFrame(left, text="Función objetivo", padding=10)
        objective.pack(fill="x")
        row = ttk.Frame(objective)
        row.pack(fill="x")
        ttk.Label(row, text="Z =").pack(side="left")
        ttk.Entry(row, textvariable=self.c1_var, width=8).pack(side="left", padx=(6, 2))
        ttk.Label(row, text="x1  +").pack(side="left")
        ttk.Entry(row, textvariable=self.c2_var, width=8).pack(side="left", padx=(6, 2))
        ttk.Label(row, text="x2").pack(side="left")

        sense = ttk.Frame(objective)
        sense.pack(fill="x", pady=(8, 0))
        ttk.Radiobutton(sense, text="Maximizar", variable=self.sense_var, value="max").pack(side="left")
        ttk.Radiobutton(sense, text="Minimizar", variable=self.sense_var, value="min").pack(side="left", padx=(14, 0))

        constraints = ttk.LabelFrame(left, text="Restricciones", padding=10)
        constraints.pack(fill="both", expand=True, pady=(10, 0))
        ttk.Label(
            constraints,
            text="Una por línea, por ejemplo:  3 2 <= 18",
            style="Muted.TLabel",
        ).pack(anchor="w")
        self.constraints_text = make_text(constraints, 8, 34, self.app.mono_font)
        self.constraints_text.pack(fill="both", expand=True, pady=(6, 0))
        ttk.Label(constraints, text="x1 ≥ 0,  x2 ≥ 0", style="Muted.TLabel").pack(anchor="w", pady=(4, 0))

        self.button_bar(left, self.solve, self.load_example, self.clear)

        right.rowconfigure(0, weight=3)
        right.rowconfigure(1, weight=2)
        right.columnconfigure(0, weight=1)
        plot = ttk.LabelFrame(right, text="Región factible y recta objetivo", padding=8)
        plot.grid(row=0, column=0, sticky="nsew")
        self.canvas = tk.Canvas(plot, background="#ffffff", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda _event: self._draw())

        self.result_box = ResultBox(right, self.app.mono_font, "metodo_grafico.txt")
        self.result_box.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        self._last = None
        self.load_example()

    def load_example(self) -> None:
        self.c1_var.set("3")
        self.c2_var.set("5")
        self.sense_var.set("max")
        self.constraints_text.delete("1.0", "end")
        self.constraints_text.insert(
            "1.0", "1 0 <= 4\n0 2 <= 12\n3 2 <= 18"
        )
        self.solve()

    def clear(self) -> None:
        self.c1_var.set("")
        self.c2_var.set("")
        self.constraints_text.delete("1.0", "end")
        self._last = None
        self.canvas.delete("all")
        self.result_box.show("Datos borrados. Escriba la función objetivo y las restricciones.")

    def solve(self) -> None:
        try:
            c = (float(self.c1_var.get()), float(self.c2_var.get()))
            constraints = parse_constraints(self.constraints_text.get("1.0", "end"))
            result = solve_graphic(c, constraints, maximize=self.sense_var.get() == "max")
        except Exception as exc:
            self.handle_error(exc)
            return

        self._last = result
        self.update_idletasks()
        self._draw()
        self.result_box.show(self._format(result))

    def _format(self, result) -> str:
        c1, c2 = result.c
        lines = [
            "§ RESULTADO — MÉTODO GRÁFICO",
            "",
            f"Función objetivo: {'Maximizar' if result.maximize else 'Minimizar'} Z = {linear_expr([c1, c2])}",
            f"Estado: {status_label(result.status)}",
        ]
        if result.status == "optimo" and result.point is not None:
            x1, x2 = result.point
            lines += [
                f"Z óptimo = {fmt(result.value)}",
                f"x1 = {fmt(x1)}",
                f"x2 = {fmt(x2)}",
                f"Región factible acotada: {'sí' if result.bounded else 'no'}",
            ]
        lines += ["", result.message, ""]
        lines.append("§ RESTRICCIONES (incluye no negatividad)")
        for i, (a, b, op, rhs) in enumerate(result.constraints, start=1):
            lines.append(f"R{i}: {linear_expr([a, b])} {op} {fmt(rhs)}")
        lines += ["x1 >= 0", "x2 >= 0", ""]
        lines.append("§ VÉRTICES Y EVALUACIÓN DE LA FUNCIÓN OBJETIVO")
        rows = []
        for i, (x, y) in enumerate(sorted(result.vertices), start=1):
            z = c1 * x + c2 * y
            is_opt = (
                result.point is not None
                and abs(x - result.point[0]) < 1e-7
                and abs(y - result.point[1]) < 1e-7
            )
            rows.append([f"V{i}", fmt(x), fmt(y), fmt(z), "★" if is_opt else ""])
        if rows:
            lines.append(table(["Vértice", "x1", "x2", "Z", ""], rows, ["l", "r", "r", "r", "c"]))
        else:
            lines.append("No se encontraron vértices factibles.")
        lines += ["", "La solución óptima de un PL con región acotada se encuentra en un vértice."]
        return "\n".join(lines)

    # ----------------------------- dibujo -----------------------------

    def _compute_bounds(self, result) -> tuple[float, float]:
        points = [(0.0, 0.0)] + list(result.vertices)
        for a, b, _op, rhs in result.constraints:
            if abs(a) > 1e-9:
                x = rhs / a
                if x > 0:
                    points.append((x, 0.0))
            if abs(b) > 1e-9:
                y = rhs / b
                if y > 0:
                    points.append((0.0, y))
        raw_x = max((p[0] for p in points), default=1.0) * 1.12
        raw_y = max((p[1] for p in points), default=1.0) * 1.12
        return self._nice_ceil(max(raw_x, 1.0)), self._nice_ceil(max(raw_y, 1.0))

    @staticmethod
    def _nice_ceil(value: float) -> float:
        if value <= 0:
            return 1.0
        exponent = 10 ** math.floor(math.log10(value))
        fraction = value / exponent
        if fraction <= 1:
            nice = 1
        elif fraction <= 2:
            nice = 2
        elif fraction <= 5:
            nice = 5
        else:
            nice = 10
        return nice * exponent

    @staticmethod
    def _clip(x0, y0, x1, y1, xmin, ymin, xmax, ymax):
        dx, dy = x1 - x0, y1 - y0
        p = [-dx, dx, -dy, dy]
        q = [x0 - xmin, xmax - x0, y0 - ymin, ymax - y0]
        u1, u2 = 0.0, 1.0
        for pi, qi in zip(p, q):
            if abs(pi) < 1e-12:
                if qi < 0:
                    return None
            else:
                r = qi / pi
                if pi < 0:
                    u1 = max(u1, r)
                else:
                    u2 = min(u2, r)
        if u1 > u2:
            return None
        return (x0 + u1 * dx, y0 + u1 * dy, x0 + u2 * dx, y0 + u2 * dy)

    def _draw(self) -> None:
        canvas = self.canvas
        canvas.delete("all")
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        if width < 80 or height < 80:
            return
        if self._last is None:
            canvas.create_text(
                width / 2,
                height / 2,
                text="Resuelva un modelo para ver la región factible",
                fill="#7a8a9b",
                font=(self.app.ui_font[0], 12),
            )
            return

        result = self._last
        left, bottom, top, right = 62, 48, 24, 26
        xmax, ymax = self._compute_bounds(result)

        def px(x: float) -> float:
            return left + (x / xmax) * (width - left - right)

        def py(y: float) -> float:
            return height - bottom - (y / ymax) * (height - bottom - top)

        # Rejilla y ejes.
        divisions = 5
        for i in range(divisions + 1):
            x = xmax * i / divisions
            y = ymax * i / divisions
            canvas.create_line(px(x), py(0), px(x), py(ymax), fill="#e7edf5")
            canvas.create_line(px(0), py(y), px(xmax), py(y), fill="#e7edf5")
            if i > 0:
                canvas.create_text(px(x), py(0) + 14, text=fmt(x, 2), fill="#5a6b7d", font=(self.app.ui_font[0], 8))
                canvas.create_text(px(0) - 26, py(y), text=fmt(y, 2), fill="#5a6b7d", font=(self.app.ui_font[0], 8))
        canvas.create_line(px(0), py(0), px(xmax), py(0), fill="#46586b", width=2)
        canvas.create_line(px(0), py(0), px(0), py(ymax), fill="#46586b", width=2)
        canvas.create_text(px(xmax), py(0) + 30, text="x1", fill="#33475b", font=(self.app.ui_font[0], 10, "bold"))
        canvas.create_text(px(0) - 38, py(ymax), text="x2", fill="#33475b", font=(self.app.ui_font[0], 10, "bold"))

        # Región factible.
        if len(result.polygon) >= 3:
            coords = []
            for x, y in result.polygon:
                coords.extend([px(x), py(y)])
            canvas.create_polygon(coords, fill="#d9f2e5", outline="#2e8b57", width=1, stipple="gray25")

        # Restricciones.
        colors = ["#c0392b", "#2471a3", "#8e44ad", "#b9770e", "#148f77", "#7f8c8d", "#d35400"]
        for idx, (a, b, _op, rhs) in enumerate(result.constraints):
            color = colors[idx % len(colors)]
            if abs(b) > 1e-9:
                y0 = (rhs - a * 0) / b
                y1 = (rhs - a * xmax) / b
                segment = self._clip(0, y0, xmax, y1, 0, 0, xmax, ymax)
            elif abs(a) > 1e-9:
                x = rhs / a
                segment = self._clip(x, 0, x, ymax, 0, 0, xmax, ymax)
            else:
                continue
            if segment is None:
                continue
            x0, y0, x1, y1 = segment
            canvas.create_line(px(x0), py(y0), px(x1), py(y1), fill=color, width=2)
            xm, ym = (x0 + x1) / 2, (y0 + y1) / 2
            canvas.create_text(
                px(xm),
                py(ym) - 8,
                text=f"R{idx + 1}",
                fill=color,
                font=(self.app.ui_font[0], 8, "bold"),
            )

        # Vértices.
        for x, y in result.vertices:
            canvas.create_oval(px(x) - 3, py(y) - 3, px(x) + 3, py(y) + 3, fill="#2471a3", outline="white")
            canvas.create_text(
                px(x) + 6,
                py(y) + 10,
                text=f"({fmt(x, 2)}, {fmt(y, 2)})",
                fill="#33475b",
                font=(self.app.ui_font[0], 8),
                anchor="nw",
            )

        # Recta objetivo en el óptimo.
        if result.status == "optimo" and result.value is not None and result.point is not None:
            c1, c2 = result.c
            if abs(c2) > 1e-9:
                y0 = (result.value - c1 * 0) / c2
                y1 = (result.value - c1 * xmax) / c2
                segment = self._clip(0, y0, xmax, y1, 0, 0, xmax, ymax)
            elif abs(c1) > 1e-9:
                x = result.value / c1
                segment = self._clip(x, 0, x, ymax, 0, 0, xmax, ymax)
            else:
                segment = None
            if segment is not None:
                x0, y0, x1, y1 = segment
                canvas.create_line(
                    px(x0), py(y0), px(x1), py(y1),
                    fill="#b00020", width=2, dash=(6, 4)
                )
            x, y = result.point
            canvas.create_oval(px(x) - 6, py(y) - 6, px(x) + 6, py(y) + 6, fill="#b00020", outline="white", width=2)
            canvas.create_text(
                px(x) + 10,
                py(y) - 12,
                text=f"Óptimo ({fmt(x, 2)}, {fmt(y, 2)})",
                fill="#b00020",
                font=(self.app.ui_font[0], 9, "bold"),
                anchor="sw",
            )

        if result.status != "optimo":
            canvas.create_text(
                width / 2,
                top + 6,
                text=status_label(result.status),
                fill="#b00020",
                font=(self.app.ui_font[0], 13, "bold"),
                anchor="n",
            )


# ---------------------------------------------------------------------------
# Simplex
# ---------------------------------------------------------------------------

class SimplexTab(BaseTab):
    def _build(self) -> None:
        left, right = self.split(420)

        self.c_var = tk.StringVar(value="3 5")
        self.sense_var = tk.StringVar(value="max")

        objective = ttk.LabelFrame(left, text="Función objetivo", padding=10)
        objective.pack(fill="x")
        ttk.Label(objective, text="Coeficientes (x1, x2, ...):").pack(anchor="w")
        ttk.Entry(objective, textvariable=self.c_var).pack(fill="x", pady=(4, 8))
        sense = ttk.Frame(objective)
        sense.pack(fill="x")
        ttk.Radiobutton(sense, text="Maximizar", variable=self.sense_var, value="max").pack(side="left")
        ttk.Radiobutton(sense, text="Minimizar", variable=self.sense_var, value="min").pack(side="left", padx=(14, 0))

        constraints = ttk.LabelFrame(left, text="Restricciones", padding=10)
        constraints.pack(fill="both", expand=True, pady=(10, 0))
        ttk.Label(
            constraints,
            text="Una por línea: coef1 coef2 ... <= | >= | = valor",
            style="Muted.TLabel",
        ).pack(anchor="w")
        self.constraints_text = make_text(constraints, 11, 36, self.app.mono_font)
        self.constraints_text.pack(fill="both", expand=True, pady=(6, 0))
        ttk.Label(
            constraints,
            text="Variables no negativas. Se permiten RHS negativos.",
            style="Muted.TLabel",
        ).pack(anchor="w", pady=(4, 0))

        self.button_bar(left, self.solve, self.load_example, self.clear)

        self.result_box = ResultBox(right, self.app.mono_font, "simplex.txt")
        self.result_box.pack(fill="both", expand=True)
        self.load_example()

    def load_example(self) -> None:
        self.c_var.set("3 5")
        self.sense_var.set("max")
        self.constraints_text.delete("1.0", "end")
        self.constraints_text.insert(
            "1.0",
            "1 0 <= 4\n0 2 <= 12\n3 2 <= 18",
        )
        self.solve()

    def clear(self) -> None:
        self.c_var.set("")
        self.constraints_text.delete("1.0", "end")
        self.result_box.show("Datos borrados. Escriba la función objetivo y las restricciones.")

    def solve(self) -> None:
        try:
            c = parse_numbers(self.c_var.get())
            if not c:
                raise ValueError("Ingrese los coeficientes de la función objetivo.")
            A, ops, b = parse_lp_constraints(
                self.constraints_text.get("1.0", "end"), len(c)
            )
            maximize = self.sense_var.get() == "max"
            result = simplex_solve(c, A, ops, b, maximize=maximize)
        except Exception as exc:
            self.handle_error(exc)
            return
        self.result_box.show(self._format(result, c, maximize))

    def _format(self, result, c: list[float], maximize: bool) -> str:
        lines = [
            "§ RESULTADO — MÉTODO SIMPLEX (DOS FASES)",
            "",
            f"Función objetivo: {'Maximizar' if maximize else 'Minimizar'} "
            f"Z = {linear_expr(c)}",
            f"Estado: {status_label(result.status)}",
            f"Mensaje: {result.message}",
        ]
        if result.status == "optimo" and result.solution is not None:
            lines += ["", "+ Solución óptima encontrada", f"Z* = {fmt(result.value)}"]
            for i, value in enumerate(result.solution, start=1):
                lines.append(f"x{i} = {fmt(value)}")
            if result.alternative_optimum:
                lines.append("* Hay soluciones óptimas alternativas.")
        lines += [
            "",
            "§ DESARROLLO DEL ALGORITMO",
            "La fase 1 minimiza la suma de variables artificiales para hallar una base factible.",
            "La fase 2 optimiza la función objetivo original. La fila Z contiene los costos reducidos.",
            "",
        ]

        counts = {1: 0, 2: 0}
        for iteration in result.iterations:
            counts[iteration.phase] = counts.get(iteration.phase, 0) + 1
            title = f"FASE {iteration.phase} · TABLA {counts[iteration.phase]}"
            if iteration.entering:
                title += f"   (entra {iteration.entering}, sale {iteration.leaving})"
            lines.append(f"§ {title}")
            headers = ["Base"] + iteration.columns + ["RHS"]
            rows = []
            for i, row in enumerate(iteration.rows):
                basis_name = iteration.columns[iteration.basis[i]]
                rows.append([basis_name] + [fmt(v, 3) for v in row])
            rows.append(["Z"] + [fmt(v, 3) for v in iteration.objective])
            lines.append(table(headers, rows, ["l"] + ["r"] * (len(headers) - 1)))
            lines.append("")

        if result.status != "optimo":
            lines.append("No se alcanzó una solución óptima; revise el mensaje y los datos.")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Transporte
# ---------------------------------------------------------------------------

def transport_table(
    matrix: list[list[float]],
    row_names: list[str],
    col_names: list[str],
    supply: list[float],
    demand: list[float],
    dec: int = 4,
) -> str:
    headers = [""] + col_names + ["Oferta"]
    rows = []
    for i, row in enumerate(matrix):
        rows.append([row_names[i]] + [fmt(v, dec) for v in row] + [fmt(supply[i], dec)])
    rows.append(["Demanda"] + [fmt(v, dec) for v in demand] + [fmt(sum(demand), dec)])
    return table(headers, rows, ["l"] + ["r"] * (len(headers) - 1))


class TransportTab(BaseTab):
    def _build(self) -> None:
        left, right = self.split(430)

        costs_frame = ttk.LabelFrame(left, text="Matriz de costos (filas = ofertas)", padding=10)
        costs_frame.pack(fill="both", expand=True)
        ttk.Label(
            costs_frame,
            text="Una fila por origen. Separe valores con espacios.",
            style="Muted.TLabel",
        ).pack(anchor="w")
        self.costs_text = make_text(costs_frame, 6, 34, self.app.mono_font)
        self.costs_text.pack(fill="both", expand=True, pady=(6, 0))

        self.supply_var = tk.StringVar(value="35 50 40")
        self.demand_var = tk.StringVar(value="45 20 30 30")
        self.row_names_var = tk.StringVar(value="Planta 1, Planta 2, Planta 3")
        self.col_names_var = tk.StringVar(value="Centro 1, Centro 2, Centro 3, Centro 4")
        self.method_var = tk.StringVar(value="Vogel")
        self.maximize_var = tk.BooleanVar(value=False)

        data = ttk.LabelFrame(left, text="Oferta, demanda y método", padding=10)
        data.pack(fill="x", pady=(10, 0))
        ttk.Label(data, text="Oferta (una por fila):").grid(row=0, column=0, sticky="w")
        ttk.Entry(data, textvariable=self.supply_var).grid(row=1, column=0, sticky="ew", pady=(2, 6))
        ttk.Label(data, text="Demanda (una por columna):").grid(row=2, column=0, sticky="w")
        ttk.Entry(data, textvariable=self.demand_var).grid(row=3, column=0, sticky="ew", pady=(2, 6))
        ttk.Label(data, text="Método inicial:").grid(row=4, column=0, sticky="w")
        ttk.Combobox(
            data,
            textvariable=self.method_var,
            values=["Vogel", "Costo mínimo", "Esquina noroeste"],
            state="readonly",
        ).grid(row=5, column=0, sticky="ew", pady=(2, 6))
        ttk.Checkbutton(data, text="Maximizar ganancia", variable=self.maximize_var).grid(
            row=6, column=0, sticky="w"
        )
        data.columnconfigure(0, weight=1)

        names = ttk.LabelFrame(left, text="Nombres (opcional)", padding=10)
        names.pack(fill="x", pady=(10, 0))
        ttk.Label(names, text="Orígenes:").grid(row=0, column=0, sticky="w")
        ttk.Entry(names, textvariable=self.row_names_var).grid(row=1, column=0, sticky="ew", pady=(2, 6))
        ttk.Label(names, text="Destinos:").grid(row=2, column=0, sticky="w")
        ttk.Entry(names, textvariable=self.col_names_var).grid(row=3, column=0, sticky="ew", pady=(2, 0))
        names.columnconfigure(0, weight=1)

        self.button_bar(left, self.solve, self.load_example, self.clear)

        self.result_box = ResultBox(right, self.app.mono_font, "transporte.txt")
        self.result_box.pack(fill="both", expand=True)
        self.load_example()

    def load_example(self) -> None:
        self.costs_text.delete("1.0", "end")
        self.costs_text.insert(
            "1.0",
            "8 6 10 9\n9 12 13 7\n14 9 16 5",
        )
        self.supply_var.set("35 50 40")
        self.demand_var.set("45 20 30 30")
        self.row_names_var.set("Planta 1, Planta 2, Planta 3")
        self.col_names_var.set("Centro 1, Centro 2, Centro 3, Centro 4")
        self.method_var.set("Vogel")
        self.maximize_var.set(False)
        self.solve()

    def clear(self) -> None:
        self.costs_text.delete("1.0", "end")
        self.supply_var.set("")
        self.demand_var.set("")
        self.result_box.show("Datos borrados. Escriba la matriz, la oferta y la demanda.")

    def solve(self) -> None:
        try:
            costs = parse_matrix(self.costs_text.get("1.0", "end"))
            supply = parse_numbers(self.supply_var.get())
            demand = parse_numbers(self.demand_var.get())
            if len(supply) != len(costs):
                raise ValueError("La oferta debe tener un valor por cada fila de costos.")
            if len(demand) != len(costs[0]):
                raise ValueError("La demanda debe tener un valor por cada columna de costos.")
            row_names = parse_names(
                self.row_names_var.get(), [f"O{i + 1}" for i in range(len(costs))]
            )
            col_names = parse_names(
                self.col_names_var.get(), [f"D{j + 1}" for j in range(len(costs[0]))]
            )
            if len(row_names) != len(costs):
                raise ValueError("La cantidad de nombres de orígenes no coincide con las filas.")
            if len(col_names) != len(costs[0]):
                raise ValueError("La cantidad de nombres de destinos no coincide con las columnas.")
            result = solve_transport(
                costs,
                supply,
                demand,
                method=self.method_var.get(),
                row_names=row_names,
                col_names=col_names,
                maximize=self.maximize_var.get(),
            )
        except Exception as exc:
            self.handle_error(exc)
            return
        self.result_box.show(self._format(result))

    def _format(self, result) -> str:
        objective = "Ganancia total máxima" if result.maximize else "Costo total mínimo"
        lines = [
            "§ RESULTADO — MODELO DE TRANSPORTE",
            "",
            f"Estado: {status_label(result.status)}",
            f"Método inicial: {result.method}",
            f"{objective}: {fmt(result.total_cost)}",
            f"Mensaje: {result.message}",
            "",
        ]
        if any(name == "Ficticio" for name in result.row_names + result.col_names):
            lines.append(
                "* Se agregó una fila o columna ficticia con costo cero para balancear el modelo."
            )
            lines.append("")

        lines.append("§ PROBLEMA BALANCEADO (costos por unidad)")
        lines.append(
            transport_table(
                result.costs,
                result.row_names,
                result.col_names,
                result.supply,
                result.demand,
            )
        )
        lines += ["", "§ SOLUCIÓN INICIAL"]
        initial = result.iterations[0]
        lines.append(
            transport_table(
                initial.allocation,
                result.row_names,
                result.col_names,
                result.supply,
                result.demand,
            )
        )
        lines.append(
            f"{'Ganancia' if result.maximize else 'Costo'} de la solución inicial: {fmt(initial.cost)}"
        )
        lines.append("")

        lines.append("§ ITERACIONES MODI (MEJORA DE LA SOLUCIÓN)")
        improvements = result.iterations[1:]
        if not improvements:
            lines.append("La solución inicial ya es óptima: todos los costos de oportunidad son >= 0.")
        for idx, iteration in enumerate(improvements[:20], start=1):
            ent = iteration.entering
            sal = iteration.leaving
            ent_name = (
                f"{result.row_names[ent[0]]} → {result.col_names[ent[1]]}" if ent else "—"
            )
            sal_name = (
                f"{result.row_names[sal[0]]} → {result.col_names[sal[1]]}" if sal else "—"
            )
            lines.append(
                f"Iteración {idx}: entra {ent_name}; sale {sal_name}; "
                f"theta = {fmt(iteration.theta)}; costo = {fmt(iteration.cost)}"
            )
            lines.append(
                transport_table(
                    iteration.allocation,
                    result.row_names,
                    result.col_names,
                    result.supply,
                    result.demand,
                )
            )
            lines.append("")
        if len(improvements) > 20:
            lines.append(f"* Se omitieron {len(improvements) - 20} iteraciones por espacio.")
            lines.append("")

        final = result.iterations[-1]
        lines.append("§ SOLUCIÓN FINAL")
        lines.append(
            transport_table(
                final.allocation,
                result.row_names,
                result.col_names,
                result.supply,
                result.demand,
            )
        )
        lines.append(f"{objective}: {fmt(result.total_cost)}")
        lines.append("")

        if final.u is not None and final.v is not None and final.deltas is not None:
            lines.append("§ POTENCIALES Y COSTOS DE OPORTUNIDAD")
            lines.append("u (orígenes): " + ", ".join(fmt(v) for v in final.u))
            lines.append("v (destinos): " + ", ".join(fmt(v) for v in final.v))
            lines.append(
                matrix_table(final.deltas, result.row_names, result.col_names)
            )
            lines.append(
                "Todos los valores anteriores son >= 0: la solución es óptima para el problema de minimización transformado."
            )
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Asignación
# ---------------------------------------------------------------------------

class AssignmentTab(BaseTab):
    def _build(self) -> None:
        left, right = self.split(410)

        matrix_frame = ttk.LabelFrame(left, text="Matriz de costos o beneficios", padding=10)
        matrix_frame.pack(fill="both", expand=True)
        ttk.Label(
            matrix_frame,
            text="Filas = agentes, columnas = tareas. Una fila por línea.",
            style="Muted.TLabel",
        ).pack(anchor="w")
        self.matrix_text = make_text(matrix_frame, 8, 32, self.app.mono_font)
        self.matrix_text.pack(fill="both", expand=True, pady=(6, 0))
        self.maximize_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            matrix_frame,
            text="Maximizar beneficio (en lugar de minimizar costo)",
            variable=self.maximize_var,
        ).pack(anchor="w", pady=(6, 0))

        self.button_bar(left, self.solve, self.load_example, self.clear)
        self.result_box = ResultBox(right, self.app.mono_font, "asignacion.txt")
        self.result_box.pack(fill="both", expand=True)
        self.load_example()

    def load_example(self) -> None:
        self.matrix_text.delete("1.0", "end")
        self.matrix_text.insert(
            "1.0",
            "9 2 7 8\n6 4 3 7\n5 8 1 8\n7 6 9 4",
        )
        self.maximize_var.set(False)
        self.solve()

    def clear(self) -> None:
        self.matrix_text.delete("1.0", "end")
        self.result_box.show("Datos borrados. Escriba la matriz de costos o beneficios.")

    def solve(self) -> None:
        try:
            costs = parse_matrix(self.matrix_text.get("1.0", "end"))
            result = hungarian(costs, maximize=self.maximize_var.get())
        except Exception as exc:
            self.handle_error(exc)
            return
        self.result_box.show(self._format(result))

    def _format(self, result) -> str:
        objective = "Beneficio máximo" if result.maximize else "Costo mínimo"
        lines = [
            "§ RESULTADO — PROBLEMA DE ASIGNACIÓN",
            "",
            f"Estado: ÓPTIMO",
            f"{objective}: {fmt(result.total_cost)}",
            f"Mensaje: {result.message}",
            "",
            "§ ASIGNACIÓN ÓPTIMA",
        ]
        rows = []
        for i, j in enumerate(result.assignment, start=1):
            if j is None:
                rows.append([f"Agente {i}", "—", "sin asignar"])
            else:
                rows.append([f"Agente {i}", f"Tarea {j + 1}", fmt(result.matrix[i - 1][j])])
        lines.append(table(["Agente", "Tarea", "Costo / beneficio"], rows, ["l", "l", "r"]))
        lines.append("")

        lines.append("§ MATRIZ CON LA ASIGNACIÓN MARCADA (*)")
        headers = [""] + [f"T{j + 1}" for j in range(len(result.matrix[0]))]
        matrix_rows = []
        for i, row in enumerate(result.matrix):
            cells = []
            for j, value in enumerate(row):
                mark = " *" if result.assignment[i] == j else ""
                cells.append(fmt(value) + mark)
            matrix_rows.append([f"A{i + 1}"] + cells)
        lines.append(table(headers, matrix_rows, ["l"] + ["r"] * (len(headers) - 1)))
        lines += ["", "El algoritmo húngaro garantiza el óptimo global para el problema de asignación."]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Teoría de colas
# ---------------------------------------------------------------------------

class QueueTab(BaseTab):
    MODELS = ["M/M/1", "M/M/1/K", "M/M/c", "M/M/c/K", "M/G/1"]

    def _build(self) -> None:
        left, right = self.split(390)

        self.model_var = tk.StringVar(value="M/M/1")
        model_frame = ttk.LabelFrame(left, text="Modelo de cola", padding=10)
        model_frame.pack(fill="x")
        ttk.Label(model_frame, text="Seleccione el modelo:").pack(anchor="w")
        combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=self.MODELS,
            state="readonly",
        )
        combo.pack(fill="x", pady=(4, 0))
        combo.bind("<<ComboboxSelected>>", lambda _event: self._update_fields())

        params = ttk.LabelFrame(left, text="Parámetros", padding=10)
        params.pack(fill="x", pady=(10, 0))
        self.entries: dict[str, ttk.Entry] = {}
        fields = [
            ("lam", "λ (tasa de llegada)"),
            ("mu", "μ (tasa de servicio por servidor)"),
            ("c", "c (número de servidores)"),
            ("K", "K (capacidad del sistema)"),
            ("sigma", "σ (desv. estándar del servicio)"),
        ]
        for row, (key, label) in enumerate(fields):
            ttk.Label(params, text=label).grid(row=row * 2, column=0, sticky="w", pady=(4, 0))
            entry = ttk.Entry(params)
            entry.grid(row=row * 2 + 1, column=0, sticky="ew", pady=(2, 4))
            self.entries[key] = entry
        params.columnconfigure(0, weight=1)
        defaults = {"lam": "2", "mu": "3", "c": "2", "K": "10", "sigma": "1.5"}
        for key, value in defaults.items():
            self.entries[key].insert(0, value)

        self.button_bar(left, self.solve, self.load_example, self.clear)

        self.result_box = ResultBox(right, self.app.mono_font, "colas.txt")
        self.result_box.pack(fill="both", expand=True)
        self._update_fields()
        self.load_example()

    def _update_fields(self) -> None:
        model = self.model_var.get()
        needs_c = model in ("M/M/c", "M/M/c/K")
        needs_k = model in ("M/M/1/K", "M/M/c/K")
        needs_sigma = model == "M/G/1"
        for key, enabled in (("c", needs_c), ("K", needs_k), ("sigma", needs_sigma)):
            entry = self.entries[key]
            entry.configure(state="normal" if enabled else "disabled")
        if needs_c and not self.entries["c"].get():
            self.entries["c"].insert(0, "2")
        if needs_k and not self.entries["K"].get():
            self.entries["K"].insert(0, "10")
        if needs_sigma and not self.entries["sigma"].get():
            self.entries["sigma"].insert(0, "1.5")

    def load_example(self) -> None:
        self.model_var.set("M/M/1")
        values = {"lam": "2", "mu": "3", "c": "2", "K": "10", "sigma": "1.5"}
        for key, value in values.items():
            entry = self.entries[key]
            state = str(entry.cget("state"))
            entry.configure(state="normal")
            entry.delete(0, "end")
            entry.insert(0, value)
            if state == "disabled":
                entry.configure(state="disabled")
        self._update_fields()
        self.solve()

    def clear(self) -> None:
        for key, entry in self.entries.items():
            state = str(entry.cget("state"))
            entry.configure(state="normal")
            entry.delete(0, "end")
            if state == "disabled":
                entry.configure(state="disabled")
        self.result_box.show("Datos borrados. Escriba los parámetros del modelo.")

    def solve(self) -> None:
        try:
            model = self.model_var.get()
            lam = float(self.entries["lam"].get())
            mu = float(self.entries["mu"].get())
            c = int(float(self.entries["c"].get() or 1)) if model in ("M/M/c", "M/M/c/K") else 1
            K_text = self.entries["K"].get().strip()
            K = int(float(K_text)) if K_text and model in ("M/M/1/K", "M/M/c/K") else None
            sigma_text = self.entries["sigma"].get().strip()
            sigma = float(sigma_text) if sigma_text and model == "M/G/1" else None
            result = solve_queue(model, lam, mu, c=c, K=K, sigma=sigma)
        except Exception as exc:
            self.handle_error(exc)
            return
        self.result_box.show(self._format(result))

    def _format(self, result) -> str:
        m = result["metrics"]
        lines = [
            "§ RESULTADO — TEORÍA DE COLAS",
            "",
            f"Modelo: {result['model']}",
            f"λ = {fmt(result['lambda'])};  μ = {fmt(result['mu'])}",
        ]
        if result["model"] in ("M/M/c", "M/M/c/K"):
            lines.append(f"c = {result['c']}")
        if result["K"] is not None:
            lines.append(f"K = {result['K']}")
        if result["sigma"] is not None:
            lines.append(f"σ = {fmt(result['sigma'])}")
        lines += [
            "",
            "§ MEDIDAS DE DESEMPEÑO",
            table(
                ["Símbolo", "Significado", "Valor"],
                [
                    ["ρ", "Utilización del sistema", fmt(m["rho"], 6)],
                    ["P0", "Probabilidad de sistema vacío", fmt(m["P0"], 6)],
                    ["L", "Número esperado en el sistema", fmt(m["L"], 6)],
                    ["Lq", "Número esperado en la cola", fmt(m["Lq"], 6)],
                    ["W", "Tiempo esperado en el sistema", fmt(m["W"], 6)],
                    ["Wq", "Tiempo esperado en la cola", fmt(m["Wq"], 6)],
                    ["P(espera)", "Probabilidad de esperar", fmt(m["P_espera"], 6)],
                    ["λ efectiva", "Tasa efectiva de llegada", fmt(m["lambda_efectiva"], 6)],
                    ["P(rechazo)", "Probabilidad de rechazo", fmt(m["P_rechazo"], 6)],
                ],
                ["l", "l", "r"],
            ),
            "",
            f"Nota: {result['note']}",
            "Las unidades de W y Wq son las mismas que las de 1/λ y 1/μ.",
        ]

        if result["pn"] is not None:
            lines += ["", "§ DISTRIBUCIÓN DEL NÚMERO DE CLIENTES"]
            cumulative = 0.0
            rows = []
            for n, pn in enumerate(result["pn"]):
                cumulative += pn
                rows.append([str(n), fmt(pn, 6), fmt(min(cumulative, 1.0), 6)])
            lines.append(table(["n", "P(N = n)", "P(N ≤ n)"], rows))
        lines += [
            "",
            "§ RELACIONES ÚTILES",
            "ρ = λ / (c μ)   ·   L = Lq + λ efectiva / μ",
            "W = L / λ efectiva   ·   Wq = Lq / λ efectiva",
            "Para M/M/1: L = ρ/(1-ρ), Lq = ρ²/(1-ρ), W = 1/(μ-λ).",
            "Para M/G/1: Lq = (ρ² + λ²σ²) / (2(1-ρ))  (Pollaczek-Khinchine).",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Cadenas de Markov
# ---------------------------------------------------------------------------

class MarkovTab(BaseTab):
    def _build(self) -> None:
        left, right = self.split(400)

        matrix_frame = ttk.LabelFrame(left, text="Matriz de transición P", padding=10)
        matrix_frame.pack(fill="both", expand=True)
        ttk.Label(
            matrix_frame,
            text="Una fila por estado. Cada fila debe sumar 1.",
            style="Muted.TLabel",
        ).pack(anchor="w")
        self.matrix_text = make_text(matrix_frame, 7, 32, self.app.mono_font)
        self.matrix_text.pack(fill="both", expand=True, pady=(6, 0))
        self.matrix_text.insert(
            "1.0",
            "0.7 0.2 0.1\n0.3 0.4 0.3\n0.2 0.2 0.6",
        )

        options = ttk.LabelFrame(left, text="Distribución inicial y pasos", padding=10)
        options.pack(fill="x", pady=(10, 0))
        self.initial_var = tk.StringVar(value="1 0 0")
        self.steps_var = tk.StringVar(value="3")
        ttk.Label(options, text="Distribución inicial (opcional):").grid(row=0, column=0, sticky="w")
        ttk.Entry(options, textvariable=self.initial_var).grid(row=1, column=0, sticky="ew", pady=(2, 6))
        ttk.Label(options, text="Número de pasos n:").grid(row=2, column=0, sticky="w")
        ttk.Entry(options, textvariable=self.steps_var).grid(row=3, column=0, sticky="ew", pady=(2, 0))
        options.columnconfigure(0, weight=1)

        self.button_bar(left, self.solve, self.load_example, self.clear)
        self.result_box = ResultBox(right, self.app.mono_font, "markov.txt")
        self.result_box.pack(fill="both", expand=True)
        self.load_example()

    def load_example(self) -> None:
        self.matrix_text.delete("1.0", "end")
        self.matrix_text.insert(
            "1.0",
            "0.7 0.2 0.1\n0.3 0.4 0.3\n0.2 0.2 0.6",
        )
        self.initial_var.set("1 0 0")
        self.steps_var.set("3")
        self.solve()

    def clear(self) -> None:
        self.matrix_text.delete("1.0", "end")
        self.initial_var.set("")
        self.steps_var.set("")
        self.result_box.show("Datos borrados. Escriba la matriz de transición.")

    def solve(self) -> None:
        try:
            P = parse_matrix(self.matrix_text.get("1.0", "end"))
            initial_text = self.initial_var.get().strip()
            initial = parse_numbers(initial_text) if initial_text else None
            steps = int(self.steps_var.get())
            result = analyze(P, initial=initial, steps=steps)
        except Exception as exc:
            self.handle_error(exc)
            return
        self.result_box.show(self._format(result, P))

    def _format(self, result, P: list[list[float]]) -> str:
        n = result.n
        states = [f"E{i + 1}" for i in range(n)]
        lines = [
            "§ RESULTADO — CADENA DE MARKOV",
            "",
            f"Número de estados: {n}",
            "",
            "§ MATRIZ DE TRANSICIÓN",
            matrix_table(P, states, states),
        ]

        lines += ["", f"§ MATRIZ P^{result.n} (en {int(self.steps_var.get())} pasos)"]
        lines.append(matrix_table(result.n_step, states, states))

        if result.initial is not None and result.distribution_n is not None:
            lines += ["", "§ DISTRIBUCIÓN DESPUÉS DE n PASOS"]
            lines.append(
                table(
                    ["Estado", "π0", "π0 · P^n"],
                    [[states[i], fmt(result.initial[i], 6), fmt(result.distribution_n[i], 6)] for i in range(n)],
                )
            )

        lines += ["", "§ DISTRIBUCIÓN ESTACIONARIA"]
        if result.steady_state is None:
            lines.append("* No existe una distribución estacionaria única.")
        else:
            lines.append(
                table(
                    ["Estado", "π"],
                    [[states[i], fmt(result.steady_state[i], 6)] for i in range(n)],
                )
            )
            lines.append(f"Suma = {fmt(sum(result.steady_state), 6)}")

        lines += ["", "§ CLASIFICACIÓN DE ESTADOS"]
        rows = []
        for idx, cls in enumerate(result.classes, start=1):
            rows.append(
                [
                    f"Clase {idx}",
                    "{" + ", ".join(states[s] for s in cls.states) + "}",
                    "Recurrente" if cls.recurrent else "Transitoria",
                    str(cls.period),
                ]
            )
        lines.append(table(["Clase", "Estados", "Tipo", "Período"], rows, ["l", "l", "l", "r"]))
        lines.append("")
        lines.append(f"Cadena irreducible: {'sí' if result.irreducible else 'no'}")
        lines.append(f"Cadena aperiódica: {'sí' if result.aperiodic else 'no'}")
        lines.append(
            "Estados absorbentes: "
            + (", ".join(states[s] for s in result.absorbing) if result.absorbing else "ninguno")
        )
        lines.append(
            "Estados transitorios: "
            + (", ".join(states[s] for s in result.transient) if result.transient else "ninguno")
        )

        if result.absorption is not None:
            abs_states = result.absorption["states"]
            trans = result.absorption["transient"]
            lines += ["", "§ ANÁLISIS DE ABSORCIÓN"]
            lines.append(
                table(
                    ["Estado transitorio", "Pasos esperados hasta absorción"],
                    [[states[s], fmt(result.absorption["expected_steps"][i], 6)] for i, s in enumerate(trans)],
                )
            )
            lines.append("")
            headers = ["Estado transitorio"] + [f"Absorción en {states[s]}" for s in abs_states]
            rows = []
            for i, s in enumerate(trans):
                rows.append([states[s]] + [fmt(v, 6) for v in result.absorption["probabilities"][i]])
            lines.append(table(headers, rows, ["l"] + ["r"] * len(abs_states)))

        lines += ["", result.message]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# PERT / CPM
# ---------------------------------------------------------------------------

class PertTab(BaseTab):
    def _build(self) -> None:
        left, right = self.split(430)

        activities = ttk.LabelFrame(left, text="Actividades", padding=10)
        activities.pack(fill="both", expand=True)
        ttk.Label(
            activities,
            text="Formato: Nombre, optimista, probable, pesimista, predecesores",
            style="Muted.TLabel",
            wraplength=390,
        ).pack(anchor="w")
        self.activities_text = make_text(activities, 12, 38, self.app.mono_font)
        self.activities_text.pack(fill="both", expand=True, pady=(6, 0))

        target_frame = ttk.LabelFrame(left, text="Plazo objetivo (opcional)", padding=10)
        target_frame.pack(fill="x", pady=(10, 0))
        self.target_var = tk.StringVar(value="16")
        ttk.Label(
            target_frame,
            text="Tiempo T para calcular P(terminar ≤ T):",
        ).pack(anchor="w")
        ttk.Entry(target_frame, textvariable=self.target_var).pack(fill="x", pady=(4, 0))

        self.button_bar(left, self.solve, self.load_example, self.clear)
        self.result_box = ResultBox(right, self.app.mono_font, "pert.txt")
        self.result_box.pack(fill="both", expand=True)
        self.load_example()

    def load_example(self) -> None:
        self.activities_text.delete("1.0", "end")
        self.activities_text.insert(
            "1.0",
            "A, 2, 4, 6, -\n"
            "B, 3, 5, 8, A\n"
            "C, 4, 6, 9, A\n"
            "D, 2, 3, 5, B, C",
        )
        self.target_var.set("16")
        self.solve()

    def clear(self) -> None:
        self.activities_text.delete("1.0", "end")
        self.target_var.set("")
        self.result_box.show("Datos borrados. Escriba las actividades y sus predecesores.")

    def solve(self) -> None:
        try:
            activities = parse_activities(self.activities_text.get("1.0", "end"))
            target_text = self.target_var.get().strip()
            target = float(target_text) if target_text else None
            result = solve_pert(activities, target=target)
        except Exception as exc:
            self.handle_error(exc)
            return
        self.result_box.show(self._format(result))

    def _format(self, result) -> str:
        lines = [
            "§ RESULTADO — PERT / CPM",
            "",
            f"Duración esperada del proyecto: {fmt(result.duration)}",
            f"Varianza de la ruta crítica: {fmt(result.variance)}",
            f"Desviación estándar: {fmt(result.std)}",
            f"Ruta crítica: {' → '.join(result.critical_path) if result.critical_path else 'no determinada'}",
            "",
            "§ CRONOGRAMA",
        ]
        rows = []
        for row in result.rows:
            rows.append(
                [
                    row.name,
                    fmt(row.duration),
                    fmt(row.variance),
                    fmt(row.es),
                    fmt(row.ef),
                    fmt(row.ls),
                    fmt(row.lf),
                    fmt(row.slack),
                    "Sí" if row.critical else "No",
                ]
            )
        lines.append(
            table(
                ["Act.", "te", "Var.", "ES", "EF", "LS", "LF", "Holgura", "Crítica"],
                rows,
                ["l", "r", "r", "r", "r", "r", "r", "r", "l"],
            )
        )
        lines += [
            "",
            "ES: inicio más temprano · EF: fin más temprano",
            "LS: inicio más tardío · LF: fin más tardío",
            "Holgura = LS - ES. Las actividades con holgura cero son críticas.",
        ]
        if result.probability is not None and result.target is not None:
            lines += [
                "",
                "§ PROBABILIDAD DE CUMPLIR EL PLAZO",
                f"P(T ≤ {fmt(result.target)}) = {result.probability:.4%}",
                f"z = ({fmt(result.target)} - {fmt(result.duration)}) / {fmt(result.std)}",
            ]
        lines += [
            "",
            "§ FÓRMULAS",
            "te = (optimista + 4·probable + pesimista) / 6",
            "Varianza = ((pesimista - optimista) / 6)²",
            "La probabilidad usa la aproximación normal sobre la ruta crítica.",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Inventarios
# ---------------------------------------------------------------------------

class InventoryTab(BaseTab):
    MODELS = ["EOQ básico", "EOQ con faltantes", "EPQ (producción)"]

    def _build(self) -> None:
        left, right = self.split(390)

        self.model_var = tk.StringVar(value="EOQ básico")
        model_frame = ttk.LabelFrame(left, text="Modelo de inventario", padding=10)
        model_frame.pack(fill="x")
        ttk.Label(model_frame, text="Seleccione el modelo:").pack(anchor="w")
        combo = ttk.Combobox(
            model_frame,
            textvariable=self.model_var,
            values=self.MODELS,
            state="readonly",
        )
        combo.pack(fill="x", pady=(4, 0))
        combo.bind("<<ComboboxSelected>>", lambda _event: self._update_fields())

        params = ttk.LabelFrame(left, text="Parámetros anuales", padding=10)
        params.pack(fill="x", pady=(10, 0))
        self.entries: dict[str, ttk.Entry] = {}
        fields = [
            ("D", "D (demanda anual)"),
            ("S", "S (costo de ordenar)"),
            ("H", "H (costo de mantener una unidad/año)"),
            ("B", "B (costo de faltante por unidad/año)"),
            ("p", "p (tasa anual de producción)"),
        ]
        for row, (key, label) in enumerate(fields):
            ttk.Label(params, text=label).grid(row=row * 2, column=0, sticky="w", pady=(4, 0))
            entry = ttk.Entry(params)
            entry.grid(row=row * 2 + 1, column=0, sticky="ew", pady=(2, 4))
            self.entries[key] = entry
        params.columnconfigure(0, weight=1)
        defaults = {"D": "1200", "S": "50", "H": "2", "B": "8", "p": "2000"}
        for key, value in defaults.items():
            self.entries[key].insert(0, value)

        self.button_bar(left, self.solve, self.load_example, self.clear)

        self.result_box = ResultBox(right, self.app.mono_font, "inventarios.txt")
        self.result_box.pack(fill="both", expand=True)
        self._update_fields()
        self.load_example()

    def _update_fields(self) -> None:
        model = self.model_var.get()
        needs_b = model == "EOQ con faltantes"
        needs_p = model.startswith("EPQ")
        for key, enabled in (("B", needs_b), ("p", needs_p)):
            self.entries[key].configure(state="normal" if enabled else "disabled")

    def load_example(self) -> None:
        self.model_var.set("EOQ básico")
        values = {"D": "1200", "S": "50", "H": "2", "B": "8", "p": "2000"}
        for key, value in values.items():
            entry = self.entries[key]
            state = str(entry.cget("state"))
            entry.configure(state="normal")
            entry.delete(0, "end")
            entry.insert(0, value)
            if state == "disabled":
                entry.configure(state="disabled")
        self._update_fields()
        self.solve()

    def clear(self) -> None:
        for entry in self.entries.values():
            state = str(entry.cget("state"))
            entry.configure(state="normal")
            entry.delete(0, "end")
            if state == "disabled":
                entry.configure(state="disabled")
        self.result_box.show("Datos borrados. Escriba los parámetros del inventario.")

    def solve(self) -> None:
        try:
            model = self.model_var.get()
            demand = float(self.entries["D"].get())
            order_cost = float(self.entries["S"].get())
            holding_cost = float(self.entries["H"].get())
            b_text = self.entries["B"].get().strip()
            shortage_cost = float(b_text) if b_text and model == "EOQ con faltantes" else None
            p_text = self.entries["p"].get().strip()
            production_rate = float(p_text) if p_text and model.startswith("EPQ") else None
            result = solve_inventory(
                model,
                demand,
                order_cost,
                holding_cost,
                shortage_cost=shortage_cost,
                production_rate=production_rate,
            )
        except Exception as exc:
            self.handle_error(exc)
            return
        self.result_box.show(self._format(result))

    def _format(self, result) -> str:
        lines = [
            "§ RESULTADO — MODELO DE INVENTARIO",
            "",
            f"Modelo: {result.model}",
            "",
            "§ POLÍTICA ÓPTIMA",
            table(
                ["Concepto", "Valor"],
                [
                    ["Cantidad óptima por pedido Q*", fmt(result.q)],
                    ["Número de pedidos por año", fmt(result.orders_per_year)],
                    ["Tiempo entre pedidos (años)", fmt(result.cycle_time)],
                    ["Inventario máximo", fmt(result.max_inventory)],
                    ["Faltante máximo", fmt(result.max_shortage)],
                    ["Costo anual de ordenar", fmt(result.ordering_cost)],
                    ["Costo anual de mantener", fmt(result.holding_cost)],
                    ["Costo anual de faltantes", fmt(result.shortage_cost)],
                    ["Costo total relevante", fmt(result.total_cost)],
                ],
                ["l", "r"],
            ),
            "",
            f"Nota: {result.note}",
            "",
            "§ FÓRMULAS",
        ]
        if result.model == "EOQ básico":
            lines += [
                "Q* = sqrt(2 D S / H)",
                "Costo total = D S / Q + H Q / 2",
            ]
        elif result.model == "EOQ con faltantes":
            lines += [
                "Q* = sqrt(2 D S (H + B) / (H B))",
                "Faltante máximo = Q* H / (H + B)",
                "Costo total = D S / Q + H (Q - F)² / (2Q) + B F² / (2Q)",
            ]
        else:
            lines += [
                "Q* = sqrt(2 D S / (H (1 - D/p)))",
                "Inventario máximo = Q* (1 - D/p)",
                "Costo total = D S / Q + H · inventario máximo / 2",
            ]
        lines += [
            "",
            "D: demanda anual · S: costo de ordenar · H: costo de mantener",
            "B: costo de faltante · p: tasa de producción anual",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Aplicación
# ---------------------------------------------------------------------------

class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(f"{APP_NAME} · Solucionador")
        self.geometry("1300x860")
        self.minsize(1080, 720)

        self.ui_font, self.mono_font, self.mono_bold = choose_fonts(self)
        setup_styles(self, self.ui_font[0], self.mono_font[0])

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self)
        self.notebook.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 0))

        tabs = [
            ("Inicio", InicioTab),
            ("Método gráfico", GraphicTab),
            ("Simplex", SimplexTab),
            ("Transporte", TransportTab),
            ("Asignación", AssignmentTab),
            ("Colas", QueueTab),
            ("Markov", MarkovTab),
            ("PERT / CPM", PertTab),
            ("Inventarios", InventoryTab),
        ]
        for title, cls in tabs:
            tab = cls(self.notebook, self)
            self.notebook.add(tab, text=title)

        footer = ttk.Frame(self, padding=(14, 6))
        footer.grid(row=1, column=0, sticky="ew")
        ttk.Label(
            footer,
            text="Listo · Cmd+Enter (macOS) / Ctrl+Enter (Windows) resuelve la pestaña activa",
            style="Muted.TLabel",
        ).pack(side="left")
        ttk.Label(
            footer,
            text=f"{APP_AUTHOR} · 100 % local · sin conexión",
            style="Muted.TLabel",
        ).pack(side="right")

        self.bind_all("<Control-Return>", self._solve_current)
        if sys.platform == "darwin":
            self.bind_all("<Command-Return>", self._solve_current)
        self.notebook.select(0)

    def _solve_current(self, _event=None):
        try:
            widget = self.nametowidget(self.notebook.select())
            if hasattr(widget, "solve"):
                widget.solve()
        except Exception:
            pass
        return "break"


def main() -> None:
    app = App()
    app.mainloop()


if __name__ == "__main__":
    main()
