from typing import Any, Callable
from pathlib import Path


from .report import Report, Failure, Severity
from . import xsd, codes, utils, commons_ip, structural
from .premis.premis import validate_premis
from .descriptive.dc_schema import validate_dc_schema


def _validate(sip_path: Path) -> Report:
    profile = utils.get_profile(sip_path)
    if profile is None:
        validate_descriptive = get_profile_failure_report
    else:
        validate_descriptive = get_descriptive_validation_fn(profile)

    return (
        structural.validate_structural(sip_path)
        + commons_ip.validate_commons_ip(sip_path)
        + xsd.validate_xsd(sip_path)
        + validate_premis(sip_path)
        + validate_descriptive(sip_path)
    )


def validate_to_report(sip_path: Path) -> Report:
    return _validate(sip_path.expanduser().resolve())


def validate(sip_path: Path) -> tuple[bool, dict[str, Any]]:
    report = validate_to_report(sip_path)
    return report.is_valid, report.to_dict()


def get_profile_failure_report(sip_path: Path) -> Report:
    return Report(
        results=[
            Failure(
                code=codes.Code.mets_other_content_information_type,
                message="The root mets must contain the csip:OTHERCONTENTINFORMATIONTYPE attribute indicating the profile ot the SIP.",
                severity=Severity.ERROR,
                source=str(sip_path / "METS.xml"),
            ),
        ]
    )


def get_descriptive_validation_fn(
    profile: utils.Profile,
) -> Callable[[Path], Report]:
    match profile:
        case utils.Profile.BASIC:
            return validate_dc_schema
        case utils.Profile.FILM:
            return validate_dc_schema
        case utils.Profile.MATERIAL_ARTWORK:
            return validate_dc_schema
