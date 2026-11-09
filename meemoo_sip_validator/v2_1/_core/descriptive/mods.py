from functools import reduce
from pathlib import Path

from edtf_validate.valid_edtf import (  # pyright: ignore[reportMissingTypeStubs]
    conformsLevel1,  # pyright: ignore[reportUnknownVariableType]
)

from ..codes import Code
from ..models import Mods, ModsDate, ModsTopic
from ..report import Failure, Report, RuleResult, Severity, TupleWithSource
from .collect import collect_instances


def is_valid_edtf(text: str) -> bool:
    # EDTF levels 0 and 1, plus the level 2 value `XXXX-XX-XX` for a fully
    # unknown date. MODS has no xsi:type to pick a level, unlike dc+schema.
    return text == "XXXX-XX-XX" or conformsLevel1(text)  # pyright: ignore[reportUnknownVariableType]


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


def missing_dutch(
    values: list[str | None], element: str, mods_path: Path
) -> list[TupleWithSource[str]]:
    """
    One failure when there are values (their xml:lang) but none is Dutch.
    MediaHaven takes only the Dutch values, so at least one must be there.
    """
    if len(values) == 0 or "nl" in values:
        return []
    return [TupleWithSource(__source__=str(mods_path), items=(element,))]


def check_dutch_genre(mods: Mods, mods_path: Path) -> RuleResult[TupleWithSource[str]]:
    return RuleResult(
        code=Code.mods_genre_dutch,
        failed_items=missing_dutch(
            [genre.xml_lang for genre in mods.genres], "mods:genre", mods_path
        ),
        fail_msg=lambda item: f'No {item.items[0]} has xml:lang="nl"; at least one must (BICP33).',
        success_msg="Validated that a mods:genre is in Dutch.",
    )


def check_dutch_topic(mods: Mods, mods_path: Path) -> RuleResult[TupleWithSource[str]]:
    topics = [
        p for subject in mods.subjects for p in subject.properties if isinstance(p, ModsTopic)
    ]
    return RuleResult(
        code=Code.mods_topic_dutch,
        failed_items=missing_dutch(
            [topic.xml_lang for topic in topics], "mods:subject/mods:topic", mods_path
        ),
        fail_msg=lambda item: f'No {item.items[0]} has xml:lang="nl"; at least one must (BICP37).',
        success_msg="Validated that a mods:topic is in Dutch.",
    )


checks = [
    check_edtf_values,
    check_dutch_genre,
    check_dutch_topic,
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
