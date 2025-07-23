from typing import Literal
from enum import StrEnum, auto

from pydantic import BaseModel


class Severity(StrEnum):
    ERROR = auto()
    WARNING = auto()
    INFO = auto()


class Error(BaseModel):
    result: Literal["error"] = "error"
    code: str
    message: str
    severity: Severity


class Success(BaseModel):
    result: Literal["success"] = "success"
    code: str
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
