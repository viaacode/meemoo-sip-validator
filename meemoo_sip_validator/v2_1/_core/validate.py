# pyright: reportExplicitAny=false

from typing import Any, Self, override
from pathlib import Path

from pydantic.dataclasses import dataclass

from eark_models.utils import XMLParseable

from .models import Report, SIP
from . import xsd
from .premis.reports import validate as validate_premis


@dataclass
class Dummy(XMLParseable):
    @override
    @classmethod
    def from_xml(cls, path: Path) -> Self:
        return cls()


def _validate(unzipped_path: Path) -> Report:
    # from py_commons_ip.sip_validator import EARKSIPValidator
    # validator = EARKSIPValidator()
    # return validator.validate(unzipped_path)

    xsd_report = xsd.validate(unzipped_path)
    if xsd_report.outcome == "FAILED":
        return xsd_report

    sip = SIP[Dummy].from_path(unzipped_path, Dummy)

    premis_report = validate_premis(sip)
    return xsd_report + premis_report


def validate_to_report(unzipped_path: Path) -> Report:
    return _validate(unzipped_path)


def validate(unzipped_path: Path) -> dict[str, Any]:
    report = validate_to_report(unzipped_path)
    return report.to_dict()
