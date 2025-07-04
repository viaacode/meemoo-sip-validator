from lxml.etree import _ElementTree

from . import MeemooSIPConstraintEvaluation, MeemooSIPConstraintEvaluationStatus
from .constraints import msip0007, msip0150


METS_NAMESPACES = {"mets": "http://www.loc.gov/METS/"}

PREMIS_NAMESPACES = {
    "premis": "http://www.loc.gov/premis/v3",
}


def validate_msip0007(root: _ElementTree) -> MeemooSIPConstraintEvaluation:
    mets_root = root.xpath(msip0007.xpath, namespaces=METS_NAMESPACES)

    if len(mets_root) == 0:
        return MeemooSIPConstraintEvaluation(
            msip0007,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            f"The element '{msip0007.xpath}' is not present",
        )
    return MeemooSIPConstraintEvaluation(
        msip0007, MeemooSIPConstraintEvaluationStatus.PASS
    )


def validate_msip0150(root: _ElementTree) -> MeemooSIPConstraintEvaluation:
    premis_version = root.xpath(
        msip0150.xpath,
        namespaces=PREMIS_NAMESPACES,
    )
    if len(premis_version) == 0:
        return MeemooSIPConstraintEvaluation(
            msip0150,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            f"The element '{msip0150.xpath}' is not present",
        )
    return MeemooSIPConstraintEvaluation(
        msip0150, MeemooSIPConstraintEvaluationStatus.PASS
    )
