"""Problema de asignación resuelto con el algoritmo húngaro."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class AssignmentResult:
    assignment: list[int | None]  # columna asignada a cada fila (None = sin asignar)
    total_cost: float
    matrix: list[list[float]]
    maximize: bool
    message: str


def hungarian(cost: list[list[float]], maximize: bool = False) -> AssignmentResult:
    """Resuelve un problema de asignación rectangular (filas -> columnas).

    Si hay más filas que columnas, algunas filas quedan sin asignar.
    """
    if not cost or not cost[0]:
        raise ValueError("La matriz de costos está vacía.")
    n_cols = len(cost[0])
    if any(len(row) != n_cols for row in cost):
        raise ValueError("Todas las filas deben tener la misma longitud.")
    n_rows = len(cost)

    original = [[float(v) for v in row] for row in cost]
    if maximize:
        big = max(max(row) for row in original)
        work = [[big - v for v in row] for row in original]
    else:
        work = [row[:] for row in original]

    size = max(n_rows, n_cols)
    a = [[0.0] * size for _ in range(size)]
    for i in range(n_rows):
        for j in range(n_cols):
            a[i][j] = work[i][j]

    u = [0.0] * (size + 1)
    v = [0.0] * (size + 1)
    p = [0] * (size + 1)
    way = [0] * (size + 1)

    for i in range(1, size + 1):
        p[0] = i
        j0 = 0
        minv = [float("inf")] * (size + 1)
        used = [False] * (size + 1)
        while True:
            used[j0] = True
            i0 = p[j0]
            delta = float("inf")
            j1 = 0
            for j in range(1, size + 1):
                if not used[j]:
                    cur = a[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j] - 1e-12:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta - 1e-12:
                        delta = minv[j]
                        j1 = j
            for j in range(size + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            j0 = j1
            if p[j0] == 0:
                break
        while True:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
            if j0 == 0:
                break

    assignment: list[int | None] = [None] * n_rows
    for j in range(1, size + 1):
        row = p[j] - 1
        col = j - 1
        if 0 <= row < n_rows and 0 <= col < n_cols:
            assignment[row] = col

    total = sum(
        original[i][j]
        for i, j in enumerate(assignment)
        if j is not None
    )
    msg = "Asignación óptima encontrada con el algoritmo húngaro."
    if n_rows > n_cols:
        msg += " Hay más tareas que agentes: algunas filas quedan sin asignar."
    return AssignmentResult(assignment, total, original, maximize, msg)
