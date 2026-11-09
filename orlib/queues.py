"""Teoría de colas: modelos M/M/1, M/M/1/K, M/M/c, M/M/c/K y M/G/1."""

from __future__ import annotations

import math
from typing import Any


def _require_positive(**kwargs: float) -> None:
    for name, value in kwargs.items():
        if value is None or value <= 0:
            raise ValueError(f"{name} debe ser mayor que cero.")


def _pn_mmc(a: float, c: int, p0: float, max_n: int = 15) -> list[float]:
    values = []
    for n in range(max_n + 1):
        if n < c:
            pn = p0 * (a ** n) / math.factorial(n)
        else:
            pn = p0 * (a ** n) / (math.factorial(c) * (c ** (n - c)))
        values.append(pn)
    return values


def solve_queue(
    model: str,
    lam: float,
    mu: float,
    c: int = 1,
    K: int | None = None,
    sigma: float | None = None,
) -> dict[str, Any]:
    """Calcula las medidas de desempeño de un modelo de colas.

    Las unidades de tiempo son las mismas que las de lambda y mu. Por ejemplo,
    si lambda y mu están en clientes/hora, W y Wq se expresan en horas.
    """
    model = model.strip().upper()
    _require_positive(lam=lam, mu=mu)
    c = int(c)

    if model == "M/M/1":
        if lam >= mu:
            raise ValueError("Para M/M/1 se requiere lambda < mu (sistema estable).")
        rho = lam / mu
        p0 = 1 - rho
        lq = rho ** 2 / (1 - rho)
        l = rho / (1 - rho)
        w = 1 / (mu - lam)
        wq = lam / (mu * (mu - lam))
        metrics = {
            "rho": rho,
            "P0": p0,
            "L": l,
            "Lq": lq,
            "W": w,
            "Wq": wq,
            "P_espera": rho,
            "lambda_efectiva": lam,
            "P_rechazo": 0.0,
        }
        pn = [p0 * rho ** n for n in range(16)]
        note = "Cola infinita, un servidor, llegadas y servicios exponenciales."

    elif model == "M/M/1/K":
        if K is None or int(K) < 1:
            raise ValueError("K debe ser un entero mayor o igual a 1.")
        K = int(K)
        rho = lam / mu
        if abs(rho - 1) < 1e-12:
            p0 = 1 / (K + 1)
        else:
            p0 = (1 - rho) / (1 - rho ** (K + 1))
        pn = [p0 * rho ** n for n in range(K + 1)]
        l = sum(n * pn[n] for n in range(K + 1))
        lq = l - (1 - p0)
        pk = pn[K]
        lam_eff = lam * (1 - pk)
        if lam_eff <= 1e-12:
            raise ValueError("La tasa efectiva de llegada es cero; revise lambda y K.")
        w = l / lam_eff
        wq = lq / lam_eff
        metrics = {
            "rho": rho,
            "P0": p0,
            "L": l,
            "Lq": lq,
            "W": w,
            "Wq": wq,
            "P_espera": 1 - p0,
            "lambda_efectiva": lam_eff,
            "P_rechazo": pk,
        }
        note = f"Cola finita con capacidad K={K} (incluye el cliente en servicio)."

    elif model in ("M/M/C", "M/M/C/∞"):
        if c < 1:
            raise ValueError("c debe ser un entero mayor o igual a 1.")
        rho = lam / (c * mu)
        if rho >= 1:
            raise ValueError("Para M/M/c se requiere lambda < c*mu (sistema estable).")
        a = lam / mu
        p0 = 1 / (
            sum(a ** n / math.factorial(n) for n in range(c))
            + (a ** c) / (math.factorial(c) * (1 - rho))
        )
        lq = p0 * (a ** c) * rho / (math.factorial(c) * (1 - rho) ** 2)
        l = lq + a
        wq = lq / lam
        w = wq + 1 / mu
        p_wait = p0 * (a ** c) / (math.factorial(c) * (1 - rho))
        metrics = {
            "rho": rho,
            "P0": p0,
            "L": l,
            "Lq": lq,
            "W": w,
            "Wq": wq,
            "P_espera": p_wait,
            "lambda_efectiva": lam,
            "P_rechazo": 0.0,
        }
        pn = _pn_mmc(a, c, p0, max(15, c + 5))
        note = f"Cola infinita con c={c} servidores en paralelo."

    elif model in ("M/M/C/K", "M/M/C/K/∞"):
        if c < 1:
            raise ValueError("c debe ser un entero mayor o igual a 1.")
        if K is None or int(K) < c:
            raise ValueError("K debe ser un entero mayor o igual a c.")
        K = int(K)
        a = lam / mu
        rho = a / c
        sum1 = sum(a ** n / math.factorial(n) for n in range(c))
        sum2 = (a ** c / math.factorial(c)) * sum(rho ** k for k in range(K - c + 1))
        p0 = 1 / (sum1 + sum2)
        pn = []
        for n in range(K + 1):
            if n < c:
                pn.append(p0 * a ** n / math.factorial(n))
            else:
                pn.append(p0 * a ** n / (math.factorial(c) * c ** (n - c)))
        l = sum(n * pn[n] for n in range(K + 1))
        lq = sum((n - c) * pn[n] for n in range(c, K + 1))
        pk = pn[K]
        lam_eff = lam * (1 - pk)
        if lam_eff <= 1e-12:
            raise ValueError("La tasa efectiva de llegada es cero; revise lambda y K.")
        w = l / lam_eff
        wq = lq / lam_eff
        metrics = {
            "rho": rho,
            "P0": p0,
            "L": l,
            "Lq": lq,
            "W": w,
            "Wq": wq,
            "P_espera": sum(pn[c:]),
            "lambda_efectiva": lam_eff,
            "P_rechazo": pk,
        }
        note = f"Cola finita con c={c} servidores y capacidad K={K}."

    elif model in ("M/G/1", "MG1"):
        if lam >= mu:
            raise ValueError("Para M/G/1 se requiere lambda < mu (sistema estable).")
        if sigma is None or sigma < 0:
            raise ValueError("La desviación estándar del servicio debe ser >= 0.")
        rho = lam / mu
        lq = (rho ** 2 + (lam ** 2) * (sigma ** 2)) / (2 * (1 - rho))
        l = lq + rho
        wq = lq / lam
        w = wq + 1 / mu
        p0 = 1 - rho
        metrics = {
            "rho": rho,
            "P0": p0,
            "L": l,
            "Lq": lq,
            "W": w,
            "Wq": wq,
            "P_espera": rho,
            "lambda_efectiva": lam,
            "P_rechazo": 0.0,
        }
        pn = None
        note = (
            "Fórmula de Pollaczek-Khinchine. Las probabilidades Pn no quedan "
            "determinadas solo con la media y la desviación del servicio."
        )
    else:
        raise ValueError("Modelo no reconocido.")

    return {
        "model": model,
        "metrics": metrics,
        "pn": pn,
        "note": note,
        "lambda": lam,
        "mu": mu,
        "c": c,
        "K": K,
        "sigma": sigma,
    }
