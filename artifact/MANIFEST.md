# Artifact Manifest

This supplement contains the code, policies, generated data, and checks needed
to reproduce the reported results.

## Source Files

- `run_guarded_fsm_sim.py`: policy definitions, controller implementations,
  random sweeps, bounded exhaustive enumeration, adversarial traces, proof
  obligation export, and report generation.
- `artifact/run_all.py`: one-command reproduction wrapper.
- `artifact/validate_artifact.py`: expected-result validator for regenerated
  outputs.
- `artifact/tests/test_guarded_fsm_artifact.py`: unit tests for controller
  behavior, enumeration, proof-obligation rows, and expected-result validation.
- `artifact/policies/approval_policy.json`: generated approval workflow policy.
- `artifact/policies/deployment_policy.json`: generated production deployment
  gate used by the parser-boundary case study.
- `artifact/policies/disclosure_policy.json`: generated disclosure policy.

## Generated Data

- `guarded_fsm_sim_results.csv`: approval-policy sweep for all controllers.
- `guarded_fsm_disclosure_results.csv`: disclosure-policy sweep for all
  controllers.
- `guarded_fsm_deployment_parser_cases.csv`: raw deployment tool-call
  parser cases, parse errors, accepted traces, blocked counts, and unsafe
  emitted-action flags for each controller.
- `guarded_fsm_enumeration_results.csv`: bounded exhaustive proposal-sequence
  enumeration.
- `guarded_fsm_adversarial_traces.csv`: minimal adversarial proposal traces.
- `guarded_fsm_proof_obligations.csv`: finite state-action proof-obligation
  rows derived from the policy definitions.
- `guarded_fsm_overhead_results.csv`: guard-decision microbenchmark.
- `guarded_fsm_artifact_metadata.json`: generation parameters and environment.
- `guarded_fsm_artifact_report.md`: generated summary tables.

## Paper Mapping

- Figures 4-6 use `guarded_fsm_sim_results_*_guard.csv`.
- Figure 7 and Figure 8 use `guarded_fsm_disclosure_results_*_guard.csv`.
- Table 8 uses `guarded_fsm_sim_results.csv`.
- Table 9 uses integrated metrics computed from `guarded_fsm_sim_results.csv`.
- Table 10 uses `guarded_fsm_disclosure_results.csv`.
- Table 11 uses `guarded_fsm_enumeration_results.csv`.
- Table 12 uses `guarded_fsm_adversarial_traces.csv`.
- The deployment parser-boundary report section uses
  `guarded_fsm_deployment_parser_cases.csv`.
- Appendix proof-obligation discussion is supported by
  `guarded_fsm_proof_obligations.csv`.

## Reproduction

Run from the repository root:

```powershell
python artifact/run_all.py
```

The artifact uses only the Python standard library.
