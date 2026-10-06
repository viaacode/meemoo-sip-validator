from functools import reduce
from pathlib import Path

from edtf_validate.valid_edtf import (  # pyright: ignore[reportMissingTypeStubs]
    conformsLevel1,  # pyright: ignore[reportUnknownVariableType]
)

from ..codes import Code
from ..models import Mods, ModsDate
from ..report import Failure, Report, RuleResult, Severity, TupleWithSource
from .collect import collect_instances


def is_valid_edtf(text: str) -> bool:
    # The spec defines EDTF as "up to level 1 plus the value `XXXX` to indicate
    # an unknown date". MODS has no xsi:type to pick a level, unlike dc+schema.
    return text == "XXXX" or conformsLevel1(text)  # pyright: ignore[reportUnknownVariableType]


def check_edtf_values(
    mods: Mods, mods_path: Path
) -> RuleResult[TupleWithSource[ModsDate]]:
    all_dates = collect_instances(mods, ModsDate)
    invalid_dates = [
        TupleWithSource(__source__=str(mods_path), items=(date,))
        for date in all_dates
        if date.encoding == "edtf" and not is_valid_edtf(date.text)
    ]

    return RuleResult(
        code=Code.edtf_valid,
        failed_items=invalid_dates,
        fail_msg=lambda date: f"Invalid or unsupported EDTF value '{date.items[0].text}'.",
        success_msg="Validated EDTF values in mods.xml.",
    )


checks = [
    check_edtf_values,
]


def validate_mods(sip_path: Path) -> Report:
    descriptive_path = sip_path / "metadata" / "descriptive" / "mods.xml"
    try:
        mods = Mods.from_xml(descriptive_path)
    except Exception as e:
        return Report(
            results=[
                Failure(
                    code=Code.xsd_valid,
                    message=str(e) or repr(e),
                    severity=Severity.ERROR,
                    source=str(descriptive_path),
                )
            ]
        )

    rule_results = (check(mods, descriptive_path) for check in checks)
    reports = (rule.to_report() for rule in rule_results)
    return reduce(Report.__add__, reports)
