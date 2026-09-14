# Steward remediation

| Requirement | Code path | Targeted proof | Status |
| --- | --- | --- | --- |
| Every scored case gets a full appeal opportunity | `score_allocation` sets `appeal_deadline` from the frozen duration after consensus scoring | `test_delayed_scoring_starts_a_fresh_full_appeal_window` | PASS locally |
| Immediate and boundary-time finalization remain blocked | `resolve_allocation` requires time strictly after the deadline | `test_immediate_and_boundary_finalization_are_rejected` | PASS locally |
| Appeal is restricted to the subject and the active window | `appeal_score` authorization and deadline guards | `test_unauthorized_and_late_appeals_fail` | PASS locally |
| Window has bounded duration | 10 minute minimum, 30 day maximum at filing | `test_appeal_window_bounds_and_forged_score` | PASS locally |
| New deployment uses corrected source commit `32fa5aa` | `deployment.json` binds source commit, SHA-256 and deployment transaction | `0x0b72...ee08` finalized with `MAJORITY_AGREE` | PASS live |
| Live scoring and appeal use the corrected contract | `AA-1789399075`; file `0x0972...d6b7`, score `0xfc6a...96ea`, appeal `0x99a9...109a` | score opened full 600-second window; appeal preserved the same deadline | PASS live |
