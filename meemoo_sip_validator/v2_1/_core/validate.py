# pyright: reportExplicitAny=false

from typing import Any
from pathlib import Path

from meemoo_sip_validator.v2_1._core.descriptive.dc_schema import validate_dc_schema


from .models import SIP, DCPlusSchema
from .report import Report, Failure, Severity
from . import xsd, codes, utils
from .premis.premis import validate_premis


def _validate(unzipped_path: Path) -> Report:
    # from py_commons_ip.sip_validator import EARKSIPValidator
    # validator = EARKSIPValidator()
    # return validator.validate(unzipped_path)

    profile = utils.get_profile(unzipped_path)
    if profile is None:
        return get_profile_failure_report(unzipped_path)

    xsd_report = xsd.validate(unzipped_path)
    if xsd_report.outcome == "FAILED":
        return xsd_report

    match profile:
        case utils.Profile.BASIC:
            sip = SIP[DCPlusSchema].from_path(unzipped_path, DCPlusSchema)
            validate_descriptive = validate_dc_schema
        case utils.Profile.FILM:
            sip = SIP[DCPlusSchema].from_path(unzipped_path, DCPlusSchema)
            validate_descriptive = validate_dc_schema
        case utils.Profile.MATERIAL_ARTWORK:
            sip = SIP[DCPlusSchema].from_path(unzipped_path, DCPlusSchema)
            validate_descriptive = validate_dc_schema

    premis_report = validate_premis(sip)
    descriptive_report = validate_descriptive(sip)
    return xsd_report + premis_report + descriptive_report


def validate_to_report(unzipped_path: Path) -> Report:
    return _validate(unzipped_path)


def validate(unzipped_path: Path) -> dict[str, Any]:
    report = validate_to_report(unzipped_path)
    return report.to_dict()


def get_profile_failure_report(unzipped_path: Path) -> Report:
    return Report(
        results=[
            Failure(
                code=codes.Code.mets_other_content_information_type,
                message="The root mets must contain the csip:OTHERCONTENTINFORMATIONTYPE attribute indicating the profile ot the SIP.",
                severity=Severity.ERROR,
                source=str(unzipped_path.joinpath("METS.xml")),
            ),
        ]
    )
