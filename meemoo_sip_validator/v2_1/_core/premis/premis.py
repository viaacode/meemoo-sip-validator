from pathlib import Path
from functools import reduce


from .. import thesauri
from ..codes import Code
from . import helpers
from ..report import Report, RuleResult, TupleWithSource
from ..models import premis


def check_object_identifier_type_vocabulary(
    premises: list[premis.Premis],
) -> RuleResult[premis.ObjectIdentifier]:
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


def check_object_identifier_type_uuid_existance(
    premises: list[premis.Premis],
) -> RuleResult[premis.Object]:
    all_object = [object for premis in premises for object in premis.objects]
    objects_without_uuid = [
        object
        for object in all_object
        if "UUID" not in [identifier.type.text for identifier in object.identifiers]
    ]

    def object_id_to_str(object: premis.Object) -> str:
        first_id = next(iter(object.identifiers), None)
        if first_id is None:
            return "<MISSING IDENTIFIERS>"
        return str((first_id.type.text, first_id.value.text))

    return RuleResult(
        code=Code.object_identifier_type_uuid_existance,
        failed_items=objects_without_uuid,
        fail_msg=lambda object: f"Usage of PREMIS object {object_id_to_str(object)} without identifier of type 'UUID'. All objects must have at least one identifier of type 'UUID'.",
        success_msg="Validated existance of identifier with type 'UUID' on all PREMIS objects.",
    )


def check_object_identifiers_uniqueness(
    premises: list[premis.Premis],
) -> RuleResult[premis.ObjectIdentifier]:
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


def check_event_type_vocabulary(
    premises: list[premis.Premis],
) -> RuleResult[premis.Event]:
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


def check_event_identifier_type_is_uuid(
    premises: list[premis.Premis],
) -> RuleResult[premis.EventIdentifier]:
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


def check_event_identifier_uniqueness(
    premises: list[premis.Premis],
) -> RuleResult[premis.EventIdentifier]:
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


def check_event_outcome_vocabulary(
    premises: list[premis.Premis],
) -> RuleResult[premis.Event]:
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


def check_event_linking_agent_identifier_cardinality(
    premises: list[premis.Premis],
) -> RuleResult[premis.Event]:
    all_events = [event for premis in premises for event in premis.events]
    invalid_events = [
        event for event in all_events if len(event.linking_agent_identifiers) == 0
    ]

    return RuleResult(
        code=Code.event_linking_agent_identifier_existance,
        failed_items=invalid_events,
        fail_msg=lambda event: f"Event ({event.identifier.type.text}, {event.identifier.value.text}) is missing a linking agent. At least one linking agent must be present.",
        success_msg="Validated existance of a linking agent on PREMIS events.",
    )


def check_event_linking_object_identifier_cardinality(
    premises: list[premis.Premis],
) -> RuleResult[premis.Event]:
    all_events = [event for premis in premises for event in premis.events]
    invalid_events = [
        event for event in all_events if len(event.linking_object_identifiers) == 0
    ]

    return RuleResult(
        code=Code.event_linking_object_identifier_existance,
        failed_items=invalid_events,
        fail_msg=lambda event: f"Event ({event.identifier.type.text}, {event.identifier.value.text}) is missing a linking object. At least one linking object must be present.",
        success_msg="Validated existance of a linking object on PREMIS events.",
    )


def check_event_linking_agent_role_vocabulary(
    premises: list[premis.Premis],
) -> RuleResult[premis.LinkingAgentIdentifier]:
    all_linking_agent_identifiers = [
        linking_agent_identifier
        for premis in premises
        for event in premis.events
        for linking_agent_identifier in event.linking_agent_identifiers
    ]
    invalid_linking_agent_identifiers = [
        linking_agent_identifier
        for linking_agent_identifier in all_linking_agent_identifiers
        if any(
            role.text not in thesauri.event_agent_roles
            for role in linking_agent_identifier.roles
        )
    ]

    def invalid_roles(agent_id: premis.LinkingAgentIdentifier) -> str:
        roles = [
            role.text
            for role in agent_id.roles
            if role not in thesauri.event_agent_roles
        ]
        return ", ".join(roles)

    return RuleResult(
        code=Code.event_linking_agent_identifier_role_thesauri,
        failed_items=invalid_linking_agent_identifiers,
        fail_msg=lambda agent_id: f"Usage of non-existant linking agent identifier role(s) '{invalid_roles(agent_id)}' on linking agent ({agent_id.type.text}, {agent_id.value.text}). Agent roles must be one of ({', '.join(thesauri.event_agent_roles)})",
        success_msg="Validated PREMIS linking agent identifier role vocabulary.",
    )


