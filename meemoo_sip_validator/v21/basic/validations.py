from lxml.etree import _ElementTree

from .. import MeemooSIPConstraintEvaluation, MeemooSIPConstraintEvaluationStatus
from .constraints import bacp22


DC_SCHEMA_NAMESPACES = {
    None: "https://data.hetarchief.be/id/sip/2.1/basic",
    "dcterms": "http://purl.org/dc/terms/",
    "xs": "http://www.w3.org/2001/XMLSchema/",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "edtf": "http://id.loc.gov/datatypes/edtf/",
    "schema": "https://schema.org/",
}


def validate_bacp22(root: _ElementTree) -> MeemooSIPConstraintEvaluation:
    metadata_element = root.getroot()
    if metadata_element.tag != f"{{{DC_SCHEMA_NAMESPACES[None]}}}{bacp22.xpath}":
        return MeemooSIPConstraintEvaluation(
            bacp22,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            f"The element '{bacp22.xpath}' is not present",
        )
    if metadata_element.nsmap != DC_SCHEMA_NAMESPACES:
        return MeemooSIPConstraintEvaluation(
            bacp22,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            f"The element '{bacp22.xpath}' does not declare the correct namespaces",
        )
    return MeemooSIPConstraintEvaluation(
        bacp22, MeemooSIPConstraintEvaluationStatus.PASS
    )
