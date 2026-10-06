import shutil
from pathlib import Path

import pytest

from meemoo_sip_validator.v2_1._core.codes import Code
from meemoo_sip_validator.v2_1._core.report import Failure
from meemoo_sip_validator.v2_1._core.utils import Profile
from meemoo_sip_validator.v2_1._core.xsd import validate_descriptive

newspaper_sip_paths = [
    next(path.iterdir()) for path in Path("tests/sip-examples/2.1").glob("newspaper_*")
]
newspaper_sip_names = [path.parent.name for path in newspaper_sip_paths]


def copy_sip(sip_path: Path, tmp_path: Path) -> Path:
    copy_path = tmp_path / sip_path.name
    _ = shutil.copytree(sip_path / "metadata", copy_path / "metadata")
    return copy_path


@pytest.mark.parametrize("sip_path", newspaper_sip_paths, ids=newspaper_sip_names)
def test_validate_descriptive_bibliographic_valid(sip_path: Path):
    report = validate_descriptive(sip_path, Profile.BIBLIOGRAPHIC)

    assert report.outcome == "PASSED"
    assert "mods-3-7" in report.results[0].message


@pytest.mark.parametrize("sip_path", newspaper_sip_paths, ids=newspaper_sip_names)
def test_validate_descriptive_bibliographic_invalid(sip_path: Path, tmp_path: Path):
    sip_path = copy_sip(sip_path, tmp_path)
    mods_path = sip_path / "metadata" / "descriptive" / "mods.xml"
    mods = mods_path.read_text(encoding="utf-8")
    mods = mods.replace("<mods:titleInfo>", "<mods:unknownElement/><mods:titleInfo>", 1)
    _ = mods_path.write_text(mods, encoding="utf-8")

    report = validate_descriptive(sip_path, Profile.BIBLIOGRAPHIC)

    assert report.outcome == "FAILED"
    failures = list(report.failures)
    assert len(failures) == 1
    assert isinstance(failures[0], Failure)
    assert failures[0].code == Code.xsd_valid
    assert failures[0].source == str(mods_path)
    assert "unknownElement" in failures[0].message
