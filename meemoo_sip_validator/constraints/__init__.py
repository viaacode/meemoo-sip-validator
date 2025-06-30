from enum import auto, StrEnum
from typing import override


class MeemooSIPConstraintObligation(StrEnum):
    MAY = auto()
    SHOULD = auto()
    MUST = auto()
    UNSPECIFIED = auto()


class MeemooSIPConstraintCardinality(StrEnum):
    AT_LEAST_ONE = auto()
    AT_MOST_ONE = auto()
    EXACTLY_ONE = auto()
    ZERO_OR_MORE = auto()
    UNSPECIFIED = auto()


class MeemooSIPConstraintSIPLevel(StrEnum):
    REPRESENTATION = auto()
    PACKAGE = auto()
    ALL = auto()
    UNSPECIFIED = auto()


class MeemooSIPConstraintDatatype(StrEnum):
    ID = auto()
    STRING = auto()
    EDTF = auto()
    BCP47 = auto()
    INTEGER = auto()
    URI = auto()
    XSD_DURATION = auto()
    XSD_DATETIME = auto()
    UNSPECIFIED = auto()


class MeemooSIPConstraintXMLNodeType(StrEnum):
    GENERAL = auto()
    ELEMENT = auto()
    ATTRIBUTE = auto()
    UNSPECIFIED = auto()


class MeemooSIPConstraintEvaluationStatus(StrEnum):
    SUCCESS = auto()
    FAIL = auto()


class MeemooSIPConstraint:
    """Class describing a meemoo SIP constraint.

    Attributes:
        _identification: The unique identifier.
        _description: The description.
        _cardinality: The cardinality, if applicable e.g. 0..1.
        _obligation: Describes the obligation, if applicable e.g. MUST, SHOULD, ...
        _sip_level: Which level of the SIP does the constraint apply to, if applicable.
        _datatype: What is the datatype of the XML node the constraint applies to , if applicable.
        _xml_node_type: Which type of XML node does the constraint apply to, if applicable.
        _filename: The filename of the relevant file, if applicable.
        _xpath: The XPath to the relevant XML node, if applicable.
    """

    def __init__(
        self,
        identification: str,
        description: str,
        cardinality: MeemooSIPConstraintCardinality = MeemooSIPConstraintCardinality.UNSPECIFIED,
        obligation: MeemooSIPConstraintObligation = MeemooSIPConstraintObligation.UNSPECIFIED,
        sip_level: MeemooSIPConstraintSIPLevel = MeemooSIPConstraintSIPLevel.UNSPECIFIED,
        datatype: MeemooSIPConstraintDatatype = MeemooSIPConstraintDatatype.UNSPECIFIED,
        xml_node_type: MeemooSIPConstraintXMLNodeType = MeemooSIPConstraintXMLNodeType.UNSPECIFIED,
        filename: str | None = None,
        xpath: str | None = None,
    ):
        self._identification: str = identification
        self._description: str = description
        self._cardinality: MeemooSIPConstraintCardinality = cardinality
        self._obligation: MeemooSIPConstraintObligation = obligation
        self._sip_level: MeemooSIPConstraintSIPLevel = sip_level
        self._datatype: MeemooSIPConstraintDatatype = datatype
        self._xml_node_type: MeemooSIPConstraintXMLNodeType = xml_node_type
        self._filename: str | None = filename
        self._xpath: str | None = xpath

    @property
    def identification(self) -> str:
        return self._identification

    @property
    def description(self) -> str:
        return self._description

    @property
    def cardinality(self) -> MeemooSIPConstraintCardinality:
        return self._cardinality

    @property
    def obligation(self) -> MeemooSIPConstraintObligation:
        return self._obligation

    @property
    def sip_level(self) -> MeemooSIPConstraintSIPLevel:
        return self._sip_level

    @property
    def datatype(self) -> MeemooSIPConstraintDatatype:
        return self._datatype

    @property
    def xml_node_type(self) -> MeemooSIPConstraintXMLNodeType:
        return self._xml_node_type

    @property
    def filename(self) -> str | None:
        return self._filename

    @property
    def xpath(self) -> str | None:
        return self._xpath

    @override
    def __eq__(self, other):
        if isinstance(other, MeemooSIPConstraint):
            return (
                self.identification == other.identification
                and self.description == other.description
                and self.cardinality == other.cardinality
                and self.obligation == other.obligation
                and self.sip_level == other.sip_level
                and self.datatype == other.datatype
                and self.xml_node_type == other.xml_node_type
                and self.filename == other.filename
                and self.xpath == other.xpath
            )
        return False


class MeemooSIPConstraintEvaluation:
    """Class describing the evaluation of a meemoo SIP constraint.

    Attributes:
        _constraint: The meemoo SIP constraint.
        _status: The status of the evaluation.
        _message: Additional message about the evaluation, if applicable.
    """

    def __init__(
        self,
        constraint: MeemooSIPConstraint,
        status: MeemooSIPConstraintEvaluationStatus,
        message: str | None = None,
    ):
        self._constraint = constraint
        self._status = status
        self._message = message

    @property
    def constraint(self) -> MeemooSIPConstraint:
        return self._constraint

    @property
    def status(self) -> MeemooSIPConstraintEvaluationStatus:
        return self._status

    @property
    def message(self) -> str | None:
        return self._message

    def is_valid(self) -> bool:
        return self.status == MeemooSIPConstraintEvaluationStatus.SUCCESS

    @override
    def __eq__(self, other):
        if isinstance(other, MeemooSIPConstraintEvaluation):
            return (
                self.constraint == other.constraint
                and self.status == other.status
                and self.message == other.message
            )
        return False
