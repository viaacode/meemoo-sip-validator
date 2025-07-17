from pathlib import Path

import pytest
from lxml import etree

from meemoo_sip_validator.constraints import (
    MeemooSIPConstraintEvaluation,
    MeemooSIPConstraintEvaluationStatus,
    msip11,
    msip12,
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

    def test_validate_msip11_correct(self, meemoo_sip_validator):
        path = Path(
            "tests",
            "resources",
            "msip11",
            "correct_contentinformationtype",
            "METS.xml",
        )
        root = etree.parse(path)
        assert meemoo_sip_validator._validate_msip11(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip11,
            MeemooSIPConstraintEvaluationStatus.PASS,
        )

    def test_validate_msip11_missing(self, meemoo_sip_validator):
        path = Path(
            "tests",
            "resources",
            "msip11",
            "missing_contentinformationtype",
            "METS.xml",
        )
        root = etree.parse(path)
        assert meemoo_sip_validator._validate_msip11(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip11,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            "The package METS does not contain a CONTENTINFORMATIONTYPE attribute. See: `mets/@csip:CONTENTINFORMATIONTYPE`",
        )

    def test_validate_msip11_wrong(self, meemoo_sip_validator):
        path = Path(
            "tests",
            "resources",
            "msip11",
            "wrong_contentinformationtype",
            "METS.xml",
        )
        root = etree.parse(path)
        assert meemoo_sip_validator._validate_msip11(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip11,
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
    def test_validate_msip12_correct(self, subpath, profile_type, meemoo_sip_validator):
        path = Path(
            "tests",
            "resources",
            "msip12",
            f"correct_othercontentinformationtype_{subpath}",
            "METS.xml",
        )

        root = etree.parse(path)

        assert meemoo_sip_validator._validate_msip12(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip12,
            MeemooSIPConstraintEvaluationStatus.PASS,
            f"https://data.hetarchief.be/id/sip/{profile_type}",
        )

    def test_validate_msip12_missing(self, meemoo_sip_validator):
        path = Path(
            "tests",
            "resources",
            "msip12",
            "missing_othercontentinformationtype",
            "METS.xml",
        )

        root = etree.parse(path)

        assert meemoo_sip_validator._validate_msip12(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip12,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            "METS does not contain a OTHERCONTENTINFORMATIONTYPE attribute. See: `mets/@csip:OTHERCONTENTINFORMATIONTYPE`",
        )

    def test_validate_msip12_wrong(self, meemoo_sip_validator):
        path = Path(
            "tests",
            "resources",
            "msip12",
            "wrong_othercontentinformationtype",
            "METS.xml",
        )

        root = etree.parse(path)

        assert meemoo_sip_validator._validate_msip12(
            root
        ) == MeemooSIPConstraintEvaluation(
            msip12,
            MeemooSIPConstraintEvaluationStatus.FAIL,
            "The value of the OTHERCONTENTINFORMATIONTYPE attribute does not contain a valid value. See: `mets/@csip:OTHERCONTENTINFORMATIONTYPE`",
        )
