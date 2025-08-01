from meemoo_sip_validator.v2_1._core.codes import Code
from tests.v2_1 import utils


from meemoo_sip_validator.v2_1._core.premis.premis import (
    check_object_identifiers_uniqueness,
)


def test_empty_sip():
    sip = utils.empty_sip(utils.Dummy())
    report = check_object_identifiers_uniqueness(sip).to_report()

    assert report.outcome == "PASSED"


def test_correct_case():
    sip = utils.empty_sip(utils.Dummy())
    sip.metadata.preservation.objects = utils.get_sample_objects()

    report = check_object_identifiers_uniqueness(sip).to_report()

    assert report.outcome == "PASSED"


def test_duplicate_identifier():
    sip = utils.empty_sip(utils.Dummy())
    sip.metadata.preservation.objects = utils.get_sample_objects()
    sip.metadata.preservation.objects[1].identifiers[0].value.text = "uuid-1"

    report = check_object_identifiers_uniqueness(sip).to_report()

    assert report.outcome == "FAILED"
    fail_codes = [failure.code for failure in report.failures]
    assert Code.object_identifiers_uniqueness in fail_codes
