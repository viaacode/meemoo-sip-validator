from enum import Enum


class Code(str, Enum):
    unique_object_identifiers = "MSIP1"
    event_types_thesauri = "MSIP2"
    related_object_identifier_valid = "MSIP3"
    relationship_types_thesauri = "MSIP4"
    relationship_sub_type_thesauri = "MSIP5"
    xsd_valid = "MSIP6"
