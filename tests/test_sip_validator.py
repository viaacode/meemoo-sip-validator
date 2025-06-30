from pathlib import Path

from meemoo_sip_validator.sip_validator import (
    MeemooSIPValidator,
    EARKValidation,
)


class TestMeemooSipValidator:

    def test_init(self):
        path = Path("path", "to", "sip")
        validator = MeemooSIPValidator(path)
        assert validator.unzipped_path == path
        assert isinstance(validator.eark_validation_report, EARKValidation)
        assert validator.eark_validation_report.is_valid is None
