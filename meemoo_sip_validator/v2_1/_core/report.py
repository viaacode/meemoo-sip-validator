from typing import Literal, Callable, Protocol, Any
from collections.abc import Generator
from enum import Enum
from dataclasses import dataclass

from .codes import Code


class Severity(str, Enum):
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class Failure:
    code: Code
    message: str
    severity: Severity
    source: str
    result: Literal["FAIL"] = "FAIL"

    def to_dict(self) -> dict[str, Any]:
        return {
            # "code": self.code, # Include this once the constraints list is finilized
            "message": self.message,
            "severity": self.severity,
            "source": self.source,
            "result": self.result,
        }


@dataclass
class Success:
    code: Code
    message: str
    result: Literal["PASS"] = "PASS"

    def to_dict(self) -> dict[str, Any]:
        return {
            # "code": self.code, # Include this once the constraints list is finilized
            "message": self.message,
            "result": self.result,
        }


@dataclass
class Report:
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
    def is_valid(self) -> bool:
        return self.outcome == "PASSED"

    @property
    def failures(self) -> Generator[Failure, None, None]:
        return (result for result in self.results if isinstance(result, Failure))

    @property
    def successes(self) -> Generator[Success, None, None]:
        return (result for result in self.results if isinstance(result, Success))

    def to_dict(self) -> dict[str, Any]:
        return {"results": [result.to_dict() for result in self.results]}


class WithSource(Protocol):
    __source__: str


@dataclass
class RuleResult[T: WithSource]:
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
                        source=fail_item.__source__,
                    )
                )

        return Report(results=report_results)


@dataclass(kw_only=True)
class TupleWithSource[*T]:
    __source__: str
    items: tuple[*T]
