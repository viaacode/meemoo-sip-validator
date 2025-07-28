from typing import Literal, Generator, Callable
from enum import StrEnum, auto

from pydantic import BaseModel

# Make sip models available through this module
from eark_models.sip.v2_2_0 import SIP as SIP
import eark_models.premis.v3_0 as premis

from .codes import Code

_ = premis  # fixes unused import error


class Severity(StrEnum):
    ERROR = auto()
    WARNING = auto()
    INFO = auto()


class Error(BaseModel):
    result: Literal["error"] = "error"
    code: Code
    message: str
    severity: Severity


class Success(BaseModel):
    result: Literal["success"] = "success"
    code: Code
    message: str


class Report(BaseModel):
    results: list[Success | Error]

    def __add__(self, other: "Report") -> "Report":
        return Report(results=self.results + other.results)

    @property
    def outcome(self) -> Literal["PASSED", "FAILED"]:
        failed = any(
            isinstance(result, Error) and result.severity == Severity.ERROR
            for result in self.results
        )
        return "FAILED" if failed else "PASSED"

    @property
    def errors(self) -> Generator[Error, None, None]:
        return (result for result in self.results if isinstance(result, Error))

    @property
    def successes(self) -> Generator[Success, None, None]:
        return (result for result in self.results if isinstance(result, Success))


class RuleResult[T](BaseModel):
    code: Code
    error_items: list[T]
    error_msg: Callable[[T], str]
    success_msg: str

    def to_report(self) -> Report:
        no_errors = len(self.error_items) == 0
        report_results: list[Success | Error] = []
        if no_errors:
            report_results.append(Success(code=self.code, message=self.success_msg))
        else:
            for error_item in self.error_items:
                error_msg = self.error_msg(error_item)
                report_results.append(
                    Error(code=self.code, message=error_msg, severity=Severity.ERROR)
                )

        return Report(results=report_results)
