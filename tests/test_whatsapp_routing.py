def test_whatsapp_engine_exports():
    import whatsapp_engine as w

    assert hasattr(w, "install_whatsapp_osint") and callable(w.install_whatsapp_osint)
    assert hasattr(w, "run_whatsapp_scan") and callable(w.run_whatsapp_scan)
    assert getattr(w, "WSP_PATH", None) == "WhatsApp-OSINT"


def test_app_menu_contains_whatsapp():
    s = open("app.py").read()
    assert "WHATSAPP-OSINT" in s
