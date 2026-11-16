# CompactMMR: Append-Only Merkle Mountain Range Ledger

A zero-dependency cryptographic ledger based on Merkle Mountain Ranges (MMR) for immutable audit trails and verifiable inclusion proofs.

## Features
- **$O(\log n)$ Appends:** Peak-merging algorithm retains past subtrees without re-hashing history.
- **Bag-the-Peaks Root Commitment:** Single root hash summarizing arbitrary log lengths.
- **Deterministic Cryptographic Verification:** Pure standard library SHA-256 implementation.

## Run Tests
```bash
python -m unittest discover -s tests -p "test_*.py"
```

## Author
Subrat Sahu (@subratsahu3) — subratsahu195@gmail.com
