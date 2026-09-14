# AllocationAppeal

AllocationAppeal scores a request against a frozen public rubric and two independently hosted records. The appeal duration is fixed when the case is filed, but the deadline is created only after scoring finalizes. Delayed scoring therefore cannot consume or eliminate the subject's protected appeal opportunity.

The duration must be between ten minutes and 30 days. Once scoring succeeds, the lifecycle becomes `APPEAL_OPEN`; only the named subject may appeal during the entire fresh window. Anyone may resolve an unappealed or appealed case strictly after the deadline, preventing an absent filer from trapping the lifecycle.

Validators independently fetch the rubric and both evidence records, bind SHA-256 digests, and strictly verify that the proposed score reasonably applies the frozen rubric and that every stored reason is attributable to the records. Duplicate IDs, repeated source hosts, unauthorized appeals, early resolution, late appeals, invalid transitions, and malformed validator candidates are rejected.

## Verification

```bash
genvm-lint contracts/contract.py
python -m pytest -q
```

> **CASE FILE AA-01** · A score is not final while the subject still has a right to contest it.

AllocationAppeal separates scoring from finality. It freezes a public rubric, one allocation request, and two separately hosted evidence records; GenLayer validators compute the exact score and reasons, but the score deliberately opens an appeal window instead of immediately closing the case.

## Case timeline

`FILED → APPEAL_OPEN → APPEALED | RESOLVED`.

The named subject is the only party that can call `appeal_score`, and only before the recorded deadline. Once that deadline has passed, `resolve_allocation` is permissionless so neither scorer nor creator can trap a result forever.

## Evidence record

Validators independently retrieve the rubric and evidence. They verify the bounded score and attributed reasons against content digests before state changes. The contract rejects duplicate IDs, invalid addresses, malformed URLs, non-distinct source hosts, out-of-range scores, late appeals, and unauthorized appeals.

## Case references

```bash
PYTHONUTF8=1 genvm-lint contracts/contract.py
python -m pytest -q
```

StudioNet: [`0xdbCb434bb043C739344417bb4f0E2a965BB7922b`](https://explorer-studio.genlayer.com/address/0xdbCb434bb043C739344417bb4f0E2a965BB7922b)

Verified live case `AA-1789399075` opened a fresh 600-second appeal window only after scoring, then accepted the named subject's appeal without changing that deadline. See `deployment.json` and `network-run.json` for the three finalized transaction hashes and both canonical readbacks.
