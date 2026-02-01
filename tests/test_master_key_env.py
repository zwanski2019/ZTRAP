def test_master_key_env_present():
    s = open("app.py").read()
    assert "ZTRAP_MASTER_KEY" in s
    assert "os.getenv(" in s


def test_master_key_defaults_to_zwanski():
    # Validate that the default string is still present for backward compatibility
    s = open("app.py").read()
    assert '"zwanski"' in s
