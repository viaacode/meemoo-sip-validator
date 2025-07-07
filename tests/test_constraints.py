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
from meemoo_sip_validator.v21.constraints import msip0007, msip0150, msip0151, msip0153
from meemoo_sip_validator.v21.validations import (
    validate_msip0007,
    validate_msip0150,
    validate_msip0151,
    validate_msip0153,
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


def test_validate_msip0007_correct():
    path = Path(
        "tests",
        "resources",
        "msip0007",
        "correct_mets",
        "METS.xml",
    )
    root = etree.parse(path)

    assert validate_msip0007(root) == MeemooSIPConstraintEvaluation(
        msip0007, MeemooSIPConstraintEvaluationStatus.PASS
    )


def test_validate_msip0007_missing():
    path = Path(
        "tests",
        "resources",
        "msip0007",
        "missing_mets",
        "METS.xml",
    )
    root = etree.parse(path)

    assert validate_msip0007(root) == MeemooSIPConstraintEvaluation(
        msip0007,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The element '{msip0007.xpath}' is not present",
    )


def test_validate_msip0150_correct():
    path = Path(
        "tests",
        "resources",
        "msip0150",
        "correct_premis",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip0150(root) == MeemooSIPConstraintEvaluation(
        msip0150,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_msip0150_missing():
    path = Path(
        "tests",
        "resources",
        "msip0150",
        "missing_premis",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip0150(root) == MeemooSIPConstraintEvaluation(
        msip0150,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The element '{msip0150.xpath}' is not present",
    )


def test_validate_msip0151_correct():
    path = Path(
        "tests",
        "resources",
        "msip0151",
        "correct_premis_version",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip0151(root) == MeemooSIPConstraintEvaluation(
        msip0151,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_msip0151_missing():
    path = Path(
        "tests",
        "resources",
        "msip0151",
        "missing_premis_version",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip0151(root) == MeemooSIPConstraintEvaluation(
        msip0151,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The attribute '{msip0151.xpath}' is not present",
    )


def test_validate_msip0151_wrong():
    path = Path(
        "tests",
        "resources",
        "msip0151",
        "wrong_premis_version",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip0151(root) == MeemooSIPConstraintEvaluation(
        msip0151,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The value of '{msip0151.xpath}' is different than '3.0'",
    )


def test_validate_msip0153_correct():
    path = Path(
        "tests",
        "resources",
        "msip0153",
        "correct_premis",
    )

    assert validate_msip0153(path) == MeemooSIPConstraintEvaluation(
        msip0153,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_msip0153_missing():
    path = Path(
        "tests",
        "resources",
        "msip0153",
        "missing_premis",
    )

    assert validate_msip0153(path) == MeemooSIPConstraintEvaluation(
        msip0153,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The file {path.joinpath('metadata', 'preservation', 'premis.xml')} is not found",
    )
