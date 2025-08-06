from pathlib import Path
import xml.etree.ElementTree as ET
from enum import Enum


class ValidatorError(Exception):
    pass


class Profile(Enum):
    BASIC = "https://data.hetarchief.be/id/sip/2.1/basic"
    FILM = "https://data.hetarchief.be/id/sip/2.1/film"
    MATERIAL_ARTWORK = "https://data.hetarchief.be/id/sip/2.1/material-artwork"


profiles = [p.value for p in Profile]


def get_profile(sip_path: Path) -> Profile | None:
    root_mets_path = sip_path / "METS.xml"
    try:
        mets_root = ET.parse(root_mets_path).getroot()
    except Exception:
        return None

    profile = mets_root.get(
        "{https://DILCIS.eu/XML/METS/CSIPExtensionMETS}OTHERCONTENTINFORMATIONTYPE"
    )
    if profile not in profiles:
        return None
    return Profile(profile)
