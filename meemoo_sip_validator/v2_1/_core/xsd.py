from importlib import resources
from pathlib import Path
import xml.etree.ElementTree as ET

from xmlschema import XMLSchema, XMLSchemaException

from .models import Report, Success, Error, Severity
from .codes import Code

assets = resources.files("meemoo_sip_validator.assets")
mets_xsd_path = str(assets.joinpath("mets-1-12.xsd.xml"))
premis_xsd_path = str(assets.joinpath("premis-3-0.xsd.xml"))
xlink_xsd_path = str(assets.joinpath("xlink-2.xsd.xml"))


def parse_xml_file(path: Path) -> Success | Error:
    try:
        ET.parse(path)
        return Success(
            code=Code.xsd_valid,
            message=f"Parsed XML: {path}",
        )
    except ET.ParseError as e:
        return Error(
            code=Code.xsd_valid,
            message=f"Could not parse XML - {e}. File: {path}",
            severity=Severity.ERROR,
        )


def parse_xml_files(paths: list[Path]) -> Report:
    return Report(results=[parse_xml_file(path) for path in paths])


def valiate_files(paths: list[Path], schema: XMLSchema) -> Report:
    code = Code.xsd_valid
    invalid_xsd_paths = [path for path in paths if not schema.is_valid(path)]

    errors: list[Error | Success] = []
    if len(invalid_xsd_paths) != 0:
        for path in invalid_xsd_paths:
            try:
                schema.validate(path)
            except XMLSchemaException as e:
                message = f"XSD validation failed on {path} - {e}"
                errors.append(
                    Error(code=code, message=message, severity=Severity.ERROR)
                )

    message = f"Structural XML files validated using XSD: {schema.name}"
    return Report(results=[Success(code=code, message=message)])


def validate_structural(unzipped_path: Path) -> Report:
    xlink_location = [("http://www.w3.org/1999/xlink", xlink_xsd_path)]
    mets_xsd = XMLSchema(mets_xsd_path, locations=xlink_location)
    mets_files = list(unzipped_path.rglob("METS.xml"))

    premis_xsd = XMLSchema(premis_xsd_path)
    premis_files = list(unzipped_path.rglob("premis.xml"))

    premis_report = valiate_files(premis_files, premis_xsd)
    mets_report = valiate_files(mets_files, mets_xsd)

    return premis_report + mets_report


def validate_basic(unzipped_path: Path) -> Report:
    descriptive_paths = list(unzipped_path.rglob("dc+schema.xml"))
    descriptive_report = parse_xml_files(descriptive_paths)

    return validate_structural(unzipped_path) + descriptive_report
