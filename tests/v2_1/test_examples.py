from pathlib import Path
import json

import pytest

from meemoo_sip_validator.v2_1 import validate_to_report

sip_paths = list(Path("tests/sip-examples/2.1").iterdir())

# TODO: This sip example has not been migrated fully to 2.1
sip_paths = [p for p in sip_paths if "ftp_sidecar" not in str(p)]

unzipped_paths = [next(path.iterdir()) for path in sip_paths]


@pytest.mark.parametrize("unzipped_path", unzipped_paths)
def test_examples(unzipped_path: Path):
    report = validate_to_report(unzipped_path)
    report_dumped = report.model_dump()
    print(json.dumps(report_dumped, indent=1))
    assert report.outcome == "PASSED"
