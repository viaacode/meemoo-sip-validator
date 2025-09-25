import sys
from pathlib import Path
import json
from importlib.metadata import version


def validator_cli():
    if len(sys.argv) == 2 and sys.argv[1] == "--version":
        print(f"meemoo-sip-validator {version('meemoo-sip-validator')}")
        exit()

    if len(sys.argv) != 3:
        print(
            "Usage: meemoo-sip-validator SIP-VERSION PATH\n\nSupported SIP versions: 2.1"
        )
        exit(1)

    version_arg = sys.argv[1]
    path = Path(sys.argv[2])
    validator_fn = get_validator_fn_for_version(version_arg)
    report = validator_fn(path)
    failures = [failure.to_dict() for failure in report.failures]

    print(json.dumps(failures, indent=4))
    if report.is_valid:
        print(
            "\nNo error produced. The SIP may still be invalid, as the validator is incomplete."
        )
        exit(0)
    else:
        print("\nSIP is not valid.")
        exit(1)


def get_validator_fn_for_version(version: str):
    match version:
        case "2.1":
            from ..v2_1 import validate_to_report

            return validate_to_report
        case _:
            print(f"Unsupported version: '{version}'")
            exit(1)
