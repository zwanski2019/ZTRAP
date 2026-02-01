import os


def test_static_files_present():
    assert os.path.exists('.streamlit/config.toml')
    assert os.path.exists('static/google5c6ccd94a91913a6.html')
    assert os.path.exists('static/sitemap.xml')
    assert os.path.exists('static/robots.txt')


def test_app_contains_structured_data():
    s = open('app.py').read()
    assert 'application/ld+json' in s
    assert 'Zwanski Tech ZTRAP' in s
