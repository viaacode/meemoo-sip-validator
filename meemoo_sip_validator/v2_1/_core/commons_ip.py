from pathlib import Path
import json

import py_commons_ip

from .utils import ValidatorError

from .report import Report, Failure, Severity, Success


def validate_commons_ip(sip_path: Path) -> Report:
    commons_ip_result = py_commons_ip.validate(sip_path, "2.2.0")
    _, commons_ip_json_report = commons_ip_result
    return commons_ip_report_to_meemoo_report(commons_ip_json_report)


def commons_ip_report_to_meemoo_report(report: str) -> Report:
    # TODO: add csip codes to Code enum
    report_dict = json.loads(report)

    results: list[Failure | Success] = []

    validations = report_dict["validation"]
    for validation in validations:
        code = validation["id"]
        level = validation["level"]
        outcome = validation["testing"]["outcome"]

        issues = validation["testing"]["issues"]
        warnings = validation["testing"]["warnings"]
        notes = validation["testing"]["notes"]
        messages = issues + warnings + notes

        if outcome == "FAILED":
            if level == "MUST":
                severity = Severity.ERROR
            elif level == "SHOULD":
                severity = Severity.WARNING
            elif level == "MAY":
                severity = Severity.INFO
            else:
                raise ValidatorError(f"Unexpected Commons IP level '{level}'")

            result = Failure(
                code=code,
                severity=Severity(severity),
                message=" ".join(messages),
                source="Unknown source",
            )

        elif outcome == "PASSED":
            result = Success(
                code=code,
                message=" ".join(messages),
            )

        else:
            continue

        results.append(result)

    return Report(results=results)
