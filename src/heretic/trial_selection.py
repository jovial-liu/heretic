# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025-2026  Philipp Emanuel Weidmann <pew@worldwidemann.com> + contributors

from collections.abc import Sequence
from typing import TypeVar

T = TypeVar("T")


def select_pareto_trial(trials: Sequence[T], index: int) -> T:
    """Select by zero-based Pareto-front position, not the displayed trial number."""
    if not 0 <= index < len(trials):
        valid = f"0..{len(trials) - 1}" if trials else "none"
        raise ValueError(
            f"Invalid --trial-index {index}: the Pareto front has {len(trials)} "
            f"trial(s); valid indices: {valid}."
        )
    return trials[index]
