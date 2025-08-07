from pathlib import Path
from functools import reduce
from dataclasses import dataclass

from .report import Report, RuleResult
from . import utils
from .codes import Code


@dataclass
class _Path:
    __source__: str
    path: Path


def check_descriptive_folder_exists(sip_path: Path) -> RuleResult[_Path]:
    descriptive_dir = sip_path / "metadata" / "descriptive"
    invalid_paths = [descriptive_dir] if not descriptive_dir.exists() else []
    return RuleResult(
        code=Code.structure_valid,
        failed_items=[_Path(str(p), p) for p in invalid_paths],
        fail_msg=lambda _path: "The folder 'metadata/descriptive' must be present and contain a single file containing the descriptive metadata",
        success_msg="Descriptive metadata folder exists.",
    )


def check_descriptive_file_exists(sip_path: Path) -> RuleResult[_Path] | None:
    profile = utils.get_profile(sip_path)
    if profile is None:
        return None

    descriptive_dir = sip_path / "metadata" / "descriptive"
    match profile:
        case utils.Profile.BASIC:
            descriptive_file = descriptive_dir / "dc+schema.xml"
        case utils.Profile.FILM:
            descriptive_file = descriptive_dir / "dc+schema.xml"
        case utils.Profile.MATERIAL_ARTWORK:
            descriptive_file = descriptive_dir / "dc+schema.xml"

    invalid_paths = [descriptive_file] if not descriptive_file.exists() else []
    return RuleResult(
        code=Code.structure_valid,
        failed_items=[_Path(str(p), p) for p in invalid_paths],
        fail_msg=lambda _path: f"The file '{_path.path}' must be present and contain the descriptive metadata.",
        success_msg="Descriptive metadata file exists.",
    )


def check_representations_folder_exists(sip_path: Path) -> RuleResult[_Path]:
    representations_dir = sip_path / "representations"
    invalid_paths = [representations_dir] if not representations_dir.exists() else []
    return RuleResult(
        code=Code.structure_valid,
        failed_items=[_Path(str(p), p) for p in invalid_paths],
        fail_msg=lambda _path: "The folder 'representations' must be present and contain a subfolder for each representation.",
        success_msg="Representations folder exists.",
    )


def check_at_least_one_repesentation_exists(sip_path: Path) -> RuleResult[_Path] | None:
    representations_dir = sip_path / "representations"
    if not representations_dir.exists():
        return None

    representations = list(representations_dir.iterdir())
    invalid_paths = [representations_dir] if len(representations) < 1 else []

    return RuleResult(
        code=Code.structure_valid,
        failed_items=[_Path(str(p), p) for p in invalid_paths],
        fail_msg=lambda _path: "The representations folder must contain at least one representation.",
        success_msg="At least one represesentation folder present.",
    )


def check_root_preservation_folder_exists(sip_path: Path) -> RuleResult[_Path]:
    preservation_dir = sip_path / "metadata" / "preservation"
    invalid_paths = [preservation_dir] if not preservation_dir.exists() else []
    return RuleResult(
        code=Code.structure_valid,
        failed_items=[_Path(str(p), p) for p in invalid_paths],
        fail_msg=lambda _path: "The folder 'metadata/preservation' must be present and contain premis.xml file.",
        success_msg="Root preservation folder exists.",
    )


def check_root_premis_exists(sip_path: Path) -> RuleResult[_Path]:
    premis_file = sip_path / "metadata" / "preservation" / "premis.xml"
    invalid_paths = [premis_file] if not premis_file.exists() else []
    return RuleResult(
        code=Code.structure_valid,
        failed_items=[_Path(str(p), p) for p in invalid_paths],
        fail_msg=lambda _path: "The file 'metadata/preservation/premis.xml' must be present and contain the preservation metadata.",
        success_msg="Root PREMIS exists.",
    )


def check_representation_premis_exists(sip_path: Path) -> RuleResult[_Path]:
    representations = sip_path.joinpath("representations").glob("*")
    premises = (
        repr / "metadata" / "preservation" / "premis.xml" for repr in representations
    )
    invalid_paths = [premis for premis in premises if not premis.exists()]
    return RuleResult(
        code=Code.structure_valid,
        failed_items=[_Path(str(p), p) for p in invalid_paths],
        fail_msg=lambda _path: f"The representation '{_path.path.parent.parent.parent.name}' is missing preservation metadata at '{_path.path}'.",
        success_msg="Representation PREMIS files exists.",
    )


def check_representation_mets_exists(sip_path: Path) -> RuleResult[_Path]:
    representations = sip_path.joinpath("representations").glob("*")
    metses = (repr / "METS.xml" for repr in representations)
    invalid_paths = [mets for mets in metses if not mets.exists()]
    return RuleResult(
        code=Code.structure_valid,
        failed_items=[_Path(str(p), p) for p in invalid_paths],
        fail_msg=lambda _path: f"The representation '{_path.path.parent.name}' is missing a METS.xml file.",
        success_msg="Representation METS files exists.",
    )


def check_representation_data_exists(sip_path: Path) -> RuleResult[_Path]:
    representations = sip_path.joinpath("representations").glob("*")
    data_folders = (repr / "data" for repr in representations)
    invalid_paths = [folder for folder in data_folders if not folder.exists()]
    return RuleResult(
        code=Code.structure_valid,
        failed_items=[_Path(str(p), p) for p in invalid_paths],
        fail_msg=lambda _path: f"The representation '{_path.path.parent.name}' is missing folder 'data'.",
        success_msg="Representation data folder exists.",
    )


def check_representation_data_contains_file(sip_path: Path) -> RuleResult[_Path]:
    representations = sip_path.joinpath("representations").glob("*")
    data_folders = [
        repr / "data" for repr in representations if repr.joinpath("data").exists()
    ]
    invalid_paths = [
        folder for folder in data_folders if len(list(folder.iterdir())) < 1
    ]
    return RuleResult(
        code=Code.structure_valid,
        failed_items=[_Path(str(p), p) for p in invalid_paths],
        fail_msg=lambda _path: f"The representation '{_path.path.parent.name}' has an empty 'data' folder.",
        success_msg="Representation data folder contains data.",
    )


checks = [
    check_descriptive_folder_exists,
    check_descriptive_file_exists,
    check_representations_folder_exists,
    check_at_least_one_repesentation_exists,
    check_root_preservation_folder_exists,
    check_root_premis_exists,
    check_representation_premis_exists,
    check_representation_mets_exists,
    check_representation_data_exists,
    check_representation_data_contains_file,
]


def validate_structural(sip_path: Path) -> Report:
    rule_results = (check(sip_path) for check in checks)
    reports = (rule.to_report() for rule in rule_results if rule is not None)
    return reduce(Report.__add__, reports)
