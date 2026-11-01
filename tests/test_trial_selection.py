# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) 2025-2026  Philipp Emanuel Weidmann <pew@worldwidemann.com> + contributors

import unittest

from heretic.trial_selection import select_pareto_trial


class SelectParetoTrialTests(unittest.TestCase):
    def test_zero_based_selection_uses_sorted_position(self):
        trials = ["trial-8", "trial-2", "trial-5"]
        self.assertEqual(select_pareto_trial(trials, 0), "trial-8")
        self.assertEqual(select_pareto_trial(trials, 2), "trial-5")

    def test_out_of_range_reports_valid_indices(self):
        with self.assertRaisesRegex(
            ValueError, r"Invalid --trial-index 3:.*valid indices: 0\.\.2"
        ):
            select_pareto_trial(["a", "b", "c"], 3)

    def test_negative_index_is_not_silently_wrapped(self):
        with self.assertRaisesRegex(ValueError, r"Invalid --trial-index -1"):
            select_pareto_trial(["a"], -1)

    def test_empty_pareto_front_has_no_valid_index(self):
        with self.assertRaisesRegex(ValueError, r"valid indices: none"):
            select_pareto_trial([], 0)


if __name__ == "__main__":
    unittest.main()
