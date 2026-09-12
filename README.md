# AllocationAppeal

> **CASE FILE AA-01** · A score is not final while the subject still has a right to contest it.

AllocationAppeal separates scoring from finality. It freezes a public rubric, one allocation request, and two separately hosted evidence records; GenLayer validators compute the exact score and reasons, but the score deliberately opens an appeal window instead of immediately closing the case.

## Case timeline

`FILED → APPEAL_OPEN → APPEALED | RESOLVED`.

The named subject is the only party that can call `appeal_score`, and only before the recorded deadline. Once that deadline has passed, `resolve_allocation` is permissionless so neither scorer nor creator can trap a result forever.

## Evidence record

Validators independently retrieve the rubric and evidence. They must agree on the precise integer score, ordered reasons, and content digests before state changes. The contract rejects duplicate IDs, invalid addresses, malformed URLs, non-distinct source hosts, out-of-range scores, late appeals, and unauthorized appeals.

## Case references

```bash
PYTHONUTF8=1 genvm-lint contracts/contract.py
python -m pytest -q
```

StudioNet: [`0x3CFdB6e2b30Fe58e9dBc69A1149CD545bfae0A88`](https://explorer-studio.genlayer.com/address/0x3CFdB6e2b30Fe58e9dBc69A1149CD545bfae0A88)
