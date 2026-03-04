import pytest
from eark_models.dc_schema.v2_1 import EDTF  # pyright: ignore[reportMissingTypeStubs]

from meemoo_sip_validator.v2_1._core.descriptive.dc_schema import (
    is_valid_mediahaven_edtf,
)


@pytest.mark.parametrize("edtf_value", ["2026-02-24T11:21:02Z", "1984?", "XXXX-XX-XX"])
def test_is_valid_mediahaven_edtf_level2(edtf_value: str):
    edtf = EDTF(
        __source__="xml",
        xsi_type="{http://id.loc.gov/datatypes/edtf/}EDTF-level2",
        text=edtf_value,
    )
    assert is_valid_mediahaven_edtf(edtf)
