"""Modelos de transporte: esquina noroeste, costo mínimo, Vogel y MODI."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import math

EPS = 1e-9


@dataclass
class TransportIteration:
    allocation: list[list[float]]
    basic: list[list[bool]]
    cost: float
    u: list[float] | None = None
    v: list[float] | None = None
    deltas: list[list[float]] | None = None
    entering: tuple[int, int] | None = None
    leaving: tuple[int, int] | None = None
    theta: float | None = None


@dataclass
class TransportResult:
    allocation: list[list[float]]
    basic: list[list[bool]]
    total_cost: float
    iterations: list[TransportIteration]
    status: str
    message: str
    costs: list[list[float]]
    supply: list[float]
    demand: list[float]
    row_names: list[str]
    col_names: list[str]
    method: str
    maximize: bool


def _balance(
    costs: list[list[float]],
    supply: list[float],
    demand: list[float],
    row_names: list[str],
    col_names: list[str],
) -> tuple[list[list[float]], list[float], list[float], list[str], list[str]]:
    costs = [row[:] for row in costs]
    supply = supply[:]
    demand = demand[:]
    row_names = row_names[:]
    col_names = col_names[:]

    total_s = sum(supply)
    total_d = sum(demand)
    if total_s > total_d + EPS:
        for row in costs:
            row.append(0.0)
        demand.append(total_s - total_d)
        col_names.append("Ficticio")
    elif total_d > total_s + EPS:
        costs.append([0.0] * len(costs[0]))
        supply.append(total_d - total_s)
        row_names.append("Ficticio")
    return costs, supply, demand, row_names, col_names


def _northwest(
    costs: list[list[float]], supply: list[float], demand: list[float]
) -> list[list[float]]:
    m, n = len(costs), len(costs[0])
    alloc = [[0.0] * n for _ in range(m)]
    s, d = supply[:], demand[:]
    i = j = 0
    while i < m and j < n:
        if s[i] <= EPS:
            i += 1
            continue
        if d[j] <= EPS:
            j += 1
            continue
        q = min(s[i], d[j])
        alloc[i][j] = q
        s[i] -= q
        d[j] -= q
        if s[i] <= EPS:
            i += 1
        if d[j] <= EPS:
            j += 1
    return alloc


def _least_cost(
    costs: list[list[float]], supply: list[float], demand: list[float]
) -> list[list[float]]:
    m, n = len(costs), len(costs[0])
    alloc = [[0.0] * n for _ in range(m)]
    s, d = supply[:], demand[:]
    while True:
        best = None
        for i in range(m):
            if s[i] <= EPS:
                continue
            for j in range(n):
                if d[j] <= EPS:
                    continue
                if best is None or costs[i][j] < best[0] - EPS:
                    best = (costs[i][j], i, j)
        if best is None:
            break
        _, i, j = best
        q = min(s[i], d[j])
        alloc[i][j] = q
        s[i] -= q
        d[j] -= q
    return alloc


def _vogel(
    costs: list[list[float]], supply: list[float], demand: list[float]
) -> list[list[float]]:
    m, n = len(costs), len(costs[0])
    alloc = [[0.0] * n for _ in range(m)]
    s, d = supply[:], demand[:]

    while True:
        rows = [i for i in range(m) if s[i] > EPS]
        cols = [j for j in range(n) if d[j] > EPS]
        if not rows or not cols:
            break

        penalties: list[tuple[float, str, int]] = []
        for i in rows:
            vals = sorted(costs[i][j] for j in cols)
            pen = vals[1] - vals[0] if len(vals) > 1 else vals[0]
            penalties.append((pen, "row", i))
        for j in cols:
            vals = sorted(costs[i][j] for i in rows)
            pen = vals[1] - vals[0] if len(vals) > 1 else vals[0]
            penalties.append((pen, "col", j))

        # Mayor penalización; en empate se prefiere fila y luego el índice menor.
        _, kind, idx = max(penalties, key=lambda t: (t[0], t[1] == "row", -t[2]))

        if kind == "row":
            j = min(cols, key=lambda c: (costs[idx][c], c))
            q = min(s[idx], d[j])
            alloc[idx][j] = q
            s[idx] -= q
            d[j] -= q
        else:
            i = min(rows, key=lambda r: (costs[r][idx], r))
            q = min(s[i], d[idx])
            alloc[i][idx] = q
            s[i] -= q
            d[idx] -= q

    return alloc


def _complete_basis(
    alloc: list[list[float]], costs: list[list[float]]
) -> list[list[bool]]:
    """Completa la base hasta m+n-1 celdas usando ceros (casos degenerados)."""
    m, n = len(alloc), len(alloc[0])
    basic = [[alloc[i][j] > EPS for j in range(n)] for i in range(m)]

    parent = list(range(m + n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    count = 0
    for i in range(m):
        for j in range(n):
            if basic[i][j]:
                union(i, m + j)
                count += 1

    target = m + n - 1
    # Preferir celdas de menor costo para los ceros de la base.
    candidates = sorted(
        (costs[i][j], i, j)
        for i in range(m)
        for j in range(n)
        if not basic[i][j]
    )
    for _, i, j in candidates:
        if count >= target:
            break
        if find(i) != find(m + j):
            basic[i][j] = True
            alloc[i][j] = 0.0
            union(i, m + j)
            count += 1

    # En teoría nunca ocurre, pero se garantiza el tamaño de la base.
    if count < target:
        for i in range(m):
            for j in range(n):
                if count >= target:
                    break
                if not basic[i][j]:
                    basic[i][j] = True
                    alloc[i][j] = 0.0
                    count += 1

    return basic


def _potentials(
    costs: list[list[float]], basic: list[list[bool]]
) -> tuple[list[float], list[float]]:
    m, n = len(costs), len(costs[0])
    row_edges = [[j for j in range(n) if basic[i][j]] for i in range(m)]
    col_edges = [[i for i in range(m) if basic[i][j]] for j in range(n)]

    u: list[float | None] = [None] * m
    v: list[float | None] = [None] * n

    for start in range(m):
        if u[start] is not None:
            continue
        u[start] = 0.0
        stack: list[tuple[str, int]] = [("r", start)]
        while stack:
            kind, idx = stack.pop()
            if kind == "r":
                for j in row_edges[idx]:
                    if v[j] is None:
                        v[j] = costs[idx][j] - u[idx]  # type: ignore[operator]
                        stack.append(("c", j))
            else:
                for i in col_edges[idx]:
                    if u[i] is None:
                        u[i] = costs[i][idx] - v[idx]  # type: ignore[operator]
                        stack.append(("r", i))

    u = [0.0 if x is None else x for x in u]
    v = [0.0 if x is None else x for x in v]
    return u, v


def _deltas(
    costs: list[list[float]],
    basic: list[list[bool]],
    u: list[float],
    v: list[float],
) -> list[list[float]]:
    m, n = len(costs), len(costs[0])
    return [
        [0.0 if basic[i][j] else costs[i][j] - u[i] - v[j] for j in range(n)]
        for i in range(m)
    ]


def _find_path(
    basic: list[list[bool]], start_row: int, end_col: int
) -> list[tuple[int, int]] | None:
    """Camino en el árbol de celdas básicas desde una fila hasta una columna."""
    m, n = len(basic), len(basic[0])
    start = ("r", start_row)
    target = ("c", end_col)
    parent: dict[tuple[str, int], tuple[str, int] | None] = {start: None}
    queue = deque([start])

    while queue:
        node = queue.popleft()
        if node == target:
            break
        kind, idx = node
        if kind == "r":
            for j in range(n):
                if basic[idx][j]:
                    nxt = ("c", j)
                    if nxt not in parent:
                        parent[nxt] = node
                        queue.append(nxt)
        else:
            for i in range(m):
                if basic[i][idx]:
                    nxt = ("r", i)
                    if nxt not in parent:
                        parent[nxt] = node
                        queue.append(nxt)

    if target not in parent:
        return None

    nodes: list[tuple[str, int]] = []
    cur: tuple[str, int] | None = target
    while cur is not None:
        nodes.append(cur)
        cur = parent[cur]
    nodes.reverse()

    edges: list[tuple[int, int]] = []
    for a, b in zip(nodes, nodes[1:]):
        if a[0] == "r":
            edges.append((a[1], b[1]))
        else:
            edges.append((b[1], a[1]))
    return edges


def _copy(alloc: list[list[float]]) -> list[list[float]]:
    return [row[:] for row in alloc]


def _copy_bool(basic: list[list[bool]]) -> list[list[bool]]:
    return [row[:] for row in basic]


def solve_transport(
    costs: list[list[float]],
    supply: list[float],
    demand: list[float],
    method: str = "vogel",
    row_names: list[str] | None = None,
    col_names: list[str] | None = None,
    maximize: bool = False,
    max_iter: int = 500,
) -> TransportResult:
    """Resuelve un modelo de transporte balanceado o desbalanceado."""
    if not costs or not costs[0]:
        raise ValueError("La matriz de costos está vacía.")
    n = len(costs[0])
    if any(len(row) != n for row in costs):
        raise ValueError("Todas las filas de la matriz de costos deben tener igual longitud.")
    m = len(costs)
    if len(supply) != m:
        raise ValueError("El número de ofertas debe coincidir con las filas de costos.")
    if len(demand) != n:
        raise ValueError("El número de demandas debe coincidir con las columnas de costos.")
    if any(v < -EPS for v in supply + demand):
        raise ValueError("Ofertas y demandas deben ser no negativas.")
    if sum(supply) <= EPS or sum(demand) <= EPS:
        raise ValueError("La oferta y la demanda totales deben ser positivas.")

    original_costs = [[float(v) for v in row] for row in costs]
    supply = [float(v) for v in supply]
    demand = [float(v) for v in demand]
    row_names = row_names[:] if row_names else [f"O{i + 1}" for i in range(m)]
    col_names = col_names[:] if col_names else [f"D{j + 1}" for j in range(n)]
    if len(row_names) != m:
        row_names = [f"O{i + 1}" for i in range(m)]
    if len(col_names) != n:
        col_names = [f"D{j + 1}" for j in range(n)]

    costs_b, supply_b, demand_b, row_names_b, col_names_b = _balance(
        original_costs, supply, demand, row_names, col_names
    )
    # El problema de maximización se transforma minimizando costos negativos.
    solve_costs = [[-v for v in row] for row in costs_b] if maximize else costs_b

    method_key = method.strip().lower()
    if method_key in ("vogel", "vog"):
        initial = _vogel(solve_costs, supply_b, demand_b)
        method_label = "Aproximación de Vogel"
    elif method_key in ("costo minimo", "costo mínimo", "least", "minimo"):
        initial = _least_cost(solve_costs, supply_b, demand_b)
        method_label = "Costo mínimo"
    elif method_key in ("noroeste", "esquina noroeste", "northwest"):
        initial = _northwest(solve_costs, supply_b, demand_b)
        method_label = "Esquina noroeste"
    else:
        raise ValueError("Método inicial no válido. Use Vogel, costo mínimo o noroeste.")

    basic = _complete_basis(initial, solve_costs)
    alloc = _copy(initial)
    iterations: list[TransportIteration] = []

    def original_cost(a: list[list[float]]) -> float:
        return sum(
            costs_b[i][j] * a[i][j]
            for i in range(len(costs_b))
            for j in range(len(costs_b[0]))
        )

    u, v = _potentials(solve_costs, basic)
    deltas = _deltas(solve_costs, basic, u, v)
    iterations.append(
        TransportIteration(
            allocation=_copy(alloc),
            basic=_copy_bool(basic),
            cost=original_cost(alloc),
            u=u[:],
            v=v[:],
            deltas=deltas,
        )
    )

    status = "optimo"
    for _ in range(max_iter):
        u, v = _potentials(solve_costs, basic)
        deltas = _deltas(solve_costs, basic, u, v)

        entering = None
        for i in range(len(solve_costs)):
            for j in range(len(solve_costs[0])):
                if not basic[i][j] and deltas[i][j] < -1e-7:
                    if entering is None or deltas[i][j] < deltas[entering[0]][entering[1]] - 1e-12:
                        entering = (i, j)

        if entering is None:
            status = "optimo"
            break

        er, ec = entering
        path = _find_path(basic, er, ec)
        if path is None:
            status = "error"
            break

        cycle = [(er, ec)] + list(reversed(path))
        minus_cells = [cell for idx, cell in enumerate(cycle) if idx % 2 == 1]
        theta = min(alloc[r][c] for r, c in minus_cells)
        leaving = min(minus_cells, key=lambda cell: alloc[cell[0]][cell[1]])

        for idx, (r, c) in enumerate(cycle):
            if idx % 2 == 0:
                alloc[r][c] += theta
            else:
                alloc[r][c] -= theta
                if abs(alloc[r][c]) < 1e-9:
                    alloc[r][c] = 0.0

        basic[leaving[0]][leaving[1]] = False
        alloc[leaving[0]][leaving[1]] = 0.0
        basic[er][ec] = True
        alloc[er][ec] = max(alloc[er][ec], 0.0)

        u, v = _potentials(solve_costs, basic)
        deltas = _deltas(solve_costs, basic, u, v)
        iterations.append(
            TransportIteration(
                allocation=_copy(alloc),
                basic=_copy_bool(basic),
                cost=original_cost(alloc),
                u=u[:],
                v=v[:],
                deltas=deltas,
                entering=entering,
                leaving=leaving,
                theta=theta,
            )
        )
    else:
        status = "limite_iteraciones"

    if status == "optimo":
        msg = "Solución óptima verificada con el método MODI (u, v)."
        if maximize:
            msg += " Se maximizó la ganancia transformando los costos."
    elif status == "error":
        msg = "No se pudo construir el ciclo de compensación; revise los datos."
    else:
        msg = "Se alcanzó el límite de iteraciones antes de verificar la optimalidad."

    return TransportResult(
        allocation=alloc,
        basic=basic,
        total_cost=original_cost(alloc),
        iterations=iterations,
        status=status,
        message=msg,
        costs=costs_b,
        supply=supply_b,
        demand=demand_b,
        row_names=row_names_b,
        col_names=col_names_b,
        method=method_label,
        maximize=maximize,
    )
