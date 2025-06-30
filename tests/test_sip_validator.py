from pathlib import Path


import pytest
from lxml import etree

from meemoo_sip_validator.constraints import (
    MeemooSIPConstraintEvaluation,
    MeemooSIPConstraintEvaluationStatus,
    msip0011,
    msip0012,
)
from meemoo_sip_validator.sip_validator import (
    MeemooSIPValidator,
    EARKValidation,
    ValidationReport,
)


class TestMeemooSipValidator:

    @pytest.fixture
    def meemoo_sip_validator(self) -> MeemooSIPValidator:
        return MeemooSIPValidator(Path("path", "to", "sip"))

    def test_init(self, meemoo_sip_validator):
        assert meemoo_sip_validator.unzipped_path == Path("path", "to", "sip")
        assert isinstance(meemoo_sip_validator.eark_validation_report, EARKValidation)
        assert meemoo_sip_validator.eark_validation_report.is_valid is None
        assert isinstance(meemoo_sip_validator.validation_report, ValidationReport)
        assert meemoo_sip_validator.validation_report.is_valid()

    def test_validate_msip0011_correct(self, meemoo_sip_validator):
        path = Path(
            "tests",
            "resources",
            "msip0011",
            "correct_contentinformationtype",
            "METS.xml",
        )
        root = etree.parse(path)
        assert meemoo_sip_validator._validate_msip0011(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip0011,
            MeemooSIPConstraintEvaluationStatus.SUCCESS,
        )

    def test_validate_msip0011_missing(self, meemoo_sip_validator):
        path = Path(
            "tests",
            "resources",
            "msip0011",
            "missing_contentinformationtype",
            "METS.xml",
        )
        root = etree.parse(path)
        assert meemoo_sip_validator._validate_msip0011(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip0011,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            "The package METS does not contain a CONTENTINFORMATIONTYPE attribute. See: `mets/@csip:CONTENTINFORMATIONTYPE`",
        )

    def test_validate_msip0011_wrong(self, meemoo_sip_validator):
        path = Path(
            "tests",
            "resources",
            "msip0011",
            "wrong_contentinformationtype",
            "METS.xml",
        )
        root = etree.parse(path)
        assert meemoo_sip_validator._validate_msip0011(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip0011,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            'The value of the CONTENTINFORMATIONTYPE attribute MUST be "OTHER". See: `mets/@csip:CONTENTINFORMATIONTYPE`',
        )

    @pytest.mark.parametrize(
        "subpath, profile_type",
        [
            ("2_1_basic", "2.1/basic"),
            ("2_1_bibliographic", "2.1/bibliographic"),
            ("2_1_film", "2.1/film"),
            ("2_1_material_artwork", "2.1/material-artwork"),
        ],
    )
    def test_validate_msip0012_correct(
        self, subpath, profile_type, meemoo_sip_validator
    ):
        path = Path(
            "tests",
            "resources",
            "msip0012",
            f"correct_othercontentinformationtype_{subpath}",
            "METS.xml",
        )

        root = etree.parse(path)

        assert meemoo_sip_validator._validate_msip0012(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip0012,
            MeemooSIPConstraintEvaluationStatus.SUCCESS,
            f"https://data.hetarchief.be/id/sip/{profile_type}",
        )

    def test_validate_msip0012_missing(self, meemoo_sip_validator):
        path = Path(
            "tests",
            "resources",
            "msip0012",
            "missing_othercontentinformationtype",
            "METS.xml",
        )

        root = etree.parse(path)

        assert meemoo_sip_validator._validate_msip0012(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip0012,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            "METS does not contain a OTHERCONTENTINFORMATIONTYPE attribute. See: `mets/@csip:OTHERCONTENTINFORMATIONTYPE`",
        )

    def test_validate_msip0012_wrong(self, meemoo_sip_validator):
        path = Path(
            "tests",
            "resources",
            "msip0012",
            "wrong_othercontentinformationtype",
            "METS.xml",
        )

        root = etree.parse(path)

        assert meemoo_sip_validator._validate_msip0012(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip0012,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            "The value of the OTHERCONTENTINFORMATIONTYPE attribute does not contain a valid value. See: `mets/@csip:OTHERCONTENTINFORMATIONTYPE`",
        )
