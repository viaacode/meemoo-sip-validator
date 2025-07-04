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
    msip0007,
)
from meemoo_sip_validator.v21.validations import (
    validate_msip0007,
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
        assert constraint.filename is None
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
