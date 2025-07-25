from typing import Literal, Generator
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
