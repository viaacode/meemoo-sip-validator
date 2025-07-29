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
        code=Code.object_identifiers_uniqueness,
        failed_items=duplicate_identifiers,
        fail_msg=lambda identifier: f"Usage of duplicate PREMIS object identifier: ({identifier.type.text}, {identifier.value.text}).",
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
        fail_msg=lambda event: f"Usage of non-existant event type '{event.type.text}' on event '{event.identifier.value.text}'. PREMIS event type must be one of ({', '.join(thesauri.event_types)})",
        success_msg="Validated PREMIS event type vocabulary.",
    )


def check_event_identifier_type_is_uuid(sip: SIP) -> RuleResult[premis.EventIdentifier]:
    premises = helpers.get_all_premis_models(sip)
    all_events_identifiers = [
        event.identifier for premis in premises for event in premis.events
    ]
    invalid_event_identifiers = [
        identifier
        for identifier in all_events_identifiers
        if identifier.type.text != "UUID"
    ]

    return RuleResult(
        code=Code.event_identifier_type_is_uuid,
        failed_items=invalid_event_identifiers,
        fail_msg=lambda identifier: f"Usage of PREMIS event {identifier.type.text, identifier.value.text} with invalid type '{identifier.type.text}'. All event identifiers must have at type 'UUID'.",
        success_msg="Validated event identifier type.",
    )


def check_event_identifier_uniqueness(sip: SIP) -> RuleResult[premis.EventIdentifier]:
    premises = helpers.get_all_premis_models(sip)
    all_events_identifiers = [
        event.identifier for premis in premises for event in premis.events
    ]
    duplicate_identifiers = [
        identifier
        for identifier in all_events_identifiers
        if len([_id for _id in all_events_identifiers if _id == identifier]) != 1
    ]

    return RuleResult(
        code=Code.event_identifier_uniqueness,
        failed_items=duplicate_identifiers,
        fail_msg=lambda identifier: f"Usage of duplicate event identifier ({identifier.type.text}, {identifier.value.text}). PREMIS event identifiers must be unique.",
        success_msg="Validated PREMIS event identifier uniqueness.",
    )


def check_event_outcome(sip: SIP) -> RuleResult[premis.Event]:
    premises = helpers.get_all_premis_models(sip)
    all_events = [event for premis in premises for event in premis.events]
    invalid_events = [
        event
        for event in all_events
        for outcome_information in event.outcome_information
        if outcome_information.outcome is None
        or outcome_information.outcome.text not in thesauri.event_outcomes
    ]

    def invalid_outcomes(event: premis.Event) -> str:
        outcomes = [
            outcome_information.outcome
            for outcome_information in event.outcome_information
            if outcome_information.outcome not in thesauri.event_outcomes
        ]
        return ",".join(
            [outcome.text if outcome else "<MISSING>" for outcome in outcomes]
        )

    return RuleResult(
        code=Code.event_outcome_thesauri,
        failed_items=invalid_events,
        fail_msg=lambda event: f"Usage of non-existant event outcome(s) '{invalid_outcomes(event)}' on event ({event.identifier.type.text}, {event.identifier.value.text}). Outcome must be one of ({','.join(thesauri.event_outcomes)})",
        success_msg="Validated PREMIS event outcome vocabulary.",
    )


def check_event_linking_agent_cardinality(sip: SIP) -> RuleResult[premis.Event]:
    premises = helpers.get_all_premis_models(sip)
    all_events = [event for premis in premises for event in premis.events]
    invalid_events = [
        event for event in all_events if len(event.linking_agent_identifiers) == 0
    ]

    return RuleResult(
        code=Code.event_linking_agent_existance,
        failed_items=invalid_events,
        fail_msg=lambda event: f"Event ({event.identifier.type.text}, {event.identifier.value.text}) is missing a linking agent. At least one linking agent must be present.",
        success_msg="Validated existance of a linking agent on PREMIS events.",
    )


