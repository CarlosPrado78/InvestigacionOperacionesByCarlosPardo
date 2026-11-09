"""Cadenas de Markov de tiempo discreto: potencia, estado estable y clasificación."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from math import gcd


EPS = 1e-10


@dataclass
class MarkovClass:
    states: list[int]
    recurrent: bool
    period: int


@dataclass
class MarkovResult:
    n: int
    steady_state: list[float] | None
    n_step: list[list[float]]
    classes: list[MarkovClass]
    absorbing: list[int]
    transient: list[int]
    irreducible: bool
    aperiodic: bool
    absorption: dict[str, object] | None
    message: str
    initial: list[float] | None = None
    distribution_n: list[float] | None = None


def validate_matrix(P: list[list[float]]) -> int:
    if not P or not P[0]:
        raise ValueError("La matriz de transición está vacía.")
    n = len(P)
    if any(len(row) != n for row in P):
        raise ValueError("La matriz de transición debe ser cuadrada.")
    for i, row in enumerate(P):
        for value in row:
            if value < -EPS:
                raise ValueError(f"La fila {i + 1} contiene una probabilidad negativa.")
        if abs(sum(row) - 1.0) > 1e-7:
            raise ValueError(
                f"La fila {i + 1} suma {sum(row):.6f}; cada fila debe sumar 1."
            )
    return n


def mat_mul(A: list[list[float]], B: list[list[float]]) -> list[list[float]]:
    n, m, p = len(A), len(B), len(B[0])
    return [
        [sum(A[i][k] * B[k][j] for k in range(m)) for j in range(p)]
        for i in range(n)
    ]


def mat_pow(P: list[list[float]], power: int) -> list[list[float]]:
    n = len(P)
    result = [[1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    base = [row[:] for row in P]
    while power > 0:
        if power & 1:
            result = mat_mul(result, base)
        base = mat_mul(base, base)
        power >>= 1
    return result


def mat_vec(A: list[list[float]], x: list[float]) -> list[float]:
    return [sum(a * b for a, b in zip(row, x)) for row in A]


def _solve_linear(A: list[list[float]], b: list[float]) -> list[float] | None:
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot][col]) < 1e-12:
            return None
        M[col], M[pivot] = M[pivot], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for r in range(n):
            if r == col:
                continue
            f = M[r][col]
            if abs(f) > 1e-14:
                M[r] = [a - f * c for a, c in zip(M[r], M[col])]
    return [M[i][-1] for i in range(n)]


def _inverse(A: list[list[float]]) -> list[list[float]] | None:
    n = len(A)
    M = [A[i][:] + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[pivot][col]) < 1e-12:
            return None
        M[col], M[pivot] = M[pivot], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for r in range(n):
            if r == col:
                continue
            f = M[r][col]
            if abs(f) > 1e-14:
                M[r] = [a - f * c for a, c in zip(M[r], M[col])]
    return [row[n:] for row in M]


def steady_state(P: list[list[float]]) -> list[float] | None:
    """Resuelve pi = pi P, sum(pi)=1. Devuelve None si no es única."""
    n = len(P)
    # (P^T - I) pi = 0, reemplazando la última ecuación por la normalización.
    A = [[P[j][i] - (1.0 if i == j else 0.0) for j in range(n)] for i in range(n)]
    A[-1] = [1.0] * n
    b = [0.0] * n
    b[-1] = 1.0
    result = _solve_linear(A, b)
    if result is None:
        return None
    # Corregir ruido numérico y normalizar.
    result = [max(0.0, v) for v in result]
    total = sum(result)
    if total <= EPS:
        return None
    return [v / total for v in result]


def _tarjan(P: list[list[float]]) -> list[list[int]]:
    n = len(P)
    index = 0
    indices = [-1] * n
    low = [0] * n
    on_stack = [False] * n
    stack: list[int] = []
    components: list[list[int]] = []

    def strongconnect(v: int) -> None:
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v)
        on_stack[v] = True
        for w in range(n):
            if P[v][w] > EPS:
                if indices[w] == -1:
                    strongconnect(w)
                    low[v] = min(low[v], low[w])
                elif on_stack[w]:
                    low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            comp: list[int] = []
            while True:
                w = stack.pop()
                on_stack[w] = False
                comp.append(w)
                if w == v:
                    break
            components.append(sorted(comp))

    for v in range(n):
        if indices[v] == -1:
            strongconnect(v)
    return components


def _period(P: list[list[float]], comp: list[int]) -> int:
    comp_set = set(comp)
    root = comp[0]
    level = {root: 0}
    queue = deque([root])
    while queue:
        u = queue.popleft()
        for v in comp:
            if P[u][v] > EPS and v not in level:
                level[v] = level[u] + 1
                queue.append(v)
    g = 0
    for u in comp:
        for v in comp:
            if P[u][v] > EPS and u in level and v in level:
                g = gcd(g, abs(level[u] + 1 - level[v]))
    return g if g > 1 else 1


def analyze(P: list[list[float]], initial: list[float] | None = None, steps: int = 1) -> MarkovResult:
    n = validate_matrix(P)
    P = [[float(v) for v in row] for row in P]
    if steps < 0:
        raise ValueError("El número de pasos debe ser >= 0.")

    components = _tarjan(P)
    classes: list[MarkovClass] = []
    state_class: dict[int, int] = {}
    for idx, comp in enumerate(components):
        outgoing = any(
            P[u][v] > EPS for u in comp for v in range(n) if v not in comp
        )
        classes.append(MarkovClass(comp, recurrent=not outgoing, period=_period(P, comp)))
        for s in comp:
            state_class[s] = idx

    absorbing = [i for i in range(n) if P[i][i] > 1.0 - 1e-9]
    transient = sorted(
        s for s, ci in state_class.items() if not classes[ci].recurrent
    )
    irreducible = len(classes) == 1
    aperiodic = all(c.period == 1 for c in classes)

    Pn = mat_pow(P, steps)
    pi = steady_state(P) if len([c for c in classes if c.recurrent]) == 1 else None

    absorption = None
    if absorbing and transient:
        t_index = {s: i for i, s in enumerate(transient)}
        q = [[P[i][j] for j in transient] for i in transient]
        r = [[P[i][j] for j in absorbing] for i in transient]
        identity = [[1.0 if i == j else 0.0 for j in range(len(transient))] for i in range(len(transient))]
        N = _inverse([[identity[i][j] - q[i][j] for j in range(len(transient))] for i in range(len(transient))])
        if N is not None:
            expected = [sum(row) for row in N]
            B = mat_mul(N, r)
            absorption = {
                "states": absorbing,
                "transient": transient,
                "expected_steps": expected,
                "probabilities": B,
            }

    dist_n = None
    if initial is not None:
        if len(initial) != n:
            raise ValueError("La distribución inicial debe tener el mismo tamaño que la matriz.")
        if any(v < -EPS for v in initial):
            raise ValueError("La distribución inicial no puede tener valores negativos.")
        total = sum(initial)
        if total <= EPS:
            raise ValueError("La distribución inicial debe sumar más que cero.")
        initial = [v / total for v in initial]
        dist_n = [
            sum(initial[i] * Pn[i][j] for i in range(n))
            for j in range(n)
        ]

    if pi is not None:
        message = "Se encontró una distribución estacionaria única."
    elif len([c for c in classes if c.recurrent]) > 1:
        message = "Hay varias clases recurrentes: la distribución estacionaria no es única."
    else:
        message = "No se pudo determinar una distribución estacionaria única."

    return MarkovResult(
        n=n,
        steady_state=pi,
        n_step=Pn,
        classes=classes,
        absorbing=absorbing,
        transient=transient,
        irreducible=irreducible,
        aperiodic=aperiodic,
        absorption=absorption,
        message=message,
        initial=initial,
        distribution_n=dist_n,
    )
