import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from compact_mmr.core import MerkleMountainRange


class TestMerkleMountainRange(unittest.TestCase):
    def setUp(self):
        self.mmr = MerkleMountainRange()

    def test_empty_mmr_root(self):
        root = self.mmr.get_root_commitment()
        self.assertEqual(len(root), 64)

    def test_append_single_leaf(self):
        idx = self.mmr.append("event_001")
        self.assertEqual(idx, 0)
        self.assertEqual(len(self.mmr.leaf_indices), 1)
        self.assertTrue(self.mmr.verify_leaf(0, "event_001"))
        self.assertFalse(self.mmr.verify_leaf(0, "tampered_event"))

    def test_append_multiple_peaks_and_merge(self):
        # Appending 4 leaves triggers multiple levels of subtree merges
        for i in range(4):
            self.mmr.append(f"block_tx_{i}")
        self.assertEqual(len(self.mmr.leaf_indices), 4)
        for i in range(4):
            self.assertTrue(self.mmr.verify_leaf(i, f"block_tx_{i}"))

        root = self.mmr.get_root_commitment()
        self.assertEqual(len(root), 64)

    def test_out_of_bounds_verification(self):
        self.assertFalse(self.mmr.verify_leaf(99, "non_existent"))


if __name__ == "__main__":
    unittest.main()
