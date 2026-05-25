from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT
sys.path.insert(0, str(ROOT))

import run_guarded_fsm_sim as sim


def read_csv(path: Path) -> list[dict[str, object]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def validate_split_csvs(combined_name: str, rows: list[dict[str, object]]) -> None:
    by_controller: dict[str, list[dict[str, object]]] = {}
    for row in rows:
        by_controller.setdefault(str(row["controller_id"]), []).append(row)
    require(set(by_controller) == {"no_guard", "schema_guard", "fsm_guard"}, f"{combined_name}: unexpected controller ids")
    for controller_id, controller_rows in by_controller.items():
        split_path = DATA_DIR / combined_name.replace(".csv", f"_{controller_id}.csv")
        split_rows = read_csv(split_path)
        require(split_rows == controller_rows, f"{split_path.name}: split CSV does not match combined rows")
        require(len(split_rows) == 11, f"{split_path.name}: expected 11 alpha rows")


def validate_metadata_and_report(quick: bool) -> None:
    metadata = json.loads((DATA_DIR / "guarded_fsm_artifact_metadata.json").read_text(encoding="utf-8"))
    generated = set(metadata["generated_files"])
    required = {
        "guarded_fsm_artifact_metadata.json",
        "guarded_fsm_artifact_report.md",
        "guarded_fsm_deployment_parser_cases.csv",
        "artifact/EXPECTED_RESULTS.json",
        "artifact/policies/approval_policy.json",
        "artifact/policies/deployment_policy.json",
        "artifact/policies/disclosure_policy.json",
    }
    missing = required.difference(generated)
    require(not missing, f"metadata generated_files missing: {sorted(missing)}")

    report = (DATA_DIR / "guarded_fsm_artifact_report.md").read_text(encoding="utf-8")
    if quick:
        require("| approval | Finite-state guard | 4 | 625 | 0 |" in report, "report missing quick approval FSM row")
        require("| disclosure | Finite-state guard | 4 | 2401 | 0 |" in report, "report missing quick disclosure FSM row")
    else:
        require("| approval | Finite-state guard | 8 | 390625 | 0 |" in report, "report missing approval FSM enumeration row")
        require("| disclosure | Finite-state guard | 6 | 117649 | 0 |" in report, "report missing disclosure FSM enumeration row")
    require("| Finite-state guard | 0.000 |" in report, "report missing zero unsafe AUC for finite-state guard")
    require("## Deployment Parser Boundary Cases" in report, "report missing deployment parser section")
    require("| prompt-injected-deploy | `malformed deploy_prod` | yes | yes | no | 2 |" in report, "report missing prompt-injected deployment row")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate regenerated guarded-FSM artifact outputs.")
    parser.add_argument("--quick", action="store_true", help="Validate outputs produced by run_guarded_fsm_sim.py --quick.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    outputs = {
        "enumeration": read_csv(DATA_DIR / "guarded_fsm_enumeration_results.csv"),
        "adversarial": read_csv(DATA_DIR / "guarded_fsm_adversarial_traces.csv"),
        "parser_cases": read_csv(DATA_DIR / "guarded_fsm_deployment_parser_cases.csv"),
    }
    sim.validate_expected_results(outputs, quick=args.quick)

    approval_rows = read_csv(DATA_DIR / "guarded_fsm_sim_results.csv")
    disclosure_rows = read_csv(DATA_DIR / "guarded_fsm_disclosure_results.csv")
    deployment_rows = read_csv(DATA_DIR / "guarded_fsm_deployment_parser_cases.csv")
    require(len(approval_rows) == 33, "approval sweep should contain 33 rows")
    require(len(disclosure_rows) == 33, "disclosure sweep should contain 33 rows")
    require(len(deployment_rows) >= 5, "deployment parser cases should contain at least 5 rows")
    require(
        all(row["fsm_guard_unsafe_emitted"] == "no" for row in deployment_rows),
        "finite-state guard should emit no unsafe deployment case",
    )
    validate_split_csvs("guarded_fsm_sim_results.csv", approval_rows)
    validate_split_csvs("guarded_fsm_disclosure_results.csv", disclosure_rows)

    proof_rows = read_csv(DATA_DIR / "guarded_fsm_proof_obligations.csv")
    failed = [row for row in proof_rows if row["preservation_check"] == "fail"]
    if failed:
        raise SystemExit(f"proof obligation failures: {failed[:3]}")
    validate_metadata_and_report(quick=args.quick)
    print("Artifact validation passed.")


if __name__ == "__main__":
    main()
