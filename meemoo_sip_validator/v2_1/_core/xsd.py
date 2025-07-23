from importlib import resources
from pathlib import Path
import xml.etree.ElementTree as ET

from xmlschema import XMLSchema

from .models import Report, Success, Error, Severity

assets = resources.files("meemoo_sip_validator.assets")
mets_xsd_path = str(assets.joinpath("mets-1-12.xsd.xml"))
premis_xsd_path = str(assets.joinpath("premis-3-0.xsd.xml"))
xlink_xsd_path = str(assets.joinpath("xlink-2.xsd.xml"))


def parse_xml_file(path: Path) -> Success | Error:
    # TODO: add code
    try:
        ET.parse(path)
        return Success(
            code="",
            message=f"Parsed XML: {path}",
        )
    except:
        return Error(
            code="",
            message=f"Could not parse XML: {path}",
            severity=Severity.ERROR,
        )


def parse_xml_files(paths: list[Path]) -> Report:
    return Report(results=[parse_xml_file(path) for path in paths])


def validate_file(path: Path, schema: XMLSchema) -> Success | Error:
    # TODO: add code
    try:
        schema.validate(path)
        return Success(
            code="",
            message=f"Validated file using XSD: {path}",
        )
    except:
        return Error(
            code="",
            message=f"XSD validation failed: {path}",
            severity=Severity.ERROR,
        )


def valiate_files(paths: list[Path], schema: XMLSchema) -> Report:
    return Report(results=[validate_file(path, schema) for path in paths])


def validate(unzipped_path: Path) -> Report:
    xlink_location = [("http://www.w3.org/1999/xlink", xlink_xsd_path)]
    mets_xsd = XMLSchema(mets_xsd_path, locations=xlink_location)
    mets_files = list(unzipped_path.rglob("METS.xml"))

    premis_xsd = XMLSchema(premis_xsd_path)
    premis_files = list(unzipped_path.rglob("premis.xml"))

    premis_report = valiate_files(premis_files, premis_xsd)
    mets_report = valiate_files(mets_files, mets_xsd)

    descriptive_paths = list(unzipped_path.rglob("dc+schema.xml"))
    descriptive_report = parse_xml_files(descriptive_paths)

    return premis_report + mets_report + descriptive_report
