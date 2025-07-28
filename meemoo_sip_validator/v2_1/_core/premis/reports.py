from typing import Callable
from functools import reduce


from .. import thesauri
from ..codes import Code
from . import helpers
from ..models import SIP, Report, premis, RuleResult


def check_object_identifier_types(sip: SIP) -> RuleResult[premis.ObjectIdentifier]:
    premises = helpers.get_all_premis_models(sip)
    all_object_identifiers = helpers.get_all_object_identifiers(premises)
    invalid_identifiers = [
        identifier
        for identifier in all_object_identifiers
        if identifier.type.text not in thesauri.object_identifier_types
    ]
    return RuleResult(
        code=Code.object_identifier_type_thesauri,
        failed_items=invalid_identifiers,
        fail_msg=lambda id: f"Usage of invalid PREMIS object identifier type: '{id.type.text}'",
        success_msg="Validated PREMIS object identifier types.",
    )


def check_object_identifiers_uniqueness(
    sip: SIP,
) -> RuleResult[premis.ObjectIdentifier]:
    premises = helpers.get_all_premis_models(sip)
    all_object_identifiers = helpers.get_all_object_identifiers(premises)
    duplicate_identifiers = [
        identifier
        for identifier in all_object_identifiers
        if len([_id for _id in all_object_identifiers if _id == identifier]) != 1
    ]

    return RuleResult(
        code=Code.unique_object_identifiers,
        failed_items=duplicate_identifiers,
        fail_msg=lambda id: f"Usage of non-unique PREMIS object identifier: {id}.",
        success_msg="PREMIS object identifier uniqueness validated.",
    )


def check_event_types(sip: SIP) -> RuleResult[premis.Event]:
    premises = helpers.get_all_premis_models(sip)
    all_events = [event for premis in premises for event in premis.events]
    invalid_events = [
        event for event in all_events if event.type.text not in thesauri.event_types
    ]

    return RuleResult(
        code=Code.event_type_thesauri,
        failed_items=invalid_events,
        fail_msg=lambda event: f"Usage of non-existant event type '{event.type.text}' on event '{event.identifier.value}'. PREMIS event type must be one of ({', '.join(thesauri.event_types)})",
        success_msg="Validated PREMIS Event types",
    )


def check_related_objects_identifier(
    sip: SIP,
) -> RuleResult[premis.RelatedObjectIdentifier]:
    premises = helpers.get_all_premis_models(sip)
    # TODO: is it possible to have a relationship to a "temporary" object created by an event?
    all_related_identifiers = [
        related_object_identifier
        for premis in premises
        for object in premis.objects
        for relationship in object.relationships
        for related_object_identifier in relationship.related_object_identifier
    ]
    all_object_identifiers = [
        object for object in helpers.get_all_object_identifiers(premises)
    ]
    non_existant_object_identifiers = [
        related_identifier
        for related_identifier in all_related_identifiers
        if helpers.to_identifier(related_identifier) not in all_object_identifiers
    ]

    return RuleResult(
        code=Code.related_object_identifier_valid,
        failed_items=non_existant_object_identifiers,
        fail_msg=lambda id: f"Usage of PREMIS related object identifier with invalid identifier {id}.",
        success_msg="Existance of PREMIS objects used as related objects validated.",
    )


def check_relationships_type(sip: SIP) -> RuleResult[premis.Relationship]:
    premises = helpers.get_all_premis_models(sip)
    all_relationships = [
        relationship
        for premis in premises
        for object in premis.objects
        for relationship in object.relationships
    ]
    invalid_relationships = [
        relationship
        for relationship in all_relationships
        if relationship.type.text not in thesauri.relationship_types
    ]

    return RuleResult(
        code=Code.relationship_type_thesauri,
        failed_items=invalid_relationships,
        fail_msg=lambda relationship: f"Usage of non-existant relationship type '{relationship.type.text}'. PREMIS  type must be one of ({', '.join(thesauri.relationship_types)}).",
        success_msg="PREMIS relationship types vocabulary validated.",
    )


def check_relationships_sub_type(sip: SIP) -> RuleResult[premis.Relationship]:
    premises = helpers.get_all_premis_models(sip)
    all_relationships = [
        relationship
        for premis in premises
        for object in premis.objects
        for relationship in object.relationships
    ]
    invalid_relationships = [
        relationship
        for relationship in all_relationships
        if relationship.sub_type.text not in thesauri.relationship_sub_types
    ]

    return RuleResult(
        code=Code.relationship_sub_type_thesauri,
        failed_items=invalid_relationships,
        fail_msg=lambda relationship: f"Usage of non-existant relationship sub-type '{relationship.sub_type.text}'. PREMIS relationship sub-type must be one of ({', '.join(thesauri.relationship_sub_types)}).",
        success_msg="PREMIS relationship sub-types vocabulary validated.",
    )


def check_relationships_sub_type_per_object_type(
    sip: SIP,
) -> RuleResult[premis.Relationship]:
    premises = helpers.get_all_premis_models(sip)
    object_and_relationhip_pairs = [
        (object, relationship)
        for premis in premises
        for object in premis.objects
        for relationship in object.relationships
    ]
    invalid_relationships = [
        relationship
        for object, relationship in object_and_relationhip_pairs
        if relationship.sub_type.text
        not in thesauri.relationship_sub_types_per_object_type[object.xsi_type]
    ]

    return RuleResult(
        code=Code.relationship_sub_type_per_object_thesauri,
        failed_items=invalid_relationships,
        fail_msg=lambda relationship: f"Usage of relationship sub-type '{relationship.sub_type.text}' on object with incorrect xsi:type.",
        success_msg="PREMIS relationship sub-types vocabulary per object type validated.",
    )


checks: list[Callable[[SIP], RuleResult]] = [
    check_object_identifier_types,
    check_object_identifiers_uniqueness,
    check_related_objects_identifier,
    check_relationships_type,
    check_relationships_sub_type,
    check_relationships_sub_type_per_object_type,
    check_event_types,
]


def validate(sip: SIP) -> Report:
    rule_results = (check(sip) for check in checks)
    reports = (rule.to_report() for rule in rule_results)
    return reduce(Report.__add__, reports)
