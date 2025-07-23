from typing import Any
from pathlib import Path

from .models import Report
from . import xsd


def validate_to_report(unzipped_path) -> Report:
    # from py_commons_ip.sip_validator import EARKSIPValidator
    # validator = EARKSIPValidator()
    # return validator.validate(unzipped_path)

    return xsd.validate(unzipped_path)


def validate(unzipped_path: Path) -> dict[str, Any]:
    report = validate_to_report(unzipped_path)
    return report.model_dump()
