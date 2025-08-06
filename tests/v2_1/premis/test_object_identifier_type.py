from meemoo_sip_validator.v2_1._core.codes import Code
from tests.v2_1 import utils


from meemoo_sip_validator.v2_1._core.premis.premis import (
    check_object_identifier_type_vocabulary,
)


def test_empty_sip():
    sip = utils.empty_sip(utils.Dummy())
    report = check_object_identifier_type_vocabulary(sip).to_report()

    assert report.outcome == "PASSED"


def test_correct_case():
    sip = utils.empty_sip(utils.Dummy())
    sip.metadata.preservation.objects = utils.get_sample_objects()

    report = check_object_identifier_type_vocabulary(sip).to_report()

    assert report.outcome == "PASSED"


def test_incorrect_object_identifier_type():
    sip = utils.empty_sip(utils.Dummy())
    sip.metadata.preservation.objects = utils.get_sample_objects()
    object_identifier = sip.metadata.preservation.objects[1].identifiers[0]
    object_identifier.type.text = "non-valid-object-identifier-type"

    report = check_object_identifier_type_vocabulary(sip).to_report()

    assert report.outcome == "FAILED"
    fail_codes = [failure.code for failure in report.failures]
    assert Code.object_identifier_type_thesauri in fail_codes
