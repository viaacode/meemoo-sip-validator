from meemoo_sip_validator.v2_1._core.codes import Code
from tests.v2_1 import utils


from meemoo_sip_validator.v2_1._core.premis.reports import (
    check_unique_object_identifiers,
)


def test_empty_sip():
    sip = utils.empty_sip(utils.Dummy())
    report = check_unique_object_identifiers(sip).to_report()

    assert report.outcome == "PASSED"


def test_correct_case():
    sip = utils.empty_sip(utils.Dummy())
    sip.metadata.preservation.objects = utils.get_sample_objects()

    report = check_unique_object_identifiers(sip).to_report()

    assert report.outcome == "PASSED"


def test_duplicate_identifier():
    sip = utils.empty_sip(utils.Dummy())
    sip.metadata.preservation.objects = utils.get_sample_objects()
    sip.metadata.preservation.objects[1].identifiers[0].value.text = "1"

    report = check_unique_object_identifiers(sip).to_report()

    assert report.outcome == "FAILED"
    error_codes = [error.code for error in report.errors]
    assert Code.unique_object_identifiers in error_codes
