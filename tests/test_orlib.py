"""Pruebas del motor de cálculo (sin interfaz gráfica)."""

from __future__ import annotations

import math
import unittest

from orlib.assignment import hungarian
from orlib.graphic import solve_graphic
from orlib.inventory import solve_inventory
from orlib.markov import analyze
from orlib.pert import Activity, solve_pert
from orlib.queues import solve_queue
from orlib.simplex import simplex_solve
from orlib.transport import solve_transport


class TestSimplex(unittest.TestCase):
    def test_maximization(self):
        result = simplex_solve(
            [3, 5],
            [[1, 0], [0, 2], [3, 2]],
            ["<=", "<=", "<="],
            [4, 12, 18],
            maximize=True,
        )
        self.assertEqual(result.status, "optimo")
        self.assertAlmostEqual(result.value, 36.0)
        self.assertAlmostEqual(result.solution[0], 2.0)
        self.assertAlmostEqual(result.solution[1], 6.0)

    def test_minimization(self):
        result = simplex_solve(
            [2, 3],
            [[1, 1], [1, 3]],
            [">=", ">="],
            [4, 6],
            maximize=False,
        )
        self.assertEqual(result.status, "optimo")
        self.assertAlmostEqual(result.value, 9.0)
        self.assertAlmostEqual(result.solution[0], 3.0)
        self.assertAlmostEqual(result.solution[1], 1.0)

    def test_equalities(self):
        result = simplex_solve(
            [1, 2],
            [[1, 1], [1, -1]],
            ["=", "="],
            [4, 2],
            maximize=False,
        )
        self.assertEqual(result.status, "optimo")
        self.assertAlmostEqual(result.value, 5.0)
        self.assertAlmostEqual(result.solution[0], 3.0)
        self.assertAlmostEqual(result.solution[1], 1.0)

    def test_two_phase(self):
        result = simplex_solve(
            [2, 3],
            [[1, 1], [1, 2], [0, 1]],
            [">=", "<=", "<="],
            [4, 10, 4],
            maximize=True,
        )
        self.assertEqual(result.status, "optimo")
        self.assertAlmostEqual(result.value, 20.0)
        self.assertAlmostEqual(result.solution[0], 10.0)
        self.assertAlmostEqual(result.solution[1], 0.0)

    def test_infeasible(self):
        result = simplex_solve(
            [1, 1],
            [[1, 1], [1, 1]],
            [">=", "<="],
            [5, 3],
            maximize=True,
        )
        self.assertEqual(result.status, "infactible")

    def test_unbounded(self):
        result = simplex_solve(
            [1, 1],
            [[1, -1]],
            ["<="],
            [1],
            maximize=True,
        )
        self.assertEqual(result.status, "no_acotado")


class TestGraphic(unittest.TestCase):
    def test_optimum(self):
        result = solve_graphic(
            (3, 5),
            [(1, 0, "<=", 4), (0, 2, "<=", 12), (3, 2, "<=", 18)],
            maximize=True,
        )
        self.assertEqual(result.status, "optimo")
        self.assertAlmostEqual(result.value, 36.0)
        self.assertAlmostEqual(result.point[0], 2.0)
        self.assertAlmostEqual(result.point[1], 6.0)
        self.assertTrue(result.bounded)
        self.assertGreaterEqual(len(result.vertices), 5)

    def test_infeasible(self):
        result = solve_graphic(
            (1, 1),
            [(1, 0, "<=", 1), (1, 0, ">=", 2)],
            maximize=True,
        )
        self.assertEqual(result.status, "infactible")

    def test_unbounded(self):
        result = solve_graphic((1, 1), [(1, -1, "<=", 1)], maximize=True)
        self.assertEqual(result.status, "no_acotado")

    def test_unbounded_region_with_finite_optimum(self):
        result = solve_graphic(
            (1, 1),
            [(1, 0, ">=", 2), (0, 1, ">=", 1)],
            maximize=False,
        )
        self.assertEqual(result.status, "optimo")
        self.assertAlmostEqual(result.value, 3.0)
        self.assertFalse(result.bounded)