def check_event_linking_object_role_vocabulary(
    premises: list[premis.Premis],
) -> RuleResult[premis.LinkingObjectIdentifier]:
    all_linking_object_identifiers = [
        linking_object_identifier
        for premis in premises
        for event in premis.events
        for linking_object_identifier in event.linking_object_identifiers
    ]
    invalid_linking_object_identifiers = [
        linking_object_identifier
        for linking_object_identifier in all_linking_object_identifiers
        if any(
            role.text not in thesauri.event_object_roles
            for role in linking_object_identifier.roles
        )
    ]

    def invalid_roles(object_id: premis.LinkingObjectIdentifier) -> str:
        roles = [
            role.text
            for role in object_id.roles
            if role not in thesauri.event_object_roles
        ]
        return ", ".join(roles)

    return RuleResult(
        code=Code.event_linking_object_identifier_role_thesauri,
        failed_items=invalid_linking_object_identifiers,
        fail_msg=lambda object_id: f"Usage of non-existant linking object identifier role(s) '{invalid_roles(object_id)}' on linking object ({object_id.type.text}, {object_id.value.text}). Object roles must be one of ({', '.join(thesauri.event_object_roles)})",
        success_msg="Validated PREMIS linking object identifier role vocabulary.",
    )


def check_event_has_one_implementer(
    premises: list[premis.Premis],
) -> RuleResult[premis.Event]:
    all_events = [event for premis in premises for event in premis.events]

    def get_implementer_roles(event: premis.Event) -> list[premis.LinkingAgentRole]:
        return [
            role
            for linking_agent_identifier in event.linking_agent_identifiers
            for role in linking_agent_identifier.roles
            if role.text == "implementer"
        ]

    invalid_events = [
        event for event in all_events if len(get_implementer_roles(event)) != 1
    ]

    return RuleResult(
        code=Code.event_implementer_cardinality,
        failed_items=invalid_events,
        fail_msg=lambda event: f"Usage of PREMIS event {event.identifier.type.text, event.identifier.value.text} with zero or more than one implementer agents. All events must have exactly one linking agent identifier with the 'implementer' role.",
        success_msg="Validated presence of implementer for all PREMIS events.",
    )


def check_event_sources_exist(
    premises: list[premis.Premis],
) -> RuleResult[premis.LinkingObjectIdentifier]:
    all_events = [event for premis in premises for event in premis.events]
    source_objects = [
        linking_object_identifier
        for event in all_events
        for linking_object_identifier in event.linking_object_identifiers
        if "source" in [role.text for role in linking_object_identifier.roles]
    ]
    all_object_identifiers = helpers.get_all_object_identifiers(premises)

    def is_outcome(linking_obj: premis.LinkingObjectIdentifier) -> bool:
        return "outcome" in [role.text for role in linking_obj.roles]

    def object_id_exists(linking_obj: premis.LinkingObjectIdentifier) -> bool:
        return helpers.to_identifier(linking_obj) not in all_object_identifiers

    all_temporary_created_object_ids = [
        helpers.to_identifier(linking_object_identifier)
        for event in all_events
        for linking_object_identifier in event.linking_object_identifiers
        if is_outcome(linking_object_identifier)
        and object_id_exists(linking_object_identifier)
    ]
    all_objects_including_temporary = (
        all_temporary_created_object_ids + all_object_identifiers
    )

    invalid_source_objects = [
        source
        for source in source_objects
        if helpers.to_identifier(source) not in all_objects_including_temporary
    ]

    return RuleResult(
        code=Code.event_source_exists,
        failed_items=invalid_source_objects,
        fail_msg=lambda linking_obj: f"Usage of PREMIS event linking object identifier {linking_obj.type.text, linking_obj.value.text} with role 'source', but no object or event outcome object with that identifier was found.",
        success_msg="Validated existance of source object for all PREMIS events.",
    )


