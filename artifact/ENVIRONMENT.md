# Environment Notes

The artifact is intentionally small and uses only Python's standard library.

- Primary script: `run_guarded_fsm_sim.py`
- Wrapper: `artifact/run_all.py`
- Tests: `artifact/tests/test_guarded_fsm_artifact.py`
- Default seed: `20260509`
- Default approval enumeration depth: `8`
- Default disclosure enumeration depth: `6`
- Default episodes per noise value: `5000`
- Default maximum proposals per episode: `14`
- Deployment parser-boundary cases are deterministic fixtures generated from
  raw JSON-like tool-call traces.

Generated metadata are written to `guarded_fsm_artifact_metadata.json` and
include the Python version, platform string, seed, episode count, enumeration
depths, deployment parser CSV, and generated file list.
