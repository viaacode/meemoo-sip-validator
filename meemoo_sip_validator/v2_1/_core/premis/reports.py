from typing import Callable
from functools import reduce


from .. import thesauri
from ..codes import Code
from . import helpers
from ..models import SIP, Report, Error, Severity, Success


def report_unique_object_identifiers(sip: SIP) -> Report:
    premises = helpers.get_all_premis_models(sip)
    all_object_identifiers = helpers.get_all_object_identifiers(premises)

    code = Code.unique_object_identifiers
    if len(helpers.unique(all_object_identifiers)) != len(all_object_identifiers):
        message = "PREMIS object identifiers must be unique over all premis.xml files in the SIP."
        result = Error(code=code, message=message, severity=Severity.ERROR)
    else:
        message = "PREMIS object identifiers are unique."
        result = Success(code=code, message=message)

    return Report(results=[result])


def report_valid_event_types(sip: SIP) -> Report:
    premises = helpers.get_all_premis_models(sip)
    all_events = [event for premis in premises for event in premis.events]

    errors: list[Error | Success] = []
    for event in all_events:
        if event.type.text not in thesauri.event_types:
            error = Error(
                code=Code.event_types_thesauri,
                message=f"Usage of non-existant event type '{event.type.text}' on event '{event.identifier.value}'. PREMIS event type must be one of ({', '.join(thesauri.event_types)})",
                severity=Severity.ERROR,
            )
            errors.append(error)

    if len(errors) != 0:
        return Report(results=errors)

    return Report(
        results=[
            Success(
                code=Code.event_types_thesauri,
                message=f"Validated PREMIS Event types",
            )
        ]
    )


def report_related_objects_valid(sip: SIP) -> Report:
    premises = helpers.get_all_premis_models(sip)
    # TODO: is it possible to have a relationship to a "temporary" object created by an event?
    all_related_identifiers = {
        helpers.convert_to_tuple(related_object_identifier)
        for premis in premises
        for object in premis.objects
        for relationship in object.relationships
        for related_object_identifier in relationship.related_object_identifier
    }
    all_object_identifiers = {
        helpers.convert_to_tuple(object)
        for object in helpers.get_all_object_identifiers(premises)
    }

    non_existant_object_identifiers = all_related_identifiers - all_object_identifiers

    errors: list[Error | Success] = []
    for identifier in non_existant_object_identifiers:
        error = Error(
            code=Code.related_object_identifier_valid,
            message=f"Usage of PREMIS related object identifier with invalid identifier {identifier}",
            severity=Severity.ERROR,
        )
        errors.append(error)

    if len(non_existant_object_identifiers) != 0:
        return Report(results=errors)

    return Report(
        results=[
            Success(
                code=Code.related_object_identifier_valid,
                message="Existance of PREMIS objects related to relationships validated",
            )
        ]
    )


def report_relationships_type(sip: SIP) -> Report:
    premises = helpers.get_all_premis_models(sip)
    all_relationships = [
        relationship
        for premis in premises
        for object in premis.objects
        for relationship in object.relationships
    ]

    errors: list[Error | Success] = []
    for relationship in all_relationships:
        if relationship.type.text not in thesauri.relationship_types:
            error = Error(
                code=Code.event_types_thesauri,
                message=f"Usage of non-existant relationship type '{relationship.type.text}'. PREMIS  type must be one of ({', '.join(thesauri.event_types)})",
                severity=Severity.ERROR,
            )
            errors.append(error)

    return Report(
        results=[
            Success(
                code=Code.event_types_thesauri,
                message="PREMIS relationship types validated",
            )
        ]
    )


checks: list[Callable[[SIP], Report]] = [
    report_unique_object_identifiers,
    report_valid_event_types,
    report_related_objects_valid,
    report_relationships_type,
]


def validate(sip: SIP) -> Report:
    reports = (check(sip) for check in checks)
    return reduce(Report.__add__, reports)
