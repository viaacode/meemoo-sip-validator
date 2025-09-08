from typing import Any, override
from enum import Enum, auto


class CodeEnum(Enum):
    @override
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> str:
        return f"MSIP{count}"


# TODO: assign fixed codes
class Code(str, CodeEnum):
    structure_valid = auto()
    xsd_valid = auto()
    edtf_valid = auto()
    license_thesauri = auto()
    mets_other_content_information_type = auto()
    object_identifiers_uniqueness = auto()
    object_identifier_type_uuid_existance = auto()
    object_identifier_type_thesauri = auto()
    file_original_name_present = auto()
    file_fixity_present = auto()
    file_is_mappable_to_data = auto()
    fixity_message_digest_algorithm_thesauri = auto()
    fixity_message_digest_matches_actual = auto()
    related_object_identifier_valid = auto()
    related_object_inverse_valid = auto()
    relationship_type_thesauri = auto()
    relationship_sub_type_thesauri = auto()
    relationship_sub_type_per_object_thesauri = auto()
    event_type_thesauri = auto()
    event_identifier_type_is_uuid = auto()
    event_identifier_uniqueness = auto()
    event_outcome_thesauri = auto()
    event_implementer_cardinality = auto()
    event_linking_agent_identifier_role_thesauri = auto()
    event_linking_agent_identifier_existance = auto()
    event_linking_object_identifier_existance = auto()
    event_linking_object_identifier_role_thesauri = auto()
    event_source_exists = auto()
    agent_identifier_uniqueness = auto()
    agent_identifier_type_uuid_existance = auto()
    agent_type_thesauri = auto()
