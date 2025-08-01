from pathlib import Path
import json

import pytest

from meemoo_sip_validator.v2_1._core.report import Report
from meemoo_sip_validator.v2_1 import validate_to_report

sip_paths = set(Path("tests/sip-examples/2.1").iterdir())

exclude = [
    "tests/sip-examples/2.1/ftp_sidecar_904c6e86-d36a-4630-897b-bb560ce4b690",
    "tests/sip-examples/2.1/newspaper_tiff_alto_pdf_ebe47259-8f23-4a2d-bf49-55ae1d855393",
    "tests/sip-examples/2.1/newspaper_c44a0b0d-6e2f-4af2-9dab-3a9d447288d0",
    "tests/sip-examples/2.1/subtitles_d3e1a978-3dd8-4b46-9314-d9189a1c94c6",
]

excluded_paths = {Path(p) for p in exclude}

sip_paths = sip_paths - excluded_paths
unzipped_paths = [(next(path.iterdir())) for path in sip_paths]
unzipped_path_names = [str(path.parent.name) for path in unzipped_paths]


@pytest.mark.parametrize("unzipped_path", unzipped_paths, ids=unzipped_path_names)
def test_examples(unzipped_path: Path):
    report = validate_to_report(unzipped_path)
    failures_dumped = Report(results=list(report.failures)).to_dict()
    print(json.dumps(failures_dumped, indent=1))
    assert report.outcome == "PASSED"
