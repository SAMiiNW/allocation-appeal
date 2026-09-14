# Steward remediation

| Requirement | Code path | Targeted proof | Status |
| --- | --- | --- | --- |
| Every scored case gets a full appeal opportunity | `score_allocation` sets `appeal_deadline` from the frozen duration after consensus scoring | `test_delayed_scoring_starts_a_fresh_full_appeal_window` | PASS locally |
| Immediate and boundary-time finalization remain blocked | `resolve_allocation` requires time strictly after the deadline | `test_immediate_and_boundary_finalization_are_rejected` | PASS locally |
| Appeal is restricted to the subject and the active window | `appeal_score` authorization and deadline guards | `test_unauthorized_and_late_appeals_fail` | PASS locally |
| Window has bounded duration | 10 minute minimum, 30 day maximum at filing | `test_appeal_window_bounds_and_forged_score` | PASS locally |
| New deployment matches corrected source | deployment manifest and Explorer source comparison | StudioNet deployment | UNVERIFIED |
| Live scoring and appeal use the corrected contract | finalized lifecycle transactions | StudioNet smoke run | UNVERIFIED |
