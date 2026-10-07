from transit_policy import transit_ok


def test_https_partner_ok():
    assert transit_ok("https://api.afyaplus.ke/triage") is True


def test_localhost_http_lab_exception():
    assert transit_ok("http://127.0.0.1:8000/triage") is True


def test_cleartext_production_host_denied():
    assert transit_ok("http://api.afyaplus.ke/triage") is False
