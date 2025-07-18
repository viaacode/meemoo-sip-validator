from dataclasses import dataclass, field
from enum import auto, StrEnum
from pathlib import Path


class MeemooSIPConstraintObligation(StrEnum):
    MAY = auto()
    SHOULD = auto()
    MUST = auto()
    MUST_NOT = auto()
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
    URL = auto()
    OR_ID = auto()
    FLOAT = auto()
    MIMETYPE = auto()
    UNSPECIFIED = auto()


class MeemooSIPConstraintXMLNodeType(StrEnum):
    GENERAL = auto()
    ELEMENT = auto()
    ATTRIBUTE = auto()
    UNSPECIFIED = auto()


class MeemooSIPConstraintEvaluationStatus(StrEnum):
    PASS = auto()  # Fully valid
    FAIL = auto()  # Invalid, MUST violated
    WARNING = auto()  # SHOULD violated
    INFO = auto()  # MAY violated
    UNSPECIFIED = auto()


@dataclass
class MeemooSIPConstraint:
    """Class describing a meemoo SIP constraint.

    Attributes:
        identification: The unique identifier.
        description: The description.
        cardinality: The cardinality, if applicable e.g. 0..1.
        obligation: Describes the obligation, if applicable e.g. MUST, SHOULD, ...
        sip_level: Which level of the SIP does the constraint apply to, if applicable.
        datatype: What is the datatype of the XML node the constraint applies to, if applicable.
        xml_node_type: Which type of XML node does the constraint apply to, if applicable.
        filename: The filename of the relevant file, if applicable.
        xpath: The XPath to the relevant XML node, if applicable.
    """

    identification: str
    description: str
    cardinality: MeemooSIPConstraintCardinality = (
        MeemooSIPConstraintCardinality.UNSPECIFIED
    )
    obligation: MeemooSIPConstraintObligation = (
        MeemooSIPConstraintObligation.UNSPECIFIED
    )
    sip_level: MeemooSIPConstraintSIPLevel = MeemooSIPConstraintSIPLevel.UNSPECIFIED
    datatype: MeemooSIPConstraintDatatype = MeemooSIPConstraintDatatype.UNSPECIFIED
    xml_node_type: MeemooSIPConstraintXMLNodeType = (
        MeemooSIPConstraintXMLNodeType.UNSPECIFIED
    )
    path: str | None = None
    xpath: str | None = None

    def get_relative_path(self) -> Path:
        return Path(self.path).relative_to("/")


@dataclass
class MeemooSIPConstraintEvaluation:
    """Class describing the evaluation of a meemoo SIP constraint.

    Attributes:
        constraint: The meemoo SIP constraint.
        severity: The status of the evaluation.
        message: Additional message about the evaluation, if applicable.
        is_valid: Is the evaluation of the constraint valid or not.
    """

    constraint: MeemooSIPConstraint
    severity: MeemooSIPConstraintEvaluationStatus
    message: str | None = None
    is_valid: bool = field(init=False)

    def __post_init__(self):
        self.is_valid = self._is_valid()

    def _is_valid(self) -> bool:
        return self.severity != MeemooSIPConstraintEvaluationStatus.FAIL


msip11 = MeemooSIPConstraint(
    "MSIP11",
    'This attribute must have the value "OTHER". The value of the `mets/@csip:OTHERCONTENTINFORMATIONTYPE` attribute describes the value of the profile of the meemoo SIP.',
    MeemooSIPConstraintCardinality.EXACTLY_ONE,
    MeemooSIPConstraintObligation.MUST,
    MeemooSIPConstraintSIPLevel.PACKAGE,
    MeemooSIPConstraintDatatype.STRING,
    MeemooSIPConstraintXMLNodeType.ATTRIBUTE,
    "/METS.xml",
    "/mets:mets/@csip:CONTENTINFORMATIONTYPE",
)
msip12 = MeemooSIPConstraint(
    "MSIP12",
    "This attribute is used to declare the Content Information Type Specification used when creating the SIP.<br>Meemoo uses this attribute to indicate which of meemoo's content profiles a SIP uses. Its value MUST be a valid URI which can be found on the different content profile pages, e.g. the URI `https://data.hetarchief.be/id/sip/2.1/basic` for the basic content profile which can be found on [its content profile page]({{ site.baseurl }}{% link docs/diginstroom/sip/2.1/profiles/basic.md %}).<br>ote that the sample above has the value of the basic profile as an example.",
    MeemooSIPConstraintCardinality.EXACTLY_ONE,
    MeemooSIPConstraintObligation.MUST,
    MeemooSIPConstraintSIPLevel.PACKAGE,
    MeemooSIPConstraintDatatype.URI,
    MeemooSIPConstraintXMLNodeType.ATTRIBUTE,
    "/METS.xml",
    '/mets:mets[@csip:CONTENTINFORMATIONTYPE="OTHER"]/@csip:OTHERCONTENTINFORMATIONTYPE',
)
