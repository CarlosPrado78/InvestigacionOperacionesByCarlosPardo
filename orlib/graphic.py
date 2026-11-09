"""Método gráfico para programación lineal con dos variables."""

from __future__ import annotations

from dataclasses import dataclass
import math

from .simplex import simplex_solve

EPS = 1e-7


@dataclass
class GraphicResult:
    status: str
    value: float | None
    point: tuple[float, float] | None
    vertices: list[tuple[float, float]]
    polygon: list[tuple[float, float]]
    bounded: bool
    message: str
    constraints: list[tuple[float, float, str, float]]
    c: tuple[float, float]
    maximize: bool


def _feasible(x: float, y: float, constraints: list[tuple[float, float, str, float]]) -> bool:
    for a, b, op, rhs in constraints:
        lhs = a * x + b * y
        if op == "<=" and lhs > rhs + EPS:
            return False
        if op == ">=" and lhs < rhs - EPS:
            return False
        if op == "=" and abs(lhs - rhs) > EPS:
            return False
    return True


def _intersect(
    l1: tuple[float, float, float], l2: tuple[float, float, float]
) -> tuple[float, float] | None:
    a1, b1, r1 = l1
    a2, b2, r2 = l2
    det = a1 * b2 - a2 * b1
    if abs(det) < 1e-12:
        return None
    x = (r1 * b2 - r2 * b1) / det
    y = (a1 * r2 - a2 * r1) / det
    return (x, y)


def _dedupe(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
    out: list[tuple[float, float]] = []
    for p in points:
        if not any(abs(p[0] - q[0]) < 1e-6 and abs(p[1] - q[1]) < 1e-6 for q in out):
            out.append((0.0 if abs(p[0]) < 1e-9 else p[0], 0.0 if abs(p[1]) < 1e-9 else p[1]))
    return out


def _recession_directions(constraints: list[tuple[float, float, str, float]]) -> list[tuple[float, float]]:
    """Direcciones no nulas d tales que A d <= 0 (o = 0) para todo el poliedro."""
    candidates: list[tuple[float, float]] = []
    for a, b, _, _ in constraints:
        candidates.append((-b, a))
        candidates.append((b, -a))
    candidates += [(1.0, 0.0), (-1.0, 0.0), (0.0, 1.0), (0.0, -1.0)]

    valid: list[tuple[float, float]] = []
    for dx, dy in candidates:
        norm = math.hypot(dx, dy)
        if norm < 1e-12:
            continue
        dx, dy = dx / norm, dy / norm
        ok = True
        for a, b, op, _ in constraints:
            value = a * dx + b * dy
            if op == "<=" and value > 1e-7:
                ok = False
                break
            if op == ">=" and value < -1e-7:
                ok = False
                break
            if op == "=" and abs(value) > 1e-7:
                ok = False
                break
        if ok:
            valid.append((dx, dy))
    return valid


def solve_graphic(
    c: tuple[float, float],
    constraints: list[tuple[float, float, str, float]],
    maximize: bool = True,
) -> GraphicResult:
    """Resuelve un PL de dos variables y devuelve los vértices de la región factible.

    Se asume no negatividad (x1, x2 >= 0), como es habitual en el método gráfico.
    """
    c = (float(c[0]), float(c[1]))
    cons = [(float(a), float(b), op.strip(), float(rhs)) for a, b, op, rhs in constraints]
    for a, b, op, rhs in cons:
        if op not in ("<=", ">=", "="):
            raise ValueError("Los operadores válidos son <=, >=, =.")

    # Normalizar RHS negativos.
    normalized: list[tuple[float, float, str, float]] = []
    for a, b, op, rhs in cons:
        if rhs < -EPS:
            a, b, rhs = -a, -b, -rhs
            op = {"<=": ">=", ">=": "<=", "=": "="}[op]
        normalized.append((a, b, op, rhs))

    all_cons = normalized + [(1.0, 0.0, ">=", 0.0), (0.0, 1.0, ">=", 0.0)]

    # Vértices: intersección de todos los pares de fronteras.
    lines = [
        (a, b, rhs)
        for a, b, op, rhs in all_cons
        if not (abs(a) < 1e-12 and abs(b) < 1e-12)
    ]
    vertices: list[tuple[float, float]] = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            p = _intersect(lines[i], lines[j])
            if p is not None and _feasible(p[0], p[1], all_cons):
                vertices.append(p)
    vertices = _dedupe(vertices)

    # Resolver con simplex para determinar el estado real.
    A = [[a, b] for a, b, _, _ in normalized]
    ops = [op for _, _, op, _ in normalized]
    b = [rhs for _, _, _, rhs in normalized]
    simplex = simplex_solve(list(c), A, ops, b, maximize=maximize)

    bounded = len(_recession_directions(all_cons)) == 0
    polygon: list[tuple[float, float]] = []
    if bounded and len(vertices) >= 3:
        cx = sum(p[0] for p in vertices) / len(vertices)
        cy = sum(p[1] for p in vertices) / len(vertices)
        polygon = sorted(vertices, key=lambda p: math.atan2(p[1] - cy, p[0] - cx))

    if simplex.status == "infactible":
        return GraphicResult(
            "infactible",
            None,
            None,
            vertices,
            polygon,
            bounded,
            "La región factible es vacía: no hay solución que cumpla todas las restricciones.",
            normalized,
            c,
            maximize,
        )

    if simplex.status == "no_acotado":
        return GraphicResult(
            "no_acotado",
            None,
            None,
            vertices,
            polygon,
            bounded,
            "La función objetivo crece (o decrece) indefinidamente: no existe óptimo finito.",
            normalized,
            c,
            maximize,
        )

    if simplex.status != "optimo" or simplex.solution is None:
        return GraphicResult(
            simplex.status,
            None,
            None,
            vertices,
            polygon,
            bounded,
            simplex.message,
            normalized,
            c,
            maximize,
        )

    point = (simplex.solution[0], simplex.solution[1])
    return GraphicResult(
        "optimo",
        simplex.value,
        point,
        vertices,
        polygon,
        bounded,
        "Óptimo hallado evaluando la función objetivo en los vértices de la región factible.",
        normalized,
        c,
        maximize,
    )
