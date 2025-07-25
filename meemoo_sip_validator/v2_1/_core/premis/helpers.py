from typing import Any
from collections import namedtuple

from ..models import SIP, Premis, premis, Error, Severity
from ..codes import Code


def get_all_premis_models(sip: SIP) -> list[Premis]:
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


def unique(items: list[Any]) -> list[Any]:
    result = []
    for item in items:
        if item not in result:
            result.append(item)
    return result


ObjectIdentifierTuple = namedtuple(
    "ObjectIdentifierTuple",
    [
        "type",
        "type_authority",
        "type_authority_uri",
        "type_value_uri",
        "value",
        "simple_link",
    ],
)


def convert_to_tuple(
    object_identifier: premis.ObjectIdentifier | premis.RelatedObjectIdentifier,
) -> ObjectIdentifierTuple:
    return ObjectIdentifierTuple(
        object_identifier.type.text,
        object_identifier.type.authority,
        object_identifier.type.authority_uri,
        object_identifier.type.value_uri,
        object_identifier.value.text,
        object_identifier.simple_link,
    )
