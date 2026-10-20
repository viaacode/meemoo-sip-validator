from unittest.mock import MagicMock, patch

import pytest
from eark_models.premis.v3_0 import (  # pyright: ignore[reportMissingTypeStubs]
    File,
    Fixity,
    IntellectualEntity,
    MessageDigest,
    MessageDigestAlgorithm,
    ObjectCharacteristics,
    ObjectIdentifier,
    ObjectIdentifierType,
    ObjectIdentifierValue,
    Premis,
)

from meemoo_sip_validator.v2_1._core.premis.premis import (
    check_fixity_message_digest_matches_actual_hash,
    check_object_identifier_type_uuid_existance,
    check_object_identifier_type_vocabulary,
    check_object_identifiers_uniqueness,
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


def object_identifier(type: str, value: str) -> ObjectIdentifier:
    return ObjectIdentifier(
        __source__="xml",
        type=ObjectIdentifierType(
            __source__="xml",
            text=type,
            authority=None,
            authority_uri=None,
            value_uri=None,
        ),
        value=ObjectIdentifierValue(__source__="xml", text=value),
        simple_link=None,
    )


def premis_with_ie(identifiers: list[ObjectIdentifier]) -> Premis:
    ie = IntellectualEntity(
        __source__="xml",
        xsi_type="{http://www.loc.gov/premis/v3}intellectualEntity",
        identifiers=identifiers,
        significant_properties=[],
        original_name=None,
        relationships=[],
    )
    return Premis(__source__="xml", version="3.0", objects=[ie], events=[], agents=[])


UUID = "e4a0b8f2-3c1d-4f5e-9a6b-7c8d9e0f1a2b"


def test_multiple_object_identifiers_of_same_type_with_different_values_are_allowed():
    premis = premis_with_ie(
        [
            object_identifier("UUID", UUID),
            object_identifier("MEEMOO-LOCAL-ID", "local-1"),
            object_identifier("MEEMOO-LOCAL-ID", "local-2"),
        ]
    )

    assert check_object_identifier_type_vocabulary([premis]).failed_items == []
    assert check_object_identifier_type_uuid_existance([premis]).failed_items == []
    assert check_object_identifiers_uniqueness([premis]).failed_items == []


def test_multiple_object_identifiers_of_same_type_with_same_value_are_rejected():
    premis = premis_with_ie(
        [
            object_identifier("UUID", UUID),
            object_identifier("MEEMOO-LOCAL-ID", "local-1"),
            object_identifier("MEEMOO-LOCAL-ID", "local-1"),
        ]
    )

    result = check_object_identifiers_uniqueness([premis])

    assert result.failed_items == [
        object_identifier("MEEMOO-LOCAL-ID", "local-1"),
        object_identifier("MEEMOO-LOCAL-ID", "local-1"),
    ]


def test_multiple_uuid_object_identifiers_are_allowed():
    # The spec requires exactly one identifier of type UUID per object,
    # but the validator currently only checks that there is at least one.
    premis = premis_with_ie(
        [
            object_identifier("UUID", UUID),
            object_identifier("UUID", "0f9e8d7c-6b5a-4f3e-2d1c-0b9a8f7e6d5c"),
        ]
    )

    assert check_object_identifier_type_uuid_existance([premis]).failed_items == []
    assert check_object_identifiers_uniqueness([premis]).failed_items == []
