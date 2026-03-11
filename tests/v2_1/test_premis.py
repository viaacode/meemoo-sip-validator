from unittest.mock import MagicMock, patch

import pytest
from eark_models.premis.v3_0 import (  # pyright: ignore[reportMissingTypeStubs]
    File,
    Fixity,
    MessageDigest,
    MessageDigestAlgorithm,
    ObjectCharacteristics,
    Premis,
)

from meemoo_sip_validator.v2_1._core.premis.premis import (
    check_fixity_message_digest_matches_actual_hash,
)


@patch("meemoo_sip_validator.v2_1._core.premis.helpers.get_data_path_for_file")
@patch("meemoo_sip_validator.v2_1._core.premis.helpers.calculate_message_digest")
@pytest.mark.parametrize(
    "md5_fixity",
    ["4499ECD616A3F8DA71DFAB6B845CED7D", "4499ecd616a3f8da71dfab6b845ced7d"],
)
def test_check_fixity_message_digest_matches_actual_hash(
    calc_mock: MagicMock,
    data_patch_mock: MagicMock,
    md5_fixity: str,
):
    calc_mock.return_value = "4499ecd616a3f8da71dfab6b845ced7d"

    premis_file = File(
        __source__="xml",
        xsi_type="{http://www.loc.gov/premis/v3}file",
        identifiers=[],
        significant_properties=[],
        characteristics=[
            ObjectCharacteristics(
                __source__="xml",
                fixity=[
                    Fixity(
                        __source__="xml",
                        message_digest_originator=None,
                        message_digest_algorithm=MessageDigestAlgorithm(
                            __source__="xml",
                            authority=None,
                            authority_uri=None,
                            value_uri=None,
                            text="MD5",
                        ),
                        message_digest=MessageDigest(__source__="xml", text=md5_fixity),
                    )
                ],
                size=None,
                format=[],
            )
        ],
        original_name=None,
        storages=[],
        relationships=[],
    )

    premis = Premis(
        __source__="xml", version="3.0", objects=[premis_file], events=[], agents=[]
    )

    results = check_fixity_message_digest_matches_actual_hash([premis])
    assert len(results.failed_items) == 0
    assert calc_mock.call_count == 1
    assert data_patch_mock.call_count == 1