class TestTransport(unittest.TestCase):
    def test_vogel_and_modi(self):
        result = solve_transport(
            [[8, 6, 10, 9], [9, 12, 13, 7], [14, 9, 16, 5]],
            [35, 50, 40],
            [45, 20, 30, 30],
            method="Vogel",
        )
        self.assertEqual(result.status, "optimo")
        self.assertAlmostEqual(result.total_cost, 1020.0)
        self.assertTrue(
            all(delta >= -1e-7 for row in result.iterations[-1].deltas for delta in row)
        )

    def test_degenerate_case(self):
        result = solve_transport(
            [[11, 7, 12, 13], [2, 2, 2, 5], [9, 10, 4, 7]],
            [5, 4, 10],
            [1, 9, 8, 1],
            method="Costo mínimo",
        )
        self.assertEqual(result.status, "optimo")
        self.assertAlmostEqual(result.total_cost, 91.0)

    def test_unbalanced(self):
        result = solve_transport(
            [[4, 6], [5, 3]],
            [10, 5],
            [7, 4],
            method="Vogel",
        )
        self.assertEqual(result.status, "optimo")
        self.assertEqual(len(result.supply), 2)
        self.assertEqual(len(result.demand), 3)
        self.assertAlmostEqual(sum(result.supply), sum(result.demand))

    def test_maximization(self):
        result = solve_transport(
            [[5, 8, 4], [6, 7, 9]],
            [100, 120],
            [80, 70, 70],
            method="Vogel",
            maximize=True,
        )
        self.assertEqual(result.status, "optimo")
        self.assertAlmostEqual(result.total_cost, 1640.0)


class TestAssignment(unittest.TestCase):
    def test_minimization(self):
        result = hungarian([[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]])
        self.assertAlmostEqual(result.total_cost, 13.0)
        self.assertEqual(result.assignment, [1, 0, 2, 3])

    def test_maximization(self):
        result = hungarian(
            [[9, 2, 7, 8], [6, 4, 3, 7], [5, 8, 1, 8], [7, 6, 9, 4]],
            maximize=True,
        )
        self.assertAlmostEqual(result.total_cost, 33.0)

    def test_rectangular(self):
        result = hungarian([[1, 2, 3], [4, 5, 6]])
        self.assertEqual(len(result.assignment), 2)
        self.assertIsNotNone(result.assignment[0])
        self.assertIsNotNone(result.assignment[1])


class TestQueues(unittest.TestCase):
    def test_mm1(self):
        result = solve_queue("M/M/1", 2, 3)
        metrics = result["metrics"]
        self.assertAlmostEqual(metrics["rho"], 2 / 3)
        self.assertAlmostEqual(metrics["L"], 2.0)
        self.assertAlmostEqual(metrics["Lq"], 4 / 3)
        self.assertAlmostEqual(metrics["W"], 1.0)
        self.assertAlmostEqual(metrics["Wq"], 2 / 3)

    def test_mmc(self):
        result = solve_queue("M/M/c", 8, 4, c=3)
        metrics = result["metrics"]
        self.assertAlmostEqual(metrics["rho"], 2 / 3)
        self.assertAlmostEqual(metrics["L"], 26 / 9, places=6)
        self.assertAlmostEqual(metrics["Lq"], 8 / 9, places=6)

    def test_finite_capacity(self):
        result = solve_queue("M/M/1/K", 3, 4, K=5)
        metrics = result["metrics"]
        self.assertAlmostEqual(sum(result["pn"]), 1.0, places=9)
        self.assertAlmostEqual(metrics["P_rechazo"], result["pn"][5], places=9)
        self.assertAlmostEqual(
            metrics["lambda_efectiva"], 3 * (1 - metrics["P_rechazo"]), places=9
        )

    def test_mg1(self):
        result = solve_queue("M/G/1", 3, 4, sigma=1.2)
        metrics = result["metrics"]
        expected_lq = (0.75 ** 2 + 3 ** 2 * 1.2 ** 2) / (2 * (1 - 0.75))
        self.assertAlmostEqual(metrics["Lq"], expected_lq)

    def test_unstable(self):
        with self.assertRaises(ValueError):
            solve_queue("M/M/1", 5, 3)


