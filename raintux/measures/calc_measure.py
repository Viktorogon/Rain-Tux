"""Formula / conditional evaluator for Rainmeter ``Formula=`` strings."""

from __future__ import annotations

from pathlib import Path

from raintux.measures.base_measure import BaseMeasure


class CalcMeasure(BaseMeasure):
    """
    Evaluate expressions and ``(condition ? a : b)`` syntax.

    TODO: wire measure references and safe math.
    """

    async def _poll(self) -> float:
        return 0.0
