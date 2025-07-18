from pathlib import Path

from lxml import etree

from meemoo_sip_validator.constraints import (
    MeemooSIPConstraintEvaluation,
    MeemooSIPConstraintEvaluationStatus,
)

from meemoo_sip_validator.v21.basic.constraints import (
    bacp22,
)
from meemoo_sip_validator.v21.basic.validations import (
    validate_bacp22,
)


def test_validate_bacp22():
    path = Path("tests", "resources", "v21", "bacp22", "correct", "dc+schema.xml")

    tree = etree.parse(path)

    assert validate_bacp22(tree) == MeemooSIPConstraintEvaluation(
        bacp22,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_bacp22_wrong_namespaces():
    path = Path(
        "tests", "resources", "v21", "bacp22", "wrong_namespaces", "dc+schema.xml"
    )

    tree = etree.parse(path)

    assert validate_bacp22(tree) == MeemooSIPConstraintEvaluation(
        bacp22,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The element '{bacp22.xpath}' does not declare the correct namespaces",
    )


def test_validate_bacp22_missing():
    path = Path("tests", "resources", "v21", "bacp22", "wrong_missing", "dc+schema.xml")

    tree = etree.parse(path)

    assert validate_bacp22(tree) == MeemooSIPConstraintEvaluation(
        bacp22,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The element '{bacp22.xpath}' is not present",
    )
