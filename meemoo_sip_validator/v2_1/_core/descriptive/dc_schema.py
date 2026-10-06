from functools import reduce
from pathlib import Path

from edtf_validate.valid_edtf import (  # pyright: ignore[reportMissingTypeStubs]
    conformsLevel0,  # pyright: ignore[reportUnknownVariableType]
    conformsLevel1,  # pyright: ignore[reportUnknownVariableType]
)

from .. import thesauri
from ..codes import Code
from ..models import EDTF, DCPlusSchema
from ..report import Failure, Report, RuleResult, Severity, TupleWithSource
from .collect import collect_instances


def is_valid_mediahaven_edtf(edtf: EDTF) -> bool:
    match edtf.xsi_type:
        case "{http://id.loc.gov/datatypes/edtf/}EDTF-level0":
            return conformsLevel0(edtf.text)  # pyright: ignore[reportUnknownVariableType]
        case "{http://id.loc.gov/datatypes/edtf/}EDTF-level1":
            return conformsLevel1(edtf.text)  # pyright: ignore[reportUnknownVariableType]
        case "{http://id.loc.gov/datatypes/edtf/}EDTF-level2":
            return edtf.text == "XXXX-XX-XX" or conformsLevel1(edtf.text)  # pyright: ignore[reportUnknownVariableType]


def check_edtf_values(dc_schema: DCPlusSchema) -> RuleResult[EDTF]:
    all_edtf = collect_instances(dc_schema, EDTF)
    invalid_edtfs = [edtf for edtf in all_edtf if not is_valid_mediahaven_edtf(edtf)]

    return RuleResult(
        code=Code.edtf_valid,
        failed_items=invalid_edtfs,
        fail_msg=lambda edtf: f"Invalid or unsupported EDTF level {edtf.xsi_type[-1]} with value '{edtf.text}'.",
        success_msg="Validated EDTF values in dc+schema.xml.",
    )


def check_license_vocabulary(
    dc_schema: DCPlusSchema,
) -> RuleResult[TupleWithSource[str]]:
    invalid_licenses = [
        TupleWithSource(__source__=dc_schema.__source__, items=(license,))
        for license in dc_schema.license
        if license not in thesauri.licenses
    ]
    return RuleResult(
        code=Code.license_thesauri,
        failed_items=invalid_licenses,
        fail_msg=lambda license: f"Unknown license '{license.items[0]}'.",
        success_msg="Validated licenses.",
    )


checks = [
    # The following constraints are check when creating the DCPlusSchema model
    # - Unique language tags
    # - Presence of a "nl" value
    # - Cardinalities
    check_edtf_values,
    check_license_vocabulary,
]


def validate_dc_schema(sip_path: Path) -> Report:
    descriptive_path = sip_path / "metadata" / "descriptive" / "dc+schema.xml"
    try:
        dc_schema = DCPlusSchema.from_xml(descriptive_path)
    except Exception as e:
        return Report(
            results=[
                Failure(
                    code=Code.xsd_valid,
                    message=str(e),
                    severity=Severity.ERROR,
                    source=str(descriptive_path),
                )
            ]
        )

    rule_results = (check(dc_schema) for check in checks)
    reports = (rule.to_report() for rule in rule_results)
    return reduce(Report.__add__, reports)
