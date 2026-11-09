"""Método Simplex de dos fases.

Resuelve problemas de programación lineal de la forma:

    max/min  c^T x
    sujeto a  A x  (<=, >=, =)  b
              x >= 0

Soporta restricciones <=, >= e =, términos independientes negativos y
detecta soluciones infactibles, no acotadas y óptimos alternativos.
"""

from __future__ import annotations

from dataclasses import dataclass
import math

EPS = 1e-9


@dataclass
class SimplexIteration:
    phase: int
    columns: list[str]
    rows: list[list[float]]
    objective: list[float]
    objective_rhs: float
    basis: list[int]
    entering: str | None = None
    leaving: str | None = None


@dataclass
class SimplexResult:
    status: str  # "optimo", "infactible", "no_acotado"
    value: float | None
    solution: list[float] | None
    iterations: list[SimplexIteration]
    message: str
    alternative_optimum: bool = False


def _pivot(rows: list[list[float]], obj: list[float], r: int, c: int) -> None:
    """Pivotea sobre (r, c). Las filas y el objetivo incluyen el RHS al final."""
    p = rows[r][c]
    if abs(p) < 1e-15:
        raise ZeroDivisionError("Pivote nulo")
    rows[r] = [v / p for v in rows[r]]
    for i in range(len(rows)):
        if i == r:
            continue
        f = rows[i][c]
        if abs(f) > 1e-14:
            rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
    f = obj[c]
    if abs(f) > 1e-14:
        obj[:] = [a - f * b for a, b in zip(obj, rows[r])]


def _pivot_rows(rows: list[list[float]], r: int, c: int) -> None:
    """Pivotea únicamente las filas (sin fila objetivo)."""
    p = rows[r][c]
    rows[r] = [v / p for v in rows[r]]
    for i in range(len(rows)):
        if i == r:
            continue
        f = rows[i][c]
        if abs(f) > 1e-14:
            rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]


def _build_objective(rows: list[list[float]], basis: list[int], c: list[float]) -> list[float]:
    """Construye la fila objetivo z - c^T x = 0 y elimina variables básicas."""
    obj = [-v for v in c] + [0.0]
    for i, b in enumerate(basis):
        cb = c[b]
        if abs(cb) > EPS:
            obj = [o + cb * v for o, v in zip(obj, rows[i])]
    return obj


def _snapshot(
    phase: int,
    columns: list[str],
    rows: list[list[float]],
    obj: list[float],
    basis: list[int],
    entering: str | None = None,
    leaving: str | None = None,
) -> SimplexIteration:
    return SimplexIteration(
        phase=phase,
        columns=list(columns),
        rows=[row[:] for row in rows],
        objective=obj[:],
        objective_rhs=obj[-1],
        basis=list(basis),
        entering=entering,
        leaving=leaving,
    )


def _run_simplex(
    rows: list[list[float]],
    basis: list[int],
    columns: list[str],
    c: list[float],
    phase: int,
    iterations: list[SimplexIteration],
    max_iter: int,
) -> tuple[str, list[float], list[int], list[list[float]]]:
    """Ejecuta el simplex (maximización) desde una base factible."""
    obj = _build_objective(rows, basis, c)
    iterations.append(_snapshot(phase, columns, rows, obj, basis))

    for _ in range(max_iter):
        # Regla de Bland: primera columna con costo reducido negativo.
        entering = next((j for j in range(len(columns)) if obj[j] < -1e-8), None)
        if entering is None:
            return "optimo", obj, basis, rows

        best_ratio = math.inf
        leaving_row = None
        leaving_basis = None
        for i, row in enumerate(rows):
            a = row[entering]
            if a > 1e-10:
                ratio = row[-1] / a
                if ratio < best_ratio - 1e-12 or (
                    abs(ratio - best_ratio) <= 1e-12
                    and (leaving_basis is None or basis[i] < leaving_basis)
                ):
                    best_ratio = ratio
                    leaving_row = i
                    leaving_basis = basis[i]

        if leaving_row is None:
            return "no_acotado", obj, basis, rows

        leaving_name = columns[basis[leaving_row]]
        _pivot(rows, obj, leaving_row, entering)
        basis[leaving_row] = entering
        iterations.append(
            _snapshot(
                phase,
                columns,
                rows,
                obj,
                basis,
                entering=columns[entering],
                leaving=leaving_name,
            )
        )

    return "limite_iteraciones", obj, basis, rows


