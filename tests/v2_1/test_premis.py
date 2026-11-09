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
    RelatedObjectIdentifier,
    RelatedObjectIdentifierType,
    RelatedObjectIdentifierValue,
    Relationship,
    RelationshipSubType,
    RelationshipType,
)

from meemoo_sip_validator.v2_1._core.premis.premis import (
    check_fixity_message_digest_matches_actual_hash,
    check_object_identifier_type_uuid_existance,
    check_object_identifier_type_vocabulary,
    check_object_identifiers_uniqueness,
    check_related_objects_inverse_relationship_valid,
    check_relationships_sub_type_vocabulary,
    check_relationships_sub_type_vocabulary_per_object_type,
    check_relationships_type_vocabulary,
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


def relationship(type: str, sub_type: str, related_uuid: str) -> Relationship:
    return Relationship(
        __source__="xml",
        type=RelationshipType(
            __source__="xml",
            text=type,
            authority=None,
            authority_uri=None,
            value_uri=None,
        ),
        sub_type=RelationshipSubType(
            __source__="xml",
            text=sub_type,
            authority=None,
            authority_uri=None,
            value_uri=None,
        ),
        related_object_identifiers=[
            RelatedObjectIdentifier(
                __source__="xml",
                type=RelatedObjectIdentifierType(
                    __source__="xml",
                    text="UUID",
                    authority=None,
                    authority_uri=None,
                    value_uri=None,
                ),
                value=RelatedObjectIdentifierValue(__source__="xml", text=related_uuid),
                simple_link=None,
            )
        ],
        related_event_identifiers=[],
    )


def premis_file(uuid: str, relationships: list[Relationship]) -> File:
    return File(
        __source__="xml",
        xsi_type="{http://www.loc.gov/premis/v3}file",
        identifiers=[object_identifier("UUID", uuid)],
        significant_properties=[],
        characteristics=[],
        original_name=None,
        storages=[],
        relationships=relationships,
    )


def premis_with_files(files: list[File]) -> Premis:
    return Premis(__source__="xml", version="3.0", objects=files, events=[], agents=[])


PDF_UUID = "1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d"
TIFF_UUID = "6e7f8a9b-0c1d-4e2f-3a4b-5c6d7e8f9a0b"


def test_derivation_pair_on_files_is_valid():
    premis = premis_with_files(
        [
            premis_file(
                PDF_UUID, [relationship("derivation", "has source", TIFF_UUID)]
            ),
            premis_file(
                TIFF_UUID, [relationship("derivation", "is source of", PDF_UUID)]
            ),
        ]
    )

    assert check_relationships_type_vocabulary([premis]).failed_items == []
    assert check_relationships_sub_type_vocabulary([premis]).failed_items == []
    assert (
        check_relationships_sub_type_vocabulary_per_object_type([premis]).failed_items
        == []
    )
    assert check_related_objects_inverse_relationship_valid([premis]).failed_items == []


def test_has_source_without_is_source_of_is_rejected():
    premis = premis_with_files(
        [
            premis_file(
                PDF_UUID, [relationship("derivation", "has source", TIFF_UUID)]
            ),
            premis_file(TIFF_UUID, []),
        ]
    )

    result = check_related_objects_inverse_relationship_valid([premis])

    assert [pair.items[0].text for pair in result.failed_items] == ["has source"]


def test_unknown_relationship_sub_type_is_reported_not_raised():
    premis = premis_with_files(
        [
            premis_file(
                PDF_UUID, [relationship("derivation", "is made of", TIFF_UUID)]
            ),
            premis_file(
                TIFF_UUID, [relationship("derivation", "has source", PDF_UUID)]
            ),
        ]
    )

    sub_type_result = check_relationships_sub_type_vocabulary([premis])
    inverse_result = check_related_objects_inverse_relationship_valid([premis])

    assert [r.sub_type.text for r in sub_type_result.failed_items] == ["is made of"]
    assert [pair.items[0].text for pair in inverse_result.failed_items] == [
        "has source"
    ]
