# pyright: reportExplicitAny=false

from typing import Any
from ..models import SIP, premis


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
