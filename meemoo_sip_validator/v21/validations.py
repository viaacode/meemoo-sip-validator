from pathlib import Path

from lxml.etree import _ElementTree

from . import MeemooSIPConstraintEvaluation, MeemooSIPConstraintEvaluationStatus
from .constraints import msip7, msip150, msip151, msip153


METS_NAMESPACES = {"mets": "http://www.loc.gov/METS/"}

PREMIS_NAMESPACES = {
    "premis": "http://www.loc.gov/premis/v3",
}


def validate_msip7(root: _ElementTree) -> MeemooSIPConstraintEvaluation:
    mets_root = root.xpath(msip7.xpath, namespaces=METS_NAMESPACES)

    if len(mets_root) == 0:
        return MeemooSIPConstraintEvaluation(
            msip7,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            f"The element '{msip7.xpath}' is not present",
        )
    return MeemooSIPConstraintEvaluation(
        msip7, MeemooSIPConstraintEvaluationStatus.PASS
    )


def validate_msip150(root: _ElementTree) -> MeemooSIPConstraintEvaluation:
    premis_version = root.xpath(
        msip150.xpath,
        namespaces=PREMIS_NAMESPACES,
    )
    if len(premis_version) == 0:
        return MeemooSIPConstraintEvaluation(
            msip150,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            f"The element '{msip150.xpath}' is not present",
        )
    return MeemooSIPConstraintEvaluation(
        msip150, MeemooSIPConstraintEvaluationStatus.PASS
    )


def validate_msip151(root: _ElementTree) -> MeemooSIPConstraintEvaluation:
    premis_version = root.xpath(
        msip151.xpath,
        namespaces=PREMIS_NAMESPACES,
    )
    if len(premis_version) == 0:
        return MeemooSIPConstraintEvaluation(
            msip151,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            f"The attribute '{msip151.xpath}' is not present",
        )
    if (premis_version)[0] != "3.0":
        return MeemooSIPConstraintEvaluation(
            msip151,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            f"The value of '{msip151.xpath}' is different than '3.0'",
        )
    return MeemooSIPConstraintEvaluation(
        msip151, MeemooSIPConstraintEvaluationStatus.PASS
    )


def validate_msip153(unzipped_folder: Path) -> MeemooSIPConstraintEvaluation:
    premis_path = unzipped_folder.joinpath(
        msip153.get_relative_path().joinpath("premis.xml")
    )
    if not premis_path.exists():
        return MeemooSIPConstraintEvaluation(
            msip153,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            f"The file {premis_path} is not found",
        )
    return MeemooSIPConstraintEvaluation(
        msip153, MeemooSIPConstraintEvaluationStatus.PASS
    )
