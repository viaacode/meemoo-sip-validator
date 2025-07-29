from typing import Self, override
from pathlib import Path

from eark_models.mets.v1_12_1 import METS
import eark_models.premis.v3_0 as premis
from eark_models.sip.v2_2_0 import PackageMetadata
from eark_models.utils import XMLParseable

from pydantic.dataclasses import dataclass

from meemoo_sip_validator.v2_1._core.models import SIP


@dataclass
class Dummy(XMLParseable):
    @override
    @classmethod
    def from_xml(cls, path: Path) -> Self:
        return cls()


def empty_sip[T: XMLParseable](descriptive: T) -> SIP[T]:
    return SIP(
        mets=METS(),
        metadata=PackageMetadata(
            descriptive=descriptive,
            preservation=premis.Premis(
                __source__=".",
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
