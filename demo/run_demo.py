#!/usr/bin/env python3
"""Small public reproduction of the P0 verified-skill execution rail.

This is intentionally narrower than the original Walker spike. The original P0
browser-recording evidence is preserved under evidence/. This script reproduces
V2 rule execution, independent System-of-Record verification, and the negative
fail-closed rail using only local synthetic data.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "fixtures" / "daily-report"


def load(name: str):
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def compile_v2(corrections: dict) -> dict:
    rules = {c["rule_id"]: c["value"] for c in corrections["changes"]}
    return {
        "skill_id": "daily-report-skill",
        "version": 2,
        "confirmed_rules": rules,
        "acceptance": "independent_system_of_record_required",
    }


def execute(source: dict, skill: dict) -> dict:
    net_sales = source["gross_sales"] - source["refunds"]
    ratio = (net_sales - source["previous_net_sales"]) / source["previous_net_sales"]
    threshold = float(skill["confirmed_rules"]["significant_change_threshold"])
    note = ""
    if abs(ratio) > threshold:
        note = f"Significant change {ratio:.0%} exceeds confirmed {threshold:.0%} threshold"
    return {
        "date": source["date"],
        "gross_sales": source["gross_sales"],
        "refunds": source["refunds"],
        "net_sales": net_sales,
        "note": note,
    }


def verify(system_of_record: list[dict], expected: dict) -> dict:
    reasons = []
    if len(system_of_record) != expected["record_count"]:
        reasons.append(f"record_count expected {expected['record_count']} got {len(system_of_record)}")
    if len(system_of_record) == 1:
        record = system_of_record[0]
        for key in ("date", "gross_sales", "refunds", "net_sales"):
            if record.get(key) != expected[key]:
                reasons.append(f"{key} expected {expected[key]!r} got {record.get(key)!r}")
        for token in expected["note_must_contain"]:
            if token not in record.get("note", ""):
                reasons.append(f"note missing token {token!r}")
    return {
        "verification": "VERIFIED" if not reasons else "NOT_VERIFIED",
        "reasons": reasons,
        "record_count": len(system_of_record),
    }


def main() -> int:
    source = load("day2-source.json")
    expected = load("expected-day2.json")
    skill = compile_v2(load("operator-corrections.json"))
    report = execute(source, skill)

    # Honest rail: UI submit corresponds to a real persisted record.
    honest_store = [report]
    honest = verify(honest_store, expected)

    # Fault rail: UI may claim success, but backend stores nothing.
    optimistic_ui_success = True
    fault_store: list[dict] = []
    fault = verify(fault_store, expected)
    fault_outcome = "HALTED_NOT_VERIFIED" if fault["verification"] != "VERIFIED" else "UNSAFE_FALSE_PASS"

    print(json.dumps({
        "skill_version": skill["version"],
        "computed": report,
        "honest_rail": honest,
        "fault_rail": {
            "ui_success_banner": optimistic_ui_success,
            "verifier": fault,
            "outcome": fault_outcome,
        },
    }, ensure_ascii=False, indent=2))

    assert report["net_sales"] == 15000
    assert "25%" in report["note"] and "15%" in report["note"]
    assert honest["verification"] == "VERIFIED"
    assert optimistic_ui_success is True
    assert fault["verification"] == "NOT_VERIFIED"
    assert fault_outcome == "HALTED_NOT_VERIFIED"
    print("\nP0 PUBLIC REPRODUCTION PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