def check_event_linking_object_cardinality(sip: SIP) -> RuleResult[premis.Event]:
    premises = helpers.get_all_premis_models(sip)
    all_events = [event for premis in premises for event in premis.events]
    invalid_events = [
        event for event in all_events if len(event.linking_object_identifiers) == 0
    ]

    return RuleResult(
        code=Code.event_linking_object_existance,
        failed_items=invalid_events,
        fail_msg=lambda event: f"Event ({event.identifier.type.text}, {event.identifier.value.text}) is missing a linking object. At least one linking object must be present.",
        success_msg="Validated existance of a linking object on PREMIS events.",
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
        fail_msg=lambda identifier: f"Usage of PREMIS related object identifier with non-existant identifier ({identifier.type.text}, {identifier.value.text}).",
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


def check_agent_identifier_type_uuid_existance(sip: SIP) -> RuleResult[premis.Agent]:
    premises = helpers.get_all_premis_models(sip)
    all_agent = [agent for premis in premises for agent in premis.agents]
    agents_without_uuid = [
        agent
        for agent in all_agent
        if "UUID" not in [identifier.type.text for identifier in agent.identifiers]
    ]

    def agent_id_to_str(agent: premis.Agent) -> str:
        first_id = next(iter(agent.identifiers), None)
        if first_id is None:
            return "<MISSING IDENTIFIERS>"
        return str((first_id.type.text, first_id.value.text))

    return RuleResult(
        code=Code.agent_identifier_type_uuid_existance,
        failed_items=agents_without_uuid,
        fail_msg=lambda agent: f"Usage of PREMIS agent {agent_id_to_str(agent)} without identifier of type 'UUID'. All agents must have at least one identifier of type 'UUID'.",
        success_msg="Validated existance of identifier with type 'UUID' on all PREMIS agents.",
    )


def check_agent_identifier_uniqueness(sip: SIP) -> RuleResult[premis.AgentIdentifier]:
    premises = helpers.get_all_premis_models(sip)
    all_agent_identifiers = [
        identifier
        for premis in premises
        for agent in premis.agents
        for identifier in agent.identifiers
    ]
    duplicate_identifiers = [
        identifier
        for identifier in all_agent_identifiers
        if len([_id for _id in all_agent_identifiers if _id == identifier]) != 1
    ]

    return RuleResult(
        code=Code.agent_identifier_uniqueness,
        failed_items=duplicate_identifiers,
        fail_msg=lambda identifier: f"Usage of duplicate agent identifier ({identifier.type.text}, {identifier.value.text}). PREMIS agent identifiers must be unique.",
        success_msg="Validated PREMIS agent identifier uniqueness.",
    )


def check_agent_type(sip: SIP) -> RuleResult[premis.Agent]:
    premises = helpers.get_all_premis_models(sip)
    all_agents = [agent for premis in premises for agent in premis.agents]
    invalid_agents = [
        agent for agent in all_agents if agent.type.text not in thesauri.agent_types
    ]

    return RuleResult(
        code=Code.agent_type_thesauri,
        failed_items=invalid_agents,
        fail_msg=lambda agent: f"Usage of non-existant agent type '{agent.type.text}'. PREMIS agent type must be one of ({','.join(thesauri.agent_types)}).",
        success_msg="Validated PREMIS agent type vocabulary.",
    )


def check_fixity_message_digest_algorithm(sip: SIP) -> RuleResult[premis.File]:
    premises = helpers.get_all_premis_models(sip)
    all_files = [
        object
        for premis in premises
        for object in premis.objects
        if object.xsi_type == "{http://www.loc.gov/premis/v3}file"
    ]
    invalid_files = [
        file
        for file in all_files
        for characteristics in file.characteristics
        for fixity in characteristics.fixity
        if fixity.message_digest_algorithm.text not in thesauri.supported_hashes
    ]

    def get_unsupported_algorithms(file: premis.File) -> str:
        algorithms = [
            fixity.message_digest_algorithm
            for characteristics in file.characteristics
            for fixity in characteristics.fixity
        ]
        return ",".join(
            algorithm.text
            for algorithm in algorithms
            if algorithm.text not in thesauri.supported_hashes
        )

    return RuleResult(
        code=Code.fixity_message_digest_algorithm,
        failed_items=invalid_files,
        fail_msg=lambda file: f"Usage of non-supported message digest algorithm(s) '{get_unsupported_algorithms(file)}'. PREMIS message digest algorithm must be one of ({','.join(thesauri.supported_hashes)}).",
        success_msg="Validated supported PREMIS fixity message digest algorithm.",
    )


checks: list[Callable[[SIP], RuleResult]] = [
    check_object_identifier_types,
    check_object_identifiers_uniqueness,
    check_related_objects_identifier,
    check_relationships_type,
    check_relationships_sub_type,
    check_relationships_sub_type_per_object_type,
    check_event_types,
    check_event_identifier_type_is_uuid,
    check_event_identifier_uniqueness,
    check_event_outcome,
    check_event_linking_agent_cardinality,
    check_event_linking_object_cardinality,
    check_agent_identifier_uniqueness,
    check_agent_identifier_type_uuid_existance,
    check_agent_type,
    check_fixity_message_digest_algorithm,
]


def validate(sip: SIP) -> Report:
    rule_results = (check(sip) for check in checks)
    reports = (rule.to_report() for rule in rule_results)
    return reduce(Report.__add__, reports)
