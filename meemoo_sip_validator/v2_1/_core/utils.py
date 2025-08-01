from pathlib import Path
import xml.etree.ElementTree as ET
from enum import Enum


class Profile(Enum):
    BASIC = "https://data.hetarchief.be/id/sip/2.1/basic"
    FILM = "https://data.hetarchief.be/id/sip/2.1/film"
    MATERIAL_ARTWORK = "https://data.hetarchief.be/id/sip/2.1/material-artwork"


profiles = [p.value for p in Profile]


def get_profile(unzipped_path: Path) -> Profile | None:
    root_mets_path = unzipped_path.joinpath("METS.xml")
    mets_root = ET.parse(root_mets_path).getroot()
    profile = mets_root.get(
        "{https://DILCIS.eu/XML/METS/CSIPExtensionMETS}OTHERCONTENTINFORMATIONTYPE"
    )
    if profile not in profiles:
        return None
    return Profile(profile)
