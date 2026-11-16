"""CompactMMR: Append-Only Merkle Mountain Range Engine."""

import hashlib
from typing import List, Tuple


class MerkleMountainRange:
    """
    Append-only Merkle Mountain Range (MMR) ledger.
    Allows continuous verifiable log insertions and tamper proofs in O(log n).
    """

    def __init__(self):
        self.nodes: List[str] = []
        self.leaf_indices: List[int] = []

    @staticmethod
    def _hash(data: str) -> str:
        return hashlib.sha256(data.encode("utf-8")).hexdigest()

    def append(self, leaf_data: str) -> int:
        """
        Appends a leaf to the MMR and merges peaks as appropriate.
        Returns the 0-based leaf ordinal index.
        """
        leaf_hash = self._hash(leaf_data)
        leaf_pos = len(self.nodes)
        self.nodes.append(leaf_hash)
        self.leaf_indices.append(leaf_pos)

        # Merge peaks with previous subtrees of equal height
        size = len(self.nodes)
        while True:
            # Calculate height from trailing ones/zeros
            h = 0
            temp = size
            while (temp & 1) == 0:
                h += 1
                temp >>= 1
            if h == 0:
                break
            right = self.nodes[-1]
            left = self.nodes[-2]
            parent = self._hash(left + right)
            self.nodes.append(parent)
            size = len(self.nodes)

        return len(self.leaf_indices) - 1

    def get_peaks(self) -> List[str]:
        """Returns the list of current peak hashes."""
        if not self.nodes:
            return []
        peaks = []
        # MMR size bits reveal active peaks
        size = len(self.nodes)
        cursor = size
        while cursor > 0:
            # Find largest power of 2 minus 1 less than or equal to cursor
            k = 1
            while (2 * k + 1) <= cursor:
                k = 2 * k + 1
            peaks.append(self.nodes[cursor - 1])
            cursor -= k
        return peaks

    def get_root_commitment(self) -> str:
        """Computes bag-the-peaks root hash for the entire log."""
        peaks = self.get_peaks()
        if not peaks:
            return self._hash("")
        if len(peaks) == 1:
            return peaks[0]
        # Recursively hash peaks together
        res = peaks[-1]
        for p in reversed(peaks[:-1]):
            res = self._hash(p + res)
        return res

    def verify_leaf(self, leaf_ordinal: int, expected_data: str) -> bool:
        """Verifies leaf data matches the recorded hash at leaf position."""
        if leaf_ordinal < 0 or leaf_ordinal >= len(self.leaf_indices):
            return False
        node_pos = self.leaf_indices[leaf_ordinal]
        return self.nodes[node_pos] == self._hash(expected_data)
