from pathlib import Path

from lxml import etree
from lxml.etree import _ElementTree
from py_commons_ip.sip_validator import EARKSIPValidator

from .constraints import (
    MeemooSIPConstraintEvaluation,
    MeemooSIPConstraintEvaluationStatus,
    msip0011,
    msip0012,
)

NAMESPACES = {
    "mets": "http://www.loc.gov/METS/",
    "csip": "https://DILCIS.eu/XML/METS/CSIPExtensionMETS",
}


class EARKValidation:
    """A sort of wrapper around the E-ARK validation.

    Attributes:
        _report - The E-ARK validation report
        _is_valid - A boolean specifying  if the validation was successful
    """

    def __init__(self):
        self._report = None
        self._is_valid = None

    @property
    def report(self) -> str:
        return self._report

    @report.setter
    def report(self, value: str):
        self._report = value

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    @is_valid.setter
    def is_valid(self, value: bool):
        self._is_valid = value


class ValidationReport:
    """Class representing the validation report.

    Attributes:
        - _constraint_evaluations: A list of evaluations of constraints.
    """

    def __init__(
        self,
    ):
        self._constraint_evaluations = []

    @property
    def constraint_evaluations(self) -> list[MeemooSIPConstraintEvaluation]:
        return self._constraint_evaluations

    def add_constraint_evaluation(
        self, constraint_evaluation: MeemooSIPConstraintEvaluation
    ):
        self.constraint_evaluations.append(constraint_evaluation)

    def add_constraint_evaluations(
        self, constraint_evaluations: list[MeemooSIPConstraintEvaluation]
    ):
        self.constraint_evaluations.extend(constraint_evaluations)

    def is_valid(self) -> bool:
        for constraint_eval in self.constraint_evaluations:
            if not constraint_eval.is_valid:
                return False
        return True


class MeemooSIPValidator:
    """Class validating a meemoo SIP.

    Attributes:
        _unzipped_path: The path to the unzipped SIP.
        _eark_validation_report: Sort of wrapper around the E-ARK validation report.
        _validation_report: The validation report containing all the validations.
    """

    def __init__(self, unzipped_path: Path):
        """Initialize a validator.

        Args:
            unzipped_path: The folder pointing to an unzipped SIP.
        """
        self._unzipped_path = unzipped_path
        self._eark_validation_report = EARKValidation()
        self._validation_report = ValidationReport()

    @property
    def unzipped_path(self) -> Path:
        return self._unzipped_path

    @property
    def eark_validation_report(self) -> EARKValidation:
        return self._eark_validation_report

    @property
    def validation_report(self) -> ValidationReport:
        return self._validation_report

    def validate(self) -> bool:
        """Validate an unzipped SIP.

        Returns:
            bool - If the validation was successful.
        """

        # E-ARK validation
        # TODO: The SIP profile actually states which E-ARK SIP version it is based on.
        #       It should parse the SIP profile first and then run the appropriate E-ARK
        #       validation.
        eark_status, eark_report = self._validate_eark()
        self.eark_validation_report.is_valid = eark_status
        self.eark_validation_report.report = eark_report

        if not eark_status:
            return False

        try:
            root = etree.parse(Path(self.unzipped_path, "METS.xml"))
        except (etree.ParseError, OSError) as e:
            # Should not happen because we already validated E-ARK validity
            raise ValueError(f"METS could not be parsed: {e}.")

        # Meemoo SIP validation

        # Necessary constraints msip0011 and msip0012 to determine profile
        msip0011_validation = self._validate_msip0011(root)
        self.validation_report.add_constraint_evaluation(msip0011_validation)
        if not msip0011_validation.is_valid:
            # We can stop
            return False

        msip0012_validation = self._validate_msip0012(root)
        self.validation_report.add_constraint_evaluation(msip0012_validation)
        if not msip0012_validation.is_valid:
            # We can stop
            return False

    def _validate_eark(self) -> tuple[bool, str]:
        eark_validator = EARKSIPValidator()
        success, eark_report = eark_validator.validate(self.unzipped_path)

        return success, eark_report

    def _validate_msip0011(self, root: _ElementTree) -> MeemooSIPConstraintEvaluation:
        """Validate the msip0011 constraint.

        Checks if the SIP is valid against the msip0011 constraint.

        Returns:
            MeemooSIPConstraintEvaluation: Containing the evaluation of constraint msip0011.
        """
        try:
            content_information_type = root.xpath(
                "/mets:mets/@csip:CONTENTINFORMATIONTYPE",
                namespaces=NAMESPACES,
            )[0]
        except IndexError:
            return MeemooSIPConstraintEvaluation(
                msip0011,
                MeemooSIPConstraintEvaluationStatus.FAIL,
                "The package METS does not contain a CONTENTINFORMATIONTYPE attribute. See: `mets/@csip:CONTENTINFORMATIONTYPE`",
            )

        if content_information_type != "OTHER":
            return MeemooSIPConstraintEvaluation(
                msip0011,
                MeemooSIPConstraintEvaluationStatus.FAIL,
                'The value of the CONTENTINFORMATIONTYPE attribute MUST be "OTHER". See: `mets/@csip:CONTENTINFORMATIONTYPE`',
            )

        return MeemooSIPConstraintEvaluation(
            msip0011,
            MeemooSIPConstraintEvaluationStatus.PASS,
        )

    def _validate_msip0012(self, root: _ElementTree) -> MeemooSIPConstraintEvaluation:
        """Validate the msip0012 constraint.

        Checks if the SIP is valid against the msip0012 constraint.

        Returns:
            MeemooSIPConstraintEvaluation: Containing the evaluation of constraint msip0012.
        """
        try:
            profile_type = root.xpath(
                "/mets:mets/@csip:OTHERCONTENTINFORMATIONTYPE",
                namespaces=NAMESPACES,
            )[0]
        except IndexError:
            return MeemooSIPConstraintEvaluation(
                msip0012,
                MeemooSIPConstraintEvaluationStatus.FAIL,
                "METS does not contain a OTHERCONTENTINFORMATIONTYPE attribute. See: `mets/@csip:OTHERCONTENTINFORMATIONTYPE`",
            )

        if profile_type == "https://data.hetarchief.be/id/sip/2.1/basic":
            return MeemooSIPConstraintEvaluation(
                msip0012,
                MeemooSIPConstraintEvaluationStatus.PASS,
                "https://data.hetarchief.be/id/sip/2.1/basic",
            )

        elif profile_type == "https://data.hetarchief.be/id/sip/2.1/bibliographic":
            return MeemooSIPConstraintEvaluation(
                msip0012,
                MeemooSIPConstraintEvaluationStatus.PASS,
                "https://data.hetarchief.be/id/sip/2.1/bibliographic",
            )

        elif profile_type == "https://data.hetarchief.be/id/sip/2.1/material-artwork":
            return MeemooSIPConstraintEvaluation(
                msip0012,
                MeemooSIPConstraintEvaluationStatus.PASS,
                "https://data.hetarchief.be/id/sip/2.1/material-artwork",
            )

        elif profile_type == "https://data.hetarchief.be/id/sip/2.1/film":
            return MeemooSIPConstraintEvaluation(
                msip0012,
                MeemooSIPConstraintEvaluationStatus.PASS,
                "https://data.hetarchief.be/id/sip/2.1/film",
            )
        else:
            return MeemooSIPConstraintEvaluation(
                msip0012,
                MeemooSIPConstraintEvaluationStatus.FAIL,
                "The value of the OTHERCONTENTINFORMATIONTYPE attribute does not contain a valid value. See: `mets/@csip:OTHERCONTENTINFORMATIONTYPE`",
            )
