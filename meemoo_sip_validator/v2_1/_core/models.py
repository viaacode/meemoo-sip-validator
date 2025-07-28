from typing import Literal, Generator, Callable
from enum import Enum

from pydantic import BaseModel

# Make sip models available through this module
from eark_models.sip.v2_2_0 import SIP as SIP
import eark_models.premis.v3_0 as premis

from .codes import Code

_ = premis  # fixes unused import error


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


class Failure(BaseModel):
    result: Literal["FAIL"] = "FAIL"
    code: Code
    message: str
    severity: Severity


class Success(BaseModel):
    result: Literal["PASS"] = "PASS"
    code: Code
    message: str


class Report(BaseModel):
    results: list[Success | Failure]

    def __add__(self, other: "Report") -> "Report":
        return Report(results=self.results + other.results)

    @property
    def outcome(self) -> Literal["PASSED", "FAILED"]:
        failed = any(
            isinstance(result, Failure) and result.severity == Severity.ERROR
            for result in self.results
        )
        return "FAILED" if failed else "PASSED"

    @property
    def failures(self) -> Generator[Failure, None, None]:
        return (result for result in self.results if isinstance(result, Failure))

    @property
    def successes(self) -> Generator[Success, None, None]:
        return (result for result in self.results if isinstance(result, Success))


class RuleResult[T](BaseModel):
    code: Code
    failed_items: list[T]
    fail_msg: Callable[[T], str]
    success_msg: str

    def to_report(self) -> Report:
        no_failures = len(self.failed_items) == 0
        report_results: list[Success | Failure] = []
        if no_failures:
            report_results.append(Success(code=self.code, message=self.success_msg))
        else:
            for fail_item in self.failed_items:
                report_results.append(
                    Failure(
                        code=self.code,
                        message=self.fail_msg(fail_item),
                        severity=Severity.ERROR,
                    )
                )

        return Report(results=report_results)
