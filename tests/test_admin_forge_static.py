import os
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import admin_forge


def test_publish_static_file_writes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    path = admin_forge.publish_static_file('verify.html', 'hello')
    assert os.path.exists(path)
    assert open(path).read() == 'hello'


def test_publish_meta_token_writes(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    # simulate admin action by writing directly
    admin_forge.publish_static_file('google_meta_verification.txt', 'meta-token-123')
    assert os.path.exists('static/google_meta_verification.txt')
    assert open('static/google_meta_verification.txt').read() == 'meta-token-123'
