from pathlib import Path

from lxml import etree

from meemoo_sip_validator.constraints import (
    MeemooSIPConstraintEvaluation,
    MeemooSIPConstraintEvaluationStatus,
)
from meemoo_sip_validator.v21.constraints import (
    msip7,
    msip151,
    msip152,
    msip154,
)
from meemoo_sip_validator.v21.validations import (
    validate_msip7,
    validate_msip151,
    validate_msip152,
    validate_msip154,
)


def test_validate_msip7_correct():
    path = Path(
        "tests",
        "resources",
        "v21",
        "msip7",
        "correct_mets",
        "METS.xml",
    )
    tree = etree.parse(path)

    assert validate_msip7(tree) == MeemooSIPConstraintEvaluation(
        msip7, MeemooSIPConstraintEvaluationStatus.PASS
    )


def test_validate_msip7_missing():
    path = Path(
        "tests",
        "resources",
        "v21",
        "msip7",
        "missing_mets",
        "METS.xml",
    )
    tree = etree.parse(path)

    assert validate_msip7(tree) == MeemooSIPConstraintEvaluation(
        msip7,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The element '{msip7.xpath}' is not present",
    )


def test_validate_msip151_correct():
    path = Path(
        "tests",
        "resources",
        "v21",
        "msip151",
        "correct_premis",
        "premis.xml",
    )
    tree = etree.parse(path)

    assert validate_msip151(tree) == MeemooSIPConstraintEvaluation(
        msip151,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_msip151_missing():
    path = Path(
        "tests",
        "resources",
        "v21",
        "msip151",
        "missing_premis",
        "premis.xml",
    )
    tree = etree.parse(path)

    assert validate_msip151(tree) == MeemooSIPConstraintEvaluation(
        msip151,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The element '{msip151.xpath}' is not present",
    )


def test_validate_msip152_correct():
    path = Path(
        "tests",
        "resources",
        "v21",
        "msip152",
        "correct_premis_version",
        "premis.xml",
    )
    tree = etree.parse(path)

    assert validate_msip152(tree) == MeemooSIPConstraintEvaluation(
        msip152,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_msip152_missing():
    path = Path(
        "tests",
        "resources",
        "v21",
        "msip152",
        "missing_premis_version",
        "premis.xml",
    )
    tree = etree.parse(path)

    assert validate_msip152(tree) == MeemooSIPConstraintEvaluation(
        msip152,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The attribute '{msip152.xpath}' is not present",
    )


def test_validate_msip152_wrong():
    path = Path(
        "tests",
        "resources",
        "v21",
        "msip152",
        "wrong_premis_version",
        "premis.xml",
    )
    tree = etree.parse(path)

    assert validate_msip152(tree) == MeemooSIPConstraintEvaluation(
        msip152,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The value of '{msip152.xpath}' is different than '3.0'",
    )


def test_validate_msip154_correct():
    path = Path(
        "tests",
        "resources",
        "v21",
        "msip154",
        "correct_premis",
    )

    assert validate_msip154(path) == MeemooSIPConstraintEvaluation(
        msip154,
        MeemooSIPConstraintEvaluationStatus.PASS,
    )


def test_validate_msip154_missing():
    path = Path(
        "tests",
        "resources",
        "v21",
        "msip154",
        "missing_premis",
    )

    assert validate_msip154(path) == MeemooSIPConstraintEvaluation(
        msip154,
        MeemooSIPConstraintEvaluationStatus.FAIL,
        f"The file {path.joinpath('metadata', 'preservation', 'premis.xml')} is not found",
    )
