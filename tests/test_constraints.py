from pathlib import Path

from lxml import etree

from meemoo_sip_validator.constraints import (
    MeemooSIPConstraint,
    MeemooSIPConstraintCardinality,
    MeemooSIPConstraintDatatype,
    MeemooSIPConstraintEvaluation,
    MeemooSIPConstraintEvaluationStatus,
    MeemooSIPConstraintObligation,
    MeemooSIPConstraintSIPLevel,
    MeemooSIPConstraintXMLNodeType,
)
from meemoo_sip_validator.v21.constraints import (
    msip7,
    msip151,
    msip152,
    msip154,
)
from meemoo_sip_validator.v21.validations import (
    validate_msip7,
    validate_msip151,
    validate_msip152,
    validate_msip154,
)
from meemoo_sip_validator.v21.basic.constraints import (
    bacp22,
)
from meemoo_sip_validator.v21.basic.validations import (
    validate_bacp22,
)


class TestMeemooSIPConstraint:
    def test_init(self):
        identification = "id01"
        description = "description"

        constraint = MeemooSIPConstraint(identification, description)

        assert constraint.identification == identification
        assert constraint.description == description

        assert constraint.cardinality == MeemooSIPConstraintCardinality.UNSPECIFIED
        assert constraint.obligation == MeemooSIPConstraintObligation.UNSPECIFIED
        assert constraint.sip_level == MeemooSIPConstraintSIPLevel.UNSPECIFIED
        assert constraint.datatype == MeemooSIPConstraintDatatype.UNSPECIFIED
        assert constraint.xml_node_type == MeemooSIPConstraintXMLNodeType.UNSPECIFIED
        assert constraint.path is None
        assert constraint.xpath is None


class TestMeemooSIPConstraintEvaluation:
    def test_init(self):
        identification = "id01"
        description = "description"
        constraint = MeemooSIPConstraint(identification, description)
        evaluation_status = MeemooSIPConstraintEvaluationStatus.PASS
        evaluation = MeemooSIPConstraintEvaluation(constraint, evaluation_status)

        assert evaluation.constraint == constraint
        assert evaluation.severity == evaluation_status
        assert evaluation.message is None


def test_validate_msip7_correct():
    path = Path(
        "tests",
        "resources",
        "msip7",
        "correct_mets",
        "METS.xml",
    )
    root = etree.parse(path)

    assert validate_msip7(root) == MeemooSIPConstraintEvaluation(
        msip7, MeemooSIPConstraintEvaluationStatus.PASS
    )


def test_validate_msip7_missing():
    path = Path(
        "tests",
        "resources",
        "msip7",
        "missing_mets",
        "METS.xml",
    )
    root = etree.parse(path)

    assert validate_msip7(root) == MeemooSIPConstraintEvaluation(
        msip7,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The element '{msip7.xpath}' is not present",
    )


def test_validate_msip151_correct():
    path = Path(
        "tests",
        "resources",
        "msip151",
        "correct_premis",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip151(root) == MeemooSIPConstraintEvaluation(
        msip151,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_msip151_missing():
    path = Path(
        "tests",
        "resources",
        "msip151",
        "missing_premis",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip151(root) == MeemooSIPConstraintEvaluation(
        msip151,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The element '{msip151.xpath}' is not present",
    )


def test_validate_msip152_correct():
    path = Path(
        "tests",
        "resources",
        "msip152",
        "correct_premis_version",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip152(root) == MeemooSIPConstraintEvaluation(
        msip152,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_msip152_missing():
    path = Path(
        "tests",
        "resources",
        "msip152",
        "missing_premis_version",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip152(root) == MeemooSIPConstraintEvaluation(
        msip152,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The attribute '{msip152.xpath}' is not present",
    )


def test_validate_msip152_wrong():
    path = Path(
        "tests",
        "resources",
        "msip152",
        "wrong_premis_version",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip152(root) == MeemooSIPConstraintEvaluation(
        msip152,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The value of '{msip152.xpath}' is different than '3.0'",
    )


def test_validate_msip154_correct():
    path = Path(
        "tests",
        "resources",
        "msip154",
        "correct_premis",
    )

    assert validate_msip154(path) == MeemooSIPConstraintEvaluation(
        msip154,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_msip154_missing():
    path = Path(
        "tests",
        "resources",
        "msip154",
        "missing_premis",
    )

    assert validate_msip154(path) == MeemooSIPConstraintEvaluation(
        msip154,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The file {path.joinpath('metadata', 'preservation', 'premis.xml')} is not found",
    )


def test_validate_bacp22():
    path = Path("tests", "resources", "bacp22", "correct", "dc+schema.xml")

    root = etree.parse(path)

    assert validate_bacp22(root) == MeemooSIPConstraintEvaluation(
        bacp22,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_bacp22_wrong_namespaces():
    path = Path("tests", "resources", "bacp22", "wrong_namespaces", "dc+schema.xml")

    root = etree.parse(path)

    assert validate_bacp22(root) == MeemooSIPConstraintEvaluation(
        bacp22,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The element '{bacp22.xpath}' does not declare the correct namespaces",
    )


def test_validate_bacp22_missing():
    path = Path("tests", "resources", "bacp22", "wrong_missing", "dc+schema.xml")

    root = etree.parse(path)

    assert validate_bacp22(root) == MeemooSIPConstraintEvaluation(
        bacp22,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The element '{bacp22.xpath}' is not present",
    )