def simplex_solve(
    c: list[float],
    A: list[list[float]],
    ops: list[str],
    b: list[float],
    maximize: bool = True,
    max_iter: int = 1000,
) -> SimplexResult:
    """Resuelve un PL con el método de dos fases.

    Parámetros
    ----------
    c : coeficientes de la función objetivo.
    A : matriz de coeficientes tecnológicos (una fila por restricción).
    ops : operadores de cada restricción: "<=", ">=" o "=".
    b : términos independientes.
    maximize : True para maximizar, False para minimizar.
    """
    n = len(c)
    m = len(A)
    if len(ops) != m or len(b) != m:
        raise ValueError("El número de restricciones no coincide con A, ops y b.")
    for row in A:
        if len(row) != n:
            raise ValueError("Todas las filas de A deben tener el mismo número de columnas.")

    A = [[float(v) for v in row] for row in A]
    b = [float(v) for v in b]
    ops = [op.strip() for op in ops]
    if any(op not in ("<=", ">=", "=") for op in ops):
        raise ValueError("Los operadores válidos son <=, >=, =.")

    # Normalizar RHS negativos.
    for i in range(m):
        if b[i] < -EPS:
            b[i] = -b[i]
            A[i] = [-v for v in A[i]]
            ops[i] = {"<=": ">=", ">=": "<=", "=": "="}[ops[i]]

    # Construir columnas: variables, holguras/excesos y artificiales.
    columns = [f"x{j + 1}" for j in range(n)]
    slack_col: dict[int, int] = {}
    artificial_col: dict[int, int] = {}
    for i, op in enumerate(ops):
        if op == "<=":
            slack_col[i] = len(columns)
            columns.append(f"s{i + 1}")
        elif op == ">=":
            slack_col[i] = len(columns)
            columns.append(f"e{i + 1}")
            artificial_col[i] = len(columns)
            columns.append(f"a{i + 1}")
        else:  # "="
            artificial_col[i] = len(columns)
            columns.append(f"a{i + 1}")

    ncols = len(columns)
    rows: list[list[float]] = []
    basis: list[int] = []
    for i in range(m):
        row = [0.0] * (ncols + 1)
        for j in range(n):
            row[j] = A[i][j]
        if i in slack_col:
            row[slack_col[i]] = 1.0 if ops[i] == "<=" else -1.0
        if i in artificial_col:
            row[artificial_col[i]] = 1.0
        row[-1] = b[i]
        rows.append(row)
        basis.append(slack_col[i] if ops[i] == "<=" else artificial_col[i])

    artificial_cols = set(artificial_col.values())
    c_phase1 = [0.0] * ncols
    for j in artificial_cols:
        c_phase1[j] = -1.0

    iterations: list[SimplexIteration] = []
    status1, obj1, basis, rows = _run_simplex(
        rows, basis, columns, c_phase1, 1, iterations, max_iter
    )

    if status1 == "no_acotado":
        return SimplexResult(
            "infactible",
            None,
            None,
            iterations,
            "La fase 1 no está acotada: el problema no tiene solución factible.",
        )

    if obj1[-1] < -1e-7:
        return SimplexResult(
            "infactible",
            None,
            None,
            iterations,
            "El problema no tiene solución factible (fase 1 termina con valor negativo).",
        )

    # Sacar de la base las variables artificiales que queden en cero.
    for i in range(len(rows)):
        if basis[i] in artificial_cols:
            pivot_col = next(
                (
                    j
                    for j in range(ncols)
                    if j not in artificial_cols and abs(rows[i][j]) > 1e-8
                ),
                None,
            )
            if pivot_col is not None:
                _pivot_rows(rows, i, pivot_col)
                basis[i] = pivot_col

    # Eliminar filas redundantes y columnas artificiales.
    keep_rows = [i for i in range(len(rows)) if basis[i] not in artificial_cols]
    rows = [rows[i] for i in keep_rows]
    basis = [basis[i] for i in keep_rows]

    keep_cols = [j for j in range(ncols) if j not in artificial_cols]
    remap = {old: new for new, old in enumerate(keep_cols)}
    columns2 = [columns[j] for j in keep_cols]
    rows = [[row[j] for j in keep_cols] + [row[-1]] for row in rows]
    basis = [remap[b] for b in basis]

    # Fase 2. Para minimizar se maximiza -c.
    c_solve = [float(v) for v in c] if maximize else [-float(v) for v in c]
    c2 = c_solve + [0.0] * (len(columns2) - n)

    status2, obj2, basis2, rows2 = _run_simplex(
        rows, basis, columns2, c2, 2, iterations, max_iter
    )

    if status2 == "no_acotado":
        return SimplexResult(
            "no_acotado",
            None,
            None,
            iterations,
            "La función objetivo no está acotada: existe una dirección de mejora infinita.",
        )
    if status2 == "limite_iteraciones":
        return SimplexResult(
            "limite_iteraciones",
            None,
            None,
            iterations,
            "Se alcanzó el límite de iteraciones antes de concluir.",
        )

    x = [0.0] * n
    for i, bcol in enumerate(basis2):
        if bcol < n:
            x[bcol] = rows2[i][-1]
    x = [0.0 if abs(v) < 1e-9 else v for v in x]
    value = obj2[-1] if maximize else -obj2[-1]
    if abs(value) < 1e-9:
        value = 0.0

    basic_set = set(basis2)
    alternative = any(
        j < n and j not in basic_set and abs(obj2[j]) < 1e-7 for j in range(len(columns2))
    )

    msg = "Solución óptima encontrada."
    if alternative:
        msg += " Existen óptimos alternativos (una variable no básica tiene costo reducido cero)."

    return SimplexResult(
        "optimo",
        value,
        x,
        iterations,
        msg,
        alternative_optimum=alternative,
    )
