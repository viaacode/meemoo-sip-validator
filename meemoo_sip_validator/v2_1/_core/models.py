from typing import Literal
from enum import StrEnum, auto

from pydantic import BaseModel

# Make sip models available through this module
from eark_models.sip.v2_2_0 import SIP as SIP
from eark_models.premis.v3_0 import Premis as Premis
import eark_models.premis.v3_0 as premis

_ = premis  # fixes unused import error

from .codes import Code


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