class TestMarkov(unittest.TestCase):
    def test_steady_state(self):
        result = analyze([[0.7, 0.3], [0.4, 0.6]], initial=[1, 0], steps=3)
        self.assertAlmostEqual(result.steady_state[0], 4 / 7)
        self.assertAlmostEqual(result.steady_state[1], 3 / 7)
        # Distribución tras 3 pasos = primera fila de P^3.
        self.assertAlmostEqual(result.distribution_n[0], 0.583)
        self.assertAlmostEqual(result.distribution_n[1], 0.417)

    def test_periodic_chain(self):
        result = analyze([[0, 1], [1, 0]])
        self.assertEqual(result.classes[0].period, 2)
        self.assertFalse(result.aperiodic)
        self.assertAlmostEqual(result.steady_state[0], 0.5)

    def test_absorbing_chain(self):
        result = analyze([[1, 0], [0.3, 0.7]])
        self.assertEqual(result.absorbing, [0])
        self.assertEqual(result.transient, [1])
        self.assertAlmostEqual(result.absorption["expected_steps"][0], 1 / 0.3)
        self.assertAlmostEqual(result.absorption["probabilities"][0][0], 1.0)

    def test_two_absorbing_states(self):
        result = analyze([[1, 0, 0], [0, 1, 0], [0.2, 0.3, 0.5]])
        self.assertIsNone(result.steady_state)
        self.assertAlmostEqual(result.absorption["probabilities"][0][0], 0.4)
        self.assertAlmostEqual(result.absorption["probabilities"][0][1], 0.6)

    def test_invalid_rows(self):
        with self.assertRaises(ValueError):
            analyze([[0.5, 0.4], [0.2, 0.8]])


class TestPert(unittest.TestCase):
    def test_critical_path(self):
        activities = [
            Activity("A", 2, 4, 6, []),
            Activity("B", 3, 5, 8, ["A"]),
            Activity("C", 4, 6, 9, ["A"]),
            Activity("D", 2, 3, 5, ["B", "C"]),
        ]
        result = solve_pert(activities, target=16)
        self.assertAlmostEqual(result.duration, 40 / 3)
        self.assertEqual(result.critical_path, ["A", "C", "D"])
        self.assertGreater(result.probability, 0.98)

    def test_cycle_detection(self):
        activities = [
            Activity("A", 1, 1, 1, ["B"]),
            Activity("B", 1, 1, 1, ["A"]),
        ]
        with self.assertRaises(ValueError):
            solve_pert(activities)


class TestInventory(unittest.TestCase):
    def test_eoq(self):
        result = solve_inventory("EOQ", 1200, 50, 2)
        self.assertAlmostEqual(result.q, math.sqrt(2 * 1200 * 50 / 2))
        self.assertAlmostEqual(result.total_cost, math.sqrt(2 * 1200 * 50 * 2))
        self.assertEqual(result.max_shortage, 0.0)

    def test_eoq_shortage(self):
        result = solve_inventory("EOQ con faltantes", 1200, 50, 2, shortage_cost=8)
        self.assertAlmostEqual(result.q, math.sqrt(2 * 1200 * 50 * 10 / (2 * 8)))
        self.assertAlmostEqual(
            result.max_shortage, result.q * 2 / (2 + 8)
        )

    def test_epq(self):
        result = solve_inventory("EPQ", 1200, 50, 2, production_rate=2000)
        factor = 1 - 1200 / 2000
        self.assertAlmostEqual(result.q, math.sqrt(2 * 1200 * 50 / (2 * factor)))
        self.assertAlmostEqual(result.max_inventory, result.q * factor)

    def test_invalid(self):
        with self.assertRaises(ValueError):
            solve_inventory("EOQ", 0, 50, 2)
        with self.assertRaises(ValueError):
            solve_inventory("EPQ", 1200, 50, 2, production_rate=1000)


if __name__ == "__main__":
    unittest.main()
