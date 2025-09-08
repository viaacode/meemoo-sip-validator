event_types = [
    "baking",
    "calibration",
    "check-in",
    "check-out",
    "cleaning",
    "compression",
    "decompression",
    "editing",
    "format-identification",
    "ingest",
    "inspection",
    "registration",
    "transcoding",
    "transcription",
    "transfer",
    "transform",
    "digital-transfer",
    "digitization",
    "quality-control",
    "repair",
    "validation",
    "migration",
    "creation",
]

event_outcomes = [
    "fail",
    "success",
    "warning",
]

event_agent_roles = [
    "authorizer",
    "executing program",
    "implementer",
    "validator",
    "instrument",
]

event_object_roles = [
    "source",
    "outcome",
]

relationship_types = [
    "structural",
]

relationship_sub_types_per_object_type = {
    "{http://www.loc.gov/premis/v3}intellectualEntity": [
        "is represented by",
        "has master copy",
        "has mezzanine copy",
        "has access copy",
        "has transcription copy",
        "has carrier copy",
    ],
    "{http://www.loc.gov/premis/v3}representation": [
        "represents",
        "is master copy of",
        "is mezzanine copy of",
        "is access copy of",
        "is transcription copy of",
        "is carrier copy of",
        "includes",
    ],
    "{http://www.loc.gov/premis/v3}file": [
        "is included in",
    ],
    "{http://www.loc.gov/premis/v3}bitstream": [],
}

inverse_relationship_sub_type_map = {
    "represents": "is represented by",
    "is represented by": "represents",
    "has master copy": "is master copy of",
    "is master copy of": "has master copy",
    "has mezzanine copy": "is mezzanine copy of",
    "is mezzanine copy of": "has mezzanine copy",
    "has access copy": "is access copy of",
    "is access copy of": "has access copy",
    "has transcription copy": "is transcription copy of",
    "is transcription copy of": "has transcription copy",
    "has carrier copy": "is carrier copy of",
    "is carrier copy of": "has carrier copy",
    "includes": "is included in",
    "is included in": "includes",
}


relationship_sub_types = (
    relationship_sub_types_per_object_type[
        "{http://www.loc.gov/premis/v3}intellectualEntity"
    ]
    + relationship_sub_types_per_object_type[
        "{http://www.loc.gov/premis/v3}representation"
    ]
    + relationship_sub_types_per_object_type["{http://www.loc.gov/premis/v3}file"]
    + relationship_sub_types_per_object_type["{http://www.loc.gov/premis/v3}bitstream"]
)

object_identifier_types = [
    # Main keys
    "UUID",
    "MEEMOO-LOCAL-ID",
    "MEEMOO-PID",
    # Overige lokale CP ID - https://developer.meemoo.be/docs/metadata/viaa/algemeen.html#mogelijke-sleutels
    "Acquisition_number",
    "Alternative_number",
    "Analoge_drager",
    "Api",
    "Ardome",
    "Basis",
    "Bestandsnaam",
    "DataPID",
    "Historical_carrier",
    "Historical_record_number",
    "Inventarisnummer",
    "MEDIA_ID",
    "Object_number",
    "Pdf",
    "PersistenteURI_Record",
    "PersistenteURI_VKC_Record",
    "PersistenteURI_VKC_Werk",
    "PersistenteURI_Werk",
    "Priref",
    "Vaf_ID",
    "Topstuk_ID",
    "Word_ID",
    "WorkPID",
]

agent_types = [
    "person",
    "organization",
    "hardware",
    "software",
]

supported_hashes = [
    "MD5",
]

licenses = [
    # licenties van developer.meemoo.be
    "VIAA-ONDERWIJS",
    "ONDERWIJS-FRAGMENT",
    "VIAA-ONDERZOEK",
    "VIAA-INTRA_CP-CONTENT",
    "VIAA-INTRA_CP-METADATA-ALL",
    "VIAA-PUBLIEK-CONTENT",
    "VIAA-PUBLIEK-METADATA-LTD",
    "VIAA-PUBLIEK-METADATA-ALL",
    "BEZOEKERTOOL-CONTENT",
    "BEZOEKERTOOL-METADATA-ALL",
    "VIAA-INTRAMUROS",
    "CC_BY-CONTENT",
    "CC_BY-SA-CONTENT",
    "CC0-CONTENT",
    "CC_BY-NC-CONTENT",
    "CC_BY-ND-CONTENT",
    "CC_BY-NC-ND-CONTENT",
    "CC_BY-METADATA",
    "CC_BY-SA-METADATA",
    "CC0-METADATA",
    "CC_BY-NC-METADATA",
    "CC_BY-ND-METADATA",
    "CC_BY-NC-ND-METADATA",
    "CC0-METADATA",
    # licenties van datamodels
    "VIAA-BIBLIOTHEKEN",
]
