from typing import Any, Callable
from pathlib import Path
import json

from eark_models.utils import XMLParseable
import py_commons_ip

from .utils import ValidatorError

from .models import SIP, DCPlusSchema
from .report import Report, Failure, Severity, Success
from . import xsd, codes, utils
from .premis.premis import validate_premis
from .descriptive.dc_schema import validate_dc_schema


def _validate(unzipped_path: Path) -> Report:
    commons_ip_result = py_commons_ip.validate(unzipped_path, "2.2.0")
    is_valid_commons_ip, commons_ip_json_report = commons_ip_result
    commons_ip_report = commons_ip_report_to_meemoo_report(commons_ip_json_report)

    if not is_valid_commons_ip:
        return commons_ip_report

    profile = utils.get_profile(unzipped_path)
    if profile is None:
        return get_profile_failure_report(unzipped_path)

    xsd_report = xsd.validate(unzipped_path)
    if xsd_report.outcome == "FAILED":
        return commons_ip_report + xsd_report

    validate_descriptive = get_descriptive_validation_fn(profile)
    DescriptiveModel = get_descriptive_model(profile)
    sip = SIP[DescriptiveModel].from_path(unzipped_path, DescriptiveModel)
    premis_report = validate_premis(sip)
    descriptive_report = validate_descriptive(sip)

    return commons_ip_report + xsd_report + premis_report + descriptive_report


def validate_to_report(unzipped_path: Path) -> Report:
    return _validate(unzipped_path)


def validate(unzipped_path: Path) -> tuple[bool, dict[str, Any]]:
    report = validate_to_report(unzipped_path)
    return report.is_valid, report.to_dict()


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


def get_descriptive_model(profile: utils.Profile) -> type[XMLParseable]:
    match profile:
        case utils.Profile.BASIC:
            return DCPlusSchema
        case utils.Profile.FILM:
            return DCPlusSchema
        case utils.Profile.MATERIAL_ARTWORK:
            return DCPlusSchema


def get_descriptive_validation_fn(
    profile: utils.Profile,
) -> Callable[[SIP[Any]], Report]:
    match profile:
        case utils.Profile.BASIC:
            return validate_dc_schema
        case utils.Profile.FILM:
            return validate_dc_schema
        case utils.Profile.MATERIAL_ARTWORK:
            return validate_dc_schema


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
