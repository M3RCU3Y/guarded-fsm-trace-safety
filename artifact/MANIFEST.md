# Manifest

## Source

- `run_guarded_fsm_sim.py` - policy definitions, controller implementations,
  simulation sweeps, exhaustive enumeration, adversarial traces, proof rows, and
  report generation.
- `artifact/run_all.py` - one-command reproduction wrapper.
- `artifact/validate_artifact.py` - expected-result and file-consistency checks.
- `artifact/tests/test_guarded_fsm_artifact.py` - unit tests.
- `scripts/make_readme_assets.py` - SVG chart and diagram generator for the
  README.

## Policies

- `artifact/policies/approval_policy.json`
- `artifact/policies/disclosure_policy.json`

## Generated outputs

- `guarded_fsm_sim_results.csv`
- `guarded_fsm_disclosure_results.csv`
- `guarded_fsm_enumeration_results.csv`
- `guarded_fsm_adversarial_traces.csv`
- `guarded_fsm_proof_obligations.csv`
- `guarded_fsm_overhead_results.csv`
- `guarded_fsm_artifact_metadata.json`
- `guarded_fsm_artifact_report.md`
- `docs/assets/*.svg`

## Expected invariants

- The finite-state guard has zero unsafe accepted traces in bounded enumeration.
- The no-guard and schema-only baselines admit the adversarial approval and
  disclosure traces.
- Split controller CSV files match the combined sweep files exactly.
- The metadata file lists all regenerated outputs.
