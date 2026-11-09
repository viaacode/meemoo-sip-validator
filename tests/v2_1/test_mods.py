import shutil
from pathlib import Path

import pytest

from meemoo_sip_validator.v2_1._core.codes import Code
from meemoo_sip_validator.v2_1._core.descriptive.mods import (
    is_valid_edtf,
    validate_mods,
)

newspaper_sip_paths = [
    next(path.iterdir()) for path in Path("tests/sip-examples/2.1").glob("newspaper_*")
]
newspaper_sip_names = [path.parent.name for path in newspaper_sip_paths]


def copy_sip(sip_path: Path, tmp_path: Path) -> Path:
    copy_path = tmp_path / sip_path.name
    _ = shutil.copytree(sip_path / "metadata", copy_path / "metadata")
    return copy_path


def edit_mods(sip_path: Path, old: str, new: str) -> Path:
    mods_path = sip_path / "metadata" / "descriptive" / "mods.xml"
    mods = mods_path.read_text(encoding="utf-8")
    assert old in mods
    _ = mods_path.write_text(mods.replace(old, new, 1), encoding="utf-8")
    return mods_path


@pytest.mark.parametrize(
    "edtf_value",
    ["1895-01-28", "1895-01", "1895/1896", "19XX", "1984?", "XXXX-XX-XX"],
)
def test_is_valid_edtf(edtf_value: str):
    assert is_valid_edtf(edtf_value)


@pytest.mark.parametrize(
    "edtf_value", ["28-01-1895", "", "XXXX", "XXXX-XX", "1XXX", "1895-01-28 "]
)
def test_is_invalid_edtf(edtf_value: str):
    assert not is_valid_edtf(edtf_value)


@pytest.mark.parametrize("sip_path", newspaper_sip_paths, ids=newspaper_sip_names)
def test_validate_mods_valid(sip_path: Path):
    report = validate_mods(sip_path)

    assert report.outcome == "PASSED"


@pytest.mark.parametrize("sip_path", newspaper_sip_paths, ids=newspaper_sip_names)
def test_validate_mods_invalid_edtf(sip_path: Path, tmp_path: Path):
    sip_path = copy_sip(sip_path, tmp_path)
    # construct a nested date
    mods_path = edit_mods(
        sip_path,
        "</mods:mods>",
        "<mods:relatedItem><mods:originInfo>"
        + '<mods:dateIssued encoding="edtf">02-08-2022</mods:dateIssued>'
        + "<mods:dateIssued>not EDTF, so not checked</mods:dateIssued>"
        + "</mods:originInfo></mods:relatedItem></mods:mods>",
    )

    report = validate_mods(sip_path)

    assert report.outcome == "FAILED"
    failures = list(report.failures)
    assert len(failures) == 1
    assert failures[0].code == Code.edtf_valid
    assert failures[0].source == str(mods_path)
    assert "'02-08-2022'" in failures[0].message


@pytest.mark.parametrize("sip_path", newspaper_sip_paths, ids=newspaper_sip_names)
def test_validate_mods_with_name(sip_path: Path, tmp_path: Path):
    sip_path = copy_sip(sip_path, tmp_path)
    _ = edit_mods(
        sip_path,
        "<mods:originInfo>",
        '<mods:name type="personal">'
        + '<mods:namePart type="family">Janssens</mods:namePart>'
        + '<mods:role><mods:roleTerm type="text">auteur</mods:roleTerm></mods:role>'
        + "</mods:name><mods:originInfo>",
    )

    report = validate_mods(sip_path)

    assert report.outcome == "PASSED"


def remove_lines(sip_path: Path, *fragments: str) -> None:
    mods_path = sip_path / "metadata" / "descriptive" / "mods.xml"
    lines = mods_path.read_text(encoding="utf-8").splitlines()
    kept = [line for line in lines if not any(f in line for f in fragments)]
    assert len(kept) < len(lines)
    _ = mods_path.write_text("\n".join(kept), encoding="utf-8")


def single_failure(sip_path: Path):
    report = validate_mods(sip_path)
    assert report.outcome == "FAILED"
    failures = list(report.failures)
    assert len(failures) == 1
    return failures[0]


@pytest.mark.parametrize("sip_path", newspaper_sip_paths, ids=newspaper_sip_names)
def test_validate_mods_no_dutch_genre(sip_path: Path, tmp_path: Path):
    sip_path = copy_sip(sip_path, tmp_path)
    remove_lines(sip_path, '<mods:genre xml:lang="nl">')

    failure = single_failure(sip_path)
    assert failure.code == Code.mods_genre_dutch
    assert "BICP33" in failure.message


@pytest.mark.parametrize("sip_path", newspaper_sip_paths, ids=newspaper_sip_names)
def test_validate_mods_no_genre(sip_path: Path, tmp_path: Path):
    sip_path = copy_sip(sip_path, tmp_path)
    remove_lines(sip_path, "<mods:genre")

    assert validate_mods(sip_path).outcome == "PASSED"


@pytest.mark.parametrize("sip_path", newspaper_sip_paths, ids=newspaper_sip_names)
def test_validate_mods_no_dutch_topic(sip_path: Path, tmp_path: Path):
    sip_path = copy_sip(sip_path, tmp_path)
    _ = edit_mods(
        sip_path,
        '<mods:topic xml:lang="nl">katten</mods:topic>',
        '<mods:topic xml:lang="de">Katzen</mods:topic>',
    )

    failure = single_failure(sip_path)
    assert failure.code == Code.mods_topic_dutch
    assert "BICP37" in failure.message


@pytest.mark.parametrize("sip_path", newspaper_sip_paths, ids=newspaper_sip_names)
def test_validate_mods_no_topic(sip_path: Path, tmp_path: Path):
    sip_path = copy_sip(sip_path, tmp_path)
    remove_lines(sip_path, "<mods:topic")

    assert validate_mods(sip_path).outcome == "PASSED"
