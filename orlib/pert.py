"""PERT/CPM: tiempos esperados, ruta crítica y probabilidad de terminación."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
import math


@dataclass
class Activity:
    name: str
    optimistic: float
    most_likely: float
    pessimistic: float
    predecessors: list[str]

    @property
    def expected(self) -> float:
        return (self.optimistic + 4 * self.most_likely + self.pessimistic) / 6

    @property
    def variance(self) -> float:
        return ((self.pessimistic - self.optimistic) / 6) ** 2


@dataclass
class PertRow:
    name: str
    duration: float
    variance: float
    es: float
    ef: float
    ls: float
    lf: float
    slack: float
    critical: bool


@dataclass
class PertResult:
    rows: list[PertRow]
    duration: float
    variance: float
    std: float
    critical_path: list[str]
    probability: float | None
    target: float | None
    message: str


def solve_pert(activities: list[Activity], target: float | None = None) -> PertResult:
    if not activities:
        raise ValueError("Debe registrar al menos una actividad.")
    names = [a.name.strip() for a in activities]
    if any(not name for name in names):
        raise ValueError("Todas las actividades deben tener nombre.")
    if len(set(names)) != len(names):
        raise ValueError("Los nombres de las actividades deben ser únicos.")
    for a in activities:
        if a.optimistic < 0 or a.most_likely < 0 or a.pessimistic < 0:
            raise ValueError(f"La actividad {a.name} tiene duraciones negativas.")
        if not (a.optimistic <= a.most_likely <= a.pessimistic):
            raise ValueError(
                f"En la actividad {a.name} debe cumplirse optimista <= probable <= pesimista."
            )

    index = {name: i for i, name in enumerate(names)}
    n = len(activities)
    successors: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n

    for i, a in enumerate(activities):
        for pred in a.predecessors:
            pred = pred.strip()
            if not pred or pred == "-":
                continue
            if pred not in index:
                raise ValueError(f"La actividad {a.name} tiene un predecesor desconocido: {pred}.")
            p = index[pred]
            successors[p].append(i)
            indegree[i] += 1

    # Orden topológico (Kahn).
    queue = deque([i for i in range(n) if indegree[i] == 0])
    order: list[int] = []
    while queue:
        u = queue.popleft()
        order.append(u)
        for v in successors[u]:
            indegree[v] -= 1
            if indegree[v] == 0:
                queue.append(v)
    if len(order) != n:
        raise ValueError("Hay un ciclo en las dependencias: el proyecto no es válido.")

    es = [0.0] * n
    ef = [0.0] * n
    for u in order:
        es[u] = max((ef[p] for p in range(n) if u in successors[p]), default=0.0)
        ef[u] = es[u] + activities[u].expected

    duration = max(ef) if ef else 0.0
    ls = [duration] * n
    lf = [duration] * n
    for u in reversed(order):
        if successors[u]:
            lf[u] = min(ls[v] for v in successors[u])
        else:
            lf[u] = duration
        ls[u] = lf[u] - activities[u].expected

    rows: list[PertRow] = []
    for i, a in enumerate(activities):
        slack = ls[i] - es[i]
        rows.append(
            PertRow(
                name=a.name,
                duration=a.expected,
                variance=a.variance,
                es=es[i],
                ef=ef[i],
                ls=ls[i],
                lf=lf[i],
                slack=0.0 if abs(slack) < 1e-9 else slack,
                critical=abs(slack) < 1e-7,
            )
        )

    # Ruta crítica: seguir actividades críticas encadenadas desde el inicio.
    starts = [i for i in range(n) if rows[i].critical and abs(es[i]) < 1e-7]
    path: list[int] = []
    if starts:
        current = min(starts, key=lambda i: names[i])
        visited: set[int] = set()
        while current not in visited:
            visited.add(current)
            path.append(current)
            candidates = [
                v
                for v in successors[current]
                if rows[v].critical and abs(es[v] - ef[current]) < 1e-7
            ]
            if not candidates:
                break
            current = min(candidates, key=lambda i: names[i])

    variance = sum(activities[i].variance for i in path) if path else 0.0
    std = math.sqrt(variance)

    probability = None
    if target is not None:
        if std < 1e-12:
            probability = 1.0 if target >= duration - 1e-9 else 0.0
        else:
            z = (target - duration) / std
            probability = 0.5 * (1 + math.erf(z / math.sqrt(2)))

    msg = "Cronograma PERT calculado."
    if not path:
        msg += " No se pudo reconstruir una ruta crítica única."

    return PertResult(
        rows=rows,
        duration=duration,
        variance=variance,
        std=std,
        critical_path=[names[i] for i in path],
        probability=probability,
        target=target,
        message=msg,
    )
