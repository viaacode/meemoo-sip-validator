from typing import Any
from pathlib import Path
from hashlib import md5

from meemoo_sip_validator.v2_1._core import thesauri
from ..models import SIP, premis, Representation
from ..report import Report, Failure, Success, Severity
from ..codes import Code


def get_all_premis_models(sip_path: Path) -> tuple[list[premis.Premis], Report]:
    premis_paths = sip_path.rglob("premis.xml")
    premis_models: list[premis.Premis] = []
    failures: list[Failure | Success] = []
    for path in premis_paths:
        try:
            premis_models.append(premis.Premis.from_xml(path))
        except Exception:
            failures.append(
                Failure(
                    code=Code.xsd_valid,
                    severity=Severity.ERROR,
                    message=f"Unable to parse premis file: {path}",
                    source=str(path),
                )
            )
    return premis_models, Report(results=failures)


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
    convertable_to_object_id: premis.RelatedObjectIdentifier
    | premis.LinkingObjectIdentifier,
):
    return premis.ObjectIdentifier(
        __source__=convertable_to_object_id.__source__,
        type=premis.ObjectIdentifierType(
            __source__=convertable_to_object_id.__source__,
            text=convertable_to_object_id.type.text,
            authority=convertable_to_object_id.type.authority,
            authority_uri=convertable_to_object_id.type.authority_uri,
            value_uri=convertable_to_object_id.type.value_uri,
        ),
        value=premis.ObjectIdentifierValue(
            __source__=convertable_to_object_id.__source__,
            text=convertable_to_object_id.value.text,
        ),
        simple_link=convertable_to_object_id.simple_link,
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
