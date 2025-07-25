from typing import Self
from pathlib import Path

from eark_models.mets.v1_12_1 import METS
import eark_models.premis.v3_0 as premis
from eark_models.sip.v2_2_0 import SIP, PackageMetadata
from eark_models.utils import XMLBase

from pydantic.dataclasses import dataclass

from meemoo_sip_validator.v2_1._core.premis.reports import (
    report_unique_object_identifiers,
)


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
    return [
        # Object 1
        premis.IntellectualEntity(
            xsi_type="{http://www.loc.gov/premis/v3}intellectualEntity",
            identifiers=[
                premis.ObjectIdentifier(
                    type=premis.ObjectIdentifierType(
                        text="UUID", authority=None, authority_uri=None, value_uri=None
                    ),
                    value=premis.ObjectIdentifierValue(text="1"),
                    simple_link=None,
                )
            ],
            significant_properties=[],
            original_name=None,
            relationships=[],
        ),
        # Object 2
        premis.Representation(
            xsi_type="{http://www.loc.gov/premis/v3}representation",
            identifiers=[
                premis.ObjectIdentifier(
                    type=premis.ObjectIdentifierType(
                        text="UUID", authority=None, authority_uri=None, value_uri=None
                    ),
                    value=premis.ObjectIdentifierValue(text="2"),
                    simple_link=None,
                )
            ],
            significant_properties=[],
            original_name=None,
            relationships=[],
            storages=[],
        ),
    ]


@dataclass
class Dummy(XMLBase):
    @classmethod
    def from_xml(cls, path: Path) -> Self:
        return cls()


def test_empty_sip():
    sip = empty_sip(Dummy())
    report = report_unique_object_identifiers(sip)

    assert report.outcome == "PASSED"


def test_correct_case():
    sip = empty_sip(Dummy())
    sip.metadata.preservation.objects = get_sample_objects()
    report = report_unique_object_identifiers(sip)

    assert report.outcome == "PASSED"


def test_duplicate_identifier():
    sip = empty_sip(Dummy())
    sip.metadata.preservation.objects = get_sample_objects()
    sip.metadata.preservation.objects[1].identifiers[0].value.text = "1"
    report = report_unique_object_identifiers(sip)

    assert report.outcome == "FAILED"
