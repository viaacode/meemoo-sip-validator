from meemoo_sip_validator.constraints import (
    MeemooSIPConstraint,
    MeemooSIPConstraintCardinality,
    MeemooSIPConstraintDatatype,
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
