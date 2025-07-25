from .. import utils


from meemoo_sip_validator.v2_1._core.premis.reports import (
    report_unique_object_identifiers,
)


def test_empty_sip():
    sip = utils.empty_sip(utils.Dummy())
    report = report_unique_object_identifiers(sip)

    assert report.outcome == "PASSED"


def test_correct_case():
    sip = utils.empty_sip(utils.Dummy())
    sip.metadata.preservation.objects = utils.get_sample_objects()
    report = report_unique_object_identifiers(sip)

    assert report.outcome == "PASSED"


def test_duplicate_identifier():
    sip = utils.empty_sip(utils.Dummy())
    sip.metadata.preservation.objects = utils.get_sample_objects()
    sip.metadata.preservation.objects[1].identifiers[0].value.text = "1"
    report = report_unique_object_identifiers(sip)

    assert report.outcome == "FAILED"
