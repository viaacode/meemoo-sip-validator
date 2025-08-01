# pyright: reportExplicitAny = false, reportAny = false

from functools import reduce
from typing import Any, cast
from collections.abc import Iterable

from edtf_validate.valid_edtf import conformsLevel0, conformsLevel1  # pyright: ignore[reportMissingTypeStubs, reportUnknownVariableType]

from ..report import RuleResult, Report
from ..models import SIP, DCPlusSchema, EDTF
from ..codes import Code


def is_valid_mediahaven_edtf(edtf: EDTF) -> bool:
    match edtf.xsi_type:
        case "{http://id.loc.gov/datatypes/edtf/}EDTF-level0":
            return conformsLevel0(edtf.text)  # pyright: ignore[reportUnknownVariableType]
        case "{http://id.loc.gov/datatypes/edtf/}EDTF-level1":
            return conformsLevel1(edtf.text)  # pyright: ignore[reportUnknownVariableType]
        case "{http://id.loc.gov/datatypes/edtf/}EDTF-level2":
            return edtf.text == "XXXX-XX-XX"


def check_edtf_values(sip: SIP[DCPlusSchema]) -> RuleResult[EDTF]:
    dc_schema = sip.metadata.descriptive
    all_edtf = collect_edtfs(dc_schema)
    invalid_edtfs = [edtf for edtf in all_edtf if not is_valid_mediahaven_edtf(edtf)]

    # TODO: create new check or better message for unsupported level 2
    return RuleResult(
        code=Code.edtf_valid,
        failed_items=invalid_edtfs,
        fail_msg=lambda edtf: f"Invalid EDTF level {edtf.xsi_type[-1]} value '{edtf.text}'.",
        success_msg="Validated EDTF values in dc+schema.xml.",
    )


def collect_edtfs(obj: object) -> list[EDTF]:
    result: list[EDTF] = []
    is_builtin = obj.__class__.__module__ == "builtins"

    if isinstance(obj, EDTF):
        result.append(obj)
    elif isinstance(obj, (list, tuple, set)):
        obj = cast(Iterable[Any], obj)
        for subvalue in obj:
            result += collect_edtfs(subvalue)
    elif not is_builtin:
        for value in obj.__dict__.values():
            result += collect_edtfs(value)

    return result


checks = [
    check_edtf_values,
]


def validate_dc_schema(sip: SIP[DCPlusSchema]) -> Report:
    rule_results = (check(sip) for check in checks)
    reports = (rule.to_report() for rule in rule_results)
    return reduce(Report.__add__, reports)
