from pathlib import Path
from hashlib import md5

from meemoo_sip_validator.v2_1._core import thesauri
from ..models import premis
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


def get_data_path_for_file(file: premis.File) -> Path | None:
    # The implementation of this function is quite naive.
    # It assumes that the structual constraints are checked.
    premis_path = Path(file.__source__)
    original_name = file.original_name
    if original_name is None:
        return None
    preservation_path = premis_path.parent
    metadata_path = preservation_path.parent
    representation_path = metadata_path.parent
    return representation_path / "data" / original_name.text


def calculate_message_digest(path: Path) -> str:
    hash = md5()
    with open(path, "rb") as f:
        while chunk := f.read(1024 * 2014):  # 1MB
            hash.update(chunk)
    return hash.hexdigest()


def get_object_id(file: premis.File) -> str:
    if len(file.identifiers) == 0:
        return "(without identifiers)"

    uuid = next((id for id in file.identifiers if id.type.text == "UUID"), None)
    if uuid is not None:
        return str((uuid.type.text, uuid.value.text))

    id = next(iter(file.identifiers))
    return str((id.type.text, id.value.text))


def get_file_fixity(file: premis.File) -> str | None:
    fixities = [
        fixity
        for characteristics in file.characteristics
        for fixity in characteristics.fixity
        if fixity.message_digest_algorithm.text in thesauri.supported_hashes
    ]
    if len(fixities) != 1:
        return None

    return fixities[0].message_digest.text
