from typing import Self
from pathlib import Path

from eark_models.mets.v1_12_1 import METS
import eark_models.premis.v3_0 as premis
from eark_models.sip.v2_2_0 import SIP, PackageMetadata
from eark_models.utils import XMLBase

from pydantic.dataclasses import dataclass


@dataclass
class Dummy(XMLBase):
    @classmethod
    def from_xml(cls, path: Path) -> Self:
        return cls()


def empty_sip[T: XMLBase](descriptive: T) -> SIP[T]:
    return SIP[T](
        mets=METS(),
        metadata=PackageMetadata(
            descriptive=descriptive,
            preservation=premis.Premis(
                objects=[],
                events=[],
                agents=[],
                version="3.0",
            ),
        ),
        representations=[],
    )


def get_sample_objects() -> list[premis.Object]:
    premis_model = premis.Premis.from_xml(Path("tests/v2_1/premis/assets/objects.xml"))
    return premis_model.objects
