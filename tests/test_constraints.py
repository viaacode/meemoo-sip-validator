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
        assert evaluation.status == evaluation_status
        assert evaluation.message is None
