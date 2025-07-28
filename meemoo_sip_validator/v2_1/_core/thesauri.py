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
