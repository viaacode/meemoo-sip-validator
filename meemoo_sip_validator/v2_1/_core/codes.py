from typing import Any
from enum import Enum, auto


class CodeEnum(Enum):
    @staticmethod
    def _generate_next_value_(
        name: str, start: int, count: int, last_values: list[Any]
    ) -> str:
        return f"MSIP{count}"


# TODO: assign fixed codes
class Code(str, CodeEnum):
    xsd_valid = auto()
    unique_object_identifiers = auto()
    object_identifier_type_thesauri = auto()
    related_object_identifier_valid = auto()
    relationship_type_thesauri = auto()
    relationship_sub_type_thesauri = auto()
    relationship_sub_type_per_object_thesauri = auto()
    event_type_thesauri = auto()
