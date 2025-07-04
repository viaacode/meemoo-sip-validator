from lxml.etree import _ElementTree

from . import MeemooSIPConstraintEvaluation, MeemooSIPConstraintEvaluationStatus
from .constraints import msip0007


METS_NAMESPACES = {"mets": "http://www.loc.gov/METS/"}


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