def check_related_objects_identifier_uses_existing_object(
    premises: list[premis.Premis],
) -> RuleResult[premis.RelatedObjectIdentifier]:
    # TODO: is it possible to have a relationship to a "temporary" object created by an event?
    all_related_identifiers = [
        related_object_identifier
        for premis in premises
        for object in premis.objects
        for relationship in object.relationships
        for related_object_identifier in relationship.related_object_identifiers
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


def check_related_objects_inverse_relationship_valid(
    premises: list[premis.Premis],
) -> RuleResult[
    TupleWithSource[premis.RelationshipSubType, premis.RelatedObjectIdentifier]
]:
    all_relationship_sub_type_and_rel_object_id_pairs = (
        (relationship.sub_type, related_object_identifier, object)
        for premis in premises
        for object in premis.objects
        for relationship in object.relationships
        for related_object_identifier in relationship.related_object_identifiers
    )
    all_objects = [object for premis in premises for object in premis.objects]

    invalid_items: list[
        TupleWithSource[premis.RelationshipSubType, premis.RelatedObjectIdentifier]
    ] = []
    for (
        sub_type,
        rel_obj_id,
        self_object,
    ) in all_relationship_sub_type_and_rel_object_id_pairs:
        related_object = helpers.find_related_object(rel_obj_id, all_objects)
        if related_object is None:
            # could not determine related object
            continue

        relationships_pointing_to_self = [
            relationship
            for relationship in related_object.relationships
            for related_object_identifier in relationship.related_object_identifiers
            if helpers.to_identifier(related_object_identifier)
            in self_object.identifiers
        ]
        inverse_found = any(
            helpers.get_inverse_relationship(relationship.sub_type) == sub_type.text
            for relationship in relationships_pointing_to_self
        )
        if not inverse_found:
            invalid_items.append(
                TupleWithSource(
                    __source__=sub_type.__source__,
                    items=(sub_type, rel_obj_id),
                )
            )

    return RuleResult(
        code=Code.related_object_inverse_valid,
        failed_items=invalid_items,
        fail_msg=lambda pair: f"Could not find inverse relationship for PREMIS related object identifier {pair.items[1].type.text, pair.items[1].value.text} with relationship sub-type '{pair.items[0].text}'.",
        success_msg="Validated inverse sub-types of PREMIS related object identifiers.",
    )


def check_relationships_type_vocabulary(
    premises: list[premis.Premis],
) -> RuleResult[premis.Relationship]:
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


def check_relationships_sub_type_vocabulary(
    premises: list[premis.Premis],
) -> RuleResult[premis.Relationship]:
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


def check_relationships_sub_type_vocabulary_per_object_type(
    premises: list[premis.Premis],
) -> RuleResult[premis.Relationship]:
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


def check_agent_identifier_type_uuid_existance(
    premises: list[premis.Premis],
) -> RuleResult[premis.Agent]:
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


def check_agent_identifier_uniqueness(
    premises: list[premis.Premis],
) -> RuleResult[premis.AgentIdentifier]:
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


def check_agent_type_vocabulary(
    premises: list[premis.Premis],
) -> RuleResult[premis.Agent]:
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


def check_fixity_message_digest_algorithm_vocabulary(
    premises: list[premis.Premis],
) -> RuleResult[premis.File]:
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

    return RuleResult(
        code=Code.fixity_message_digest_algorithm_thesauri,
        failed_items=invalid_files,
        fail_msg=lambda file: f"Usage of non-supported message digest algorithm(s) in PREMIS file '{helpers.get_object_id(file)}'. PREMIS message digest algorithm must be one of ({','.join(thesauri.supported_hashes)}).",
        success_msg="Validated supported PREMIS fixity message digest algorithm.",
    )


def check_file_orignal_name_present(
    premises: list[premis.Premis],
) -> RuleResult[premis.File]:
    files = [
        file
        for premis in premises
        for file in premis.objects
        if file.xsi_type == "{http://www.loc.gov/premis/v3}file"
    ]
    invalid_files = [file for file in files if file.original_name is None]

    return RuleResult(
        code=Code.file_original_name_present,
        failed_items=invalid_files,
        fail_msg=lambda file: f"Usage of PREMIS file {helpers.get_object_id(file)} with missing original name. All files must have an orignal name element.",
        success_msg="Validated presense of orignal name on PREMIS file.",
    )


def check_file_fixity_present(premises: list[premis.Premis]) -> RuleResult[premis.File]:
    files = [
        file
        for premis in premises
        for file in premis.objects
        if file.xsi_type == "{http://www.loc.gov/premis/v3}file"
    ]
    invalid_files = [file for file in files if helpers.get_file_fixity(file) is None]

    return RuleResult(
        code=Code.file_fixity_present,
        failed_items=invalid_files,
        fail_msg=lambda file: f"Usage of PREMIS file {helpers.get_object_id(file)} with missing fixity. All files must have a fixity element.",
        success_msg="Validated presense of orignal name on PREMIS file.",
    )


def check_file_references_existing_data(
    premises: list[premis.Premis],
) -> RuleResult[premis.File]:
    files = [
        file
        for premis in premises
        for file in premis.objects
        if file.xsi_type == "{http://www.loc.gov/premis/v3}file"
    ]
    data_paths = [helpers.get_data_path_for_file(file) for file in files]
    invalid_files: list[premis.File] = []
    for file, data_path in zip(files, data_paths):
        if file.original_name is None:
            continue  # Checked by other rule

        if data_path is None:
            continue  # checked by other rule: data_path is None if the original name is None

        if not data_path.exists():
            invalid_files.append(file)

    return RuleResult(
        code=Code.file_is_mappable_to_data,
        failed_items=invalid_files,
        fail_msg=lambda file: f"Could not find data '{helpers.get_data_path_for_file(file)}' referenced by PREMIS file {helpers.get_object_id(file)}.",
        success_msg="Validated reference from PREMIS files to data.",
    )


def check_fixity_message_digest_matches_actual_hash(
    premises: list[premis.Premis],
) -> RuleResult[premis.File]:
    files = [
        file
        for premis in premises
        for file in premis.objects
        if file.xsi_type == "{http://www.loc.gov/premis/v3}file"
    ]
    data_paths = [helpers.get_data_path_for_file(file) for file in files]

    invalid_files: list[premis.File] = []
    for file, data_path in zip(files, data_paths):
        if data_path is None:
            continue  # checked by other rule
        if not data_path.exists():
            continue  # checked by other rule
        calculated_digest = helpers.calculate_message_digest(data_path)
        fixity = helpers.get_file_fixity(file)
        if fixity is None:
            continue  # checked by other rule
        if fixity != calculated_digest:
            invalid_files.append(file)

    return RuleResult(
        code=Code.fixity_message_digest_matches_actual,
        failed_items=invalid_files,
        fail_msg=lambda file: f"Incorrect message digest for PREMIS file {helpers.get_object_id(file)}.",
        success_msg="Validated PREMIS file message digest values.",
    )


checks = [
    check_object_identifier_type_vocabulary,
    check_object_identifiers_uniqueness,
    check_object_identifier_type_uuid_existance,
    check_related_objects_identifier_uses_existing_object,
    check_related_objects_inverse_relationship_valid,
    check_relationships_type_vocabulary,
    check_relationships_sub_type_vocabulary,
    check_relationships_sub_type_vocabulary_per_object_type,
    check_event_type_vocabulary,
    check_event_identifier_type_is_uuid,
    check_event_identifier_uniqueness,
    check_event_outcome_vocabulary,
    check_event_linking_agent_role_vocabulary,
    check_event_linking_object_role_vocabulary,
    check_event_has_one_implementer,
    check_event_linking_agent_identifier_cardinality,
    check_event_linking_object_identifier_cardinality,
    check_event_sources_exist,
    check_agent_identifier_uniqueness,
    check_agent_identifier_type_uuid_existance,
    check_agent_type_vocabulary,
    check_fixity_message_digest_algorithm_vocabulary,
    check_fixity_message_digest_matches_actual_hash,
    check_file_orignal_name_present,
    check_file_fixity_present,
    check_file_references_existing_data,
]


def validate_premis(sip_path: Path) -> Report:
    premises, failed_parse_report = helpers.get_all_premis_models(sip_path)
    rule_results = (check(premises) for check in checks)
    reports = (rule.to_report() for rule in rule_results)
    combined_report = reduce(Report.__add__, reports)

    return failed_parse_report + combined_report
