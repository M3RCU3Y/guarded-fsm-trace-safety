# Trace-Safe Runtime Enforcement Reproduction Guide

This artifact regenerates the simulation tables used by the paper, checks finite
guard obligations by enumeration, and records a small decision-overhead
benchmark. In this standalone release folder, generated CSVs, metadata, and the
summary report live at the repository root beside `run_guarded_fsm_sim.py`.

## Requirements

- Python 3.10 or newer.
- No third-party Python packages are required for the artifact scripts.

## One-Command Reproduction

From the repository root:

```powershell
python artifact/run_all.py
```

The command regenerates:

- `guarded_fsm_sim_results.csv`
- `guarded_fsm_disclosure_results.csv`
- `guarded_fsm_deployment_parser_cases.csv`
- `guarded_fsm_enumeration_results.csv`
- `guarded_fsm_adversarial_traces.csv`
- `guarded_fsm_overhead_results.csv`
- `guarded_fsm_artifact_metadata.json`
- `guarded_fsm_artifact_report.md`
- `artifact/policies/*.json`

It also runs the artifact unit tests.

## Manual Commands

Regenerate the full artifact:

```powershell
python run_guarded_fsm_sim.py
```

Run a quick smoke version:

```powershell
python run_guarded_fsm_sim.py --quick
python artifact/validate_artifact.py --quick
```

Run tests:

```powershell
python -m unittest discover -s artifact/tests -p "test_*.py"
```

## Expected Results

The finite-state guard should have zero unsafe accepted traces in the bounded
enumeration rows for both the approval policy and the disclosure policy. The no
guard and schema guard baselines should show unsafe traces for the adversarial
cases `request-then-execute` and `private-then-external`.

The deployment parser-boundary cases show a more realistic integration shape:
raw JSON-like tool calls are mapped into a finite deployment alphabet, parse
errors fail closed as `malformed`, and the finite-state guard blocks production
deployment unless CI has passed and human approval has been recorded.

## Troubleshooting

If validation cannot find generated CSV files, run `python artifact/run_all.py`
from the repository root first. If a test cannot import
`run_guarded_fsm_sim.py`, make sure the current working directory is the
repository root.
