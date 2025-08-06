from importlib import resources
from pathlib import Path

from xmlschema import XMLSchema, XMLSchemaException

from .report import Report, Success, Failure, Severity
from .utils import Profile, get_profile
from .codes import Code

assets = resources.files("meemoo_sip_validator.assets")

mets_xsd_path = str(assets.joinpath("mets-1-12.xsd.xml"))
premis_xsd_path = str(assets.joinpath("premis-3-0.xsd.xml"))
xlink_xsd_path = str(assets.joinpath("xlink-2.xsd.xml"))
basic_xsd_path = str(assets.joinpath("2.1/basic-2-1.xsd.xml"))
film_xsd_path = str(assets.joinpath("2.1/film-2-1.xsd.xml"))
material_artwork_xsd_path = str(assets.joinpath("2.1/material-artwork-2-1.xsd.xml"))


def valiate_files(paths: list[Path], schema: XMLSchema) -> Report:
    code = Code.xsd_valid
    invalid_xsd_paths = [path for path in paths if not schema.is_valid(path)]

    failures: list[Failure | Success] = []
    if len(invalid_xsd_paths) != 0:
        for path in invalid_xsd_paths:
            try:
                schema.validate(path)
            except XMLSchemaException as e:
                message = f"XSD validation failed on {path} - {e}"
                failures.append(
                    Failure(
                        source=str(path),
                        code=code,
                        message=message,
                        severity=Severity.ERROR,
                    )
                )

    message = f"Structural XML files validated using XSD: {schema.name}"
    return Report(results=[Success(code=code, message=message)])


def validate_mets(sip_path: Path) -> Report:
    xlink_location = [("http://www.w3.org/1999/xlink", xlink_xsd_path)]
    mets_xsd = XMLSchema(mets_xsd_path, locations=xlink_location)
    mets_files = list(sip_path.rglob("METS.xml"))
    mets_report = valiate_files(mets_files, mets_xsd)

    return mets_report


def validate_preservation(sip_path: Path) -> Report:
    premis_xsd = XMLSchema(premis_xsd_path)
    premis_files = list(sip_path.rglob("premis.xml"))
    premis_report = valiate_files(premis_files, premis_xsd)

    return premis_report


def validate_descriptive_basic(sip_path: Path) -> Report:
    basic_xsd = XMLSchema(basic_xsd_path)
    descriptive_files = list(sip_path.rglob("dc+schema.xml"))

    basic_report = valiate_files(descriptive_files, basic_xsd)

    return basic_report


def validate_descriptive(sip_path: Path, profile: Profile) -> Report:
    match profile:
        case Profile.BASIC:
            return validate_descriptive_basic(sip_path)
        case Profile.FILM:
            return validate_descriptive_basic(sip_path)
        case Profile.MATERIAL_ARTWORK:
            return validate_descriptive_basic(sip_path)


def validate(sip_path: Path) -> Report:
    profile = get_profile(sip_path)
    if profile is None:
        return get_profile_failure_report(sip_path)
    profile = Profile(profile)

    return (
        validate_mets(sip_path)
        + validate_preservation(sip_path)
        + validate_descriptive(sip_path, profile)
    )


def get_profile_failure_report(sip_path: Path):
    return Report(
        results=[
            Failure(
                code=Code.mets_other_content_information_type,
                message="The root mets must contain the csip:OTHERCONTENTINFORMATIONTYPE attribute indicating the profile ot the SIP.",
                severity=Severity.ERROR,
                source=str(sip_path / "METS.xml"),
            ),
        ]
    )
