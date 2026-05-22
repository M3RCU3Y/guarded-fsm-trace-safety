# Artifact Notes

This folder contains the validation layer around the finite-state guard
simulations.

## What is here

- `run_all.py` runs the full reproduction path from the repository root.
- `validate_artifact.py` checks regenerated CSVs, split result files, metadata,
  expected enumeration counts, adversarial traces, and report contents.
- `EXPECTED_RESULTS.json` records the fixed values used by the validator.
- `policies/*.json` contains machine-readable snapshots of the approval and
  disclosure guards.
- `tests/test_guarded_fsm_artifact.py` covers the core guard behavior, baseline
  failures, finite enumeration, proof-obligation rows, and expected-result
  validation.

## Commands

The artifact requires Python 3.10 or newer and uses only the Python standard
library.

Run the full reproduction:

```bash
python artifact/run_all.py
```

Run a quick smoke version:

```bash
python run_guarded_fsm_sim.py --quick
python artifact/validate_artifact.py --quick
python -m unittest discover -s artifact/tests -p "test_*.py"
```
