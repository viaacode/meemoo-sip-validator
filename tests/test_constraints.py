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
from meemoo_sip_validator.v21.constraints import msip7, msip150, msip151, msip153
from meemoo_sip_validator.v21.validations import (
    validate_msip7,
    validate_msip150,
    validate_msip151,
    validate_msip153,
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


def test_validate_msip150_correct():
    path = Path(
        "tests",
        "resources",
        "msip150",
        "correct_premis",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip150(root) == MeemooSIPConstraintEvaluation(
        msip150,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_msip150_missing():
    path = Path(
        "tests",
        "resources",
        "msip150",
        "missing_premis",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip150(root) == MeemooSIPConstraintEvaluation(
        msip150,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The element '{msip150.xpath}' is not present",
    )


def test_validate_msip151_correct():
    path = Path(
        "tests",
        "resources",
        "msip151",
        "correct_premis_version",
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
        "missing_premis_version",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip151(root) == MeemooSIPConstraintEvaluation(
        msip151,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The attribute '{msip151.xpath}' is not present",
    )


def test_validate_msip151_wrong():
    path = Path(
        "tests",
        "resources",
        "msip151",
        "wrong_premis_version",
        "premis.xml",
    )
    root = etree.parse(path)

    assert validate_msip151(root) == MeemooSIPConstraintEvaluation(
        msip151,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The value of '{msip151.xpath}' is different than '3.0'",
    )


def test_validate_msip153_correct():
    path = Path(
        "tests",
        "resources",
        "msip153",
        "correct_premis",
    )

    assert validate_msip153(path) == MeemooSIPConstraintEvaluation(
        msip153,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_msip153_missing():
    path = Path(
        "tests",
        "resources",
        "msip153",
        "missing_premis",
    )

    assert validate_msip153(path) == MeemooSIPConstraintEvaluation(
        msip153,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The file {path.joinpath('metadata', 'preservation', 'premis.xml')} is not found",
    )
