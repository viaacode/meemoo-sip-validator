# pyright: reportExplicitAny=false

from typing import Any
from pathlib import Path
from hashlib import md5

from meemoo_sip_validator.v2_1._core import thesauri
from ..models import SIP, premis, Representation


def get_all_premis_models(sip: SIP[Any]) -> list[premis.Premis]:
    return [sip.metadata.preservation] + [
        r.metadata.preservation for r in sip.representations
    ]


def get_all_object_identifiers(
    premises: list[premis.Premis],
) -> list[premis.ObjectIdentifier]:
    return [
        identifier
        for premis in premises
        for object in premis.objects
        for identifier in object.identifiers
    ]


def unique[T](items: list[T]) -> list[T]:
    result: list[T] = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


def to_identifier(
    related_object_identifier: premis.RelatedObjectIdentifier,
):
    return premis.ObjectIdentifier(
        __source__=related_object_identifier.__source__,
        type=premis.ObjectIdentifierType(
            __source__=related_object_identifier.__source__,
            text=related_object_identifier.type.text,
            authority=related_object_identifier.type.authority,
            authority_uri=related_object_identifier.type.authority_uri,
            value_uri=related_object_identifier.type.value_uri,
        ),
        value=premis.ObjectIdentifierValue(
            __source__=related_object_identifier.__source__,
            text=related_object_identifier.value.text,
        ),
        simple_link=related_object_identifier.simple_link,
    )


def find_related_object(
    related_object_identifier: premis.RelatedObjectIdentifier,
    all_objects: list[premis.Object],
) -> premis.Object | None:
    related_identifier = to_identifier(related_object_identifier)
    objects = [
        object for object in all_objects if related_identifier in object.identifiers
    ]
    if len(objects) != 1:
        return None
    return objects[0]


def get_inverse_relationship(sub_type: premis.RelationshipSubType) -> str:
    return thesauri.inverse_relationship_sub_type_map[sub_type.text]


def get_file_and_representation_pairs(
    sip: SIP[Any],
) -> list[tuple[premis.File, Representation[Any]]]:
    return [
        (object, representation)
        for representation in sip.representations
        for object in representation.metadata.preservation.objects
        if object.xsi_type == "{http://www.loc.gov/premis/v3}file"
    ]


def get_file_and_data_pairs(sip: SIP[Any]) -> list[tuple[premis.File, Path]]:
    pairs = get_file_and_representation_pairs(sip)
    files_and_data: list[tuple[premis.File, Path]] = []
    for file, representation in pairs:
        if file.original_name is None:
            continue  # already checked by other rule
        file_data_matches = (
            path for path in representation.data if path.name == file.original_name.text
        )
        data_path = next(file_data_matches, None)
        if data_path is None:
            continue  # already check by other rule
        files_and_data.append((file, data_path))
    return files_and_data


def calculate_message_digest(path: Path) -> str:
    with open(path, "rb") as f:
        contents = f.read()
    return md5(contents).hexdigest()


def get_object_id(file: premis.File) -> str:
    if len(file.identifiers) == 0:
        return "(without identifiers)"

    uuid = next((id for id in file.identifiers if id.type.text == "UUID"), None)
    if uuid is not None:
        return str((uuid.type.text, uuid.value.text))

    id = next(iter(file.identifiers))
    return str((id.type.text, id.value.text))
