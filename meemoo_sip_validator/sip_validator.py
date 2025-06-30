from pathlib import Path

from py_commons_ip.sip_validator import EARKSIPValidator

from .constraints import (
    MeemooSIPConstraintEvaluation,
)


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
            if not constraint_eval.is_valid():
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
        """Validate an unzipped SIP making use of the commons-IP validator.

        Returns:
            bool - If the validation was successful.
        """

        # E-ARK validation
        eark_status, eark_report = self._validate_eark()
        self.eark_validation_report.is_valid = eark_status
        self.eark_validation_report.report = eark_report

        return eark_status

    def _validate_eark(self) -> tuple[bool, str]:
        eark_validator = EARKSIPValidator()
        success, eark_report = eark_validator.validate(self.unzipped_path)

        return success, eark_report
