"""Modelos de inventario: EOQ, EOQ con faltantes y lote de producción (EPQ)."""

from __future__ import annotations

from dataclasses import dataclass
import math


@dataclass
class InventoryResult:
    model: str
    q: float
    orders_per_year: float
    cycle_time: float
    total_cost: float
    ordering_cost: float
    holding_cost: float
    shortage_cost: float
    max_inventory: float
    max_shortage: float
    note: str


def solve_inventory(
    model: str,
    demand: float,
    order_cost: float,
    holding_cost: float,
    shortage_cost: float | None = None,
    production_rate: float | None = None,
) -> InventoryResult:
    """Calcula la política óptima de inventario.

    Las unidades de tiempo son anuales. D es la demanda anual, S el costo de
    ordenar, H el costo de mantener una unidad un año y B el costo de faltante.
    """
    if demand <= 0:
        raise ValueError("La demanda anual D debe ser mayor que cero.")
    if order_cost <= 0:
        raise ValueError("El costo de ordenar S debe ser mayor que cero.")
    if holding_cost <= 0:
        raise ValueError("El costo de mantener H debe ser mayor que cero.")

    key = model.strip().lower()
    if key in ("eoq", "básico", "basico", "eoq básico", "eoq basico", "lote económico", "lote economico"):
        q = math.sqrt(2 * demand * order_cost / holding_cost)
        orders = demand / q
        cycle = q / demand
        ordering = demand * order_cost / q
        holding = holding_cost * q / 2
        return InventoryResult(
            model="EOQ básico",
            q=q,
            orders_per_year=orders,
            cycle_time=cycle,
            total_cost=ordering + holding,
            ordering_cost=ordering,
            holding_cost=holding,
            shortage_cost=0.0,
            max_inventory=q,
            max_shortage=0.0,
            note="Lote económico clásico sin faltantes y con demanda constante.",
        )

    if key in ("eoq con faltantes", "faltantes", "backorder", "eoq faltantes"):
        if shortage_cost is None or shortage_cost <= 0:
            raise ValueError("El costo de faltante B debe ser mayor que cero.")
        b = shortage_cost
        q = math.sqrt(2 * demand * order_cost * (holding_cost + b) / (holding_cost * b))
        shortage = q * holding_cost / (holding_cost + b)
        max_inventory = q - shortage
        orders = demand / q
        cycle = q / demand
        ordering = demand * order_cost / q
        holding = holding_cost * max_inventory ** 2 / (2 * q)
        shortage_cost_total = b * shortage ** 2 / (2 * q)
        return InventoryResult(
            model="EOQ con faltantes",
            q=q,
            orders_per_year=orders,
            cycle_time=cycle,
            total_cost=ordering + holding + shortage_cost_total,
            ordering_cost=ordering,
            holding_cost=holding,
            shortage_cost=shortage_cost_total,
            max_inventory=max_inventory,
            max_shortage=shortage,
            note="Se permite déficit; el faltante se satisface después.",
        )

    if key in (
        "epq",
        "producción",
        "produccion",
        "lote de producción",
        "lote de produccion",
        "epq (producción)",
        "epq (produccion)",
        "lote de producción (epq)",
        "lote de produccion (epq)",
    ):
        if production_rate is None or production_rate <= demand:
            raise ValueError("La tasa de producción p debe ser mayor que la demanda D.")
        p = production_rate
        factor = 1 - demand / p
        q = math.sqrt(2 * demand * order_cost / (holding_cost * factor))
        max_inventory = q * factor
        orders = demand / q
        cycle = q / demand
        ordering = demand * order_cost / q
        holding = holding_cost * max_inventory / 2
        return InventoryResult(
            model="Lote de producción (EPQ)",
            q=q,
            orders_per_year=orders,
            cycle_time=cycle,
            total_cost=ordering + holding,
            ordering_cost=ordering,
            holding_cost=holding,
            shortage_cost=0.0,
            max_inventory=max_inventory,
            max_shortage=0.0,
            note="Producción y consumo simultáneos; no se permiten faltantes.",
        )

    raise ValueError("Modelo de inventario no reconocido.")
