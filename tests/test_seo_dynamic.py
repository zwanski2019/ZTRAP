import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from seo import regenerate_sitemap


def test_regenerate_sitemap_creates_file(tmp_path):
    out = tmp_path / "sitemap.xml"
    # call with some tools
    path = regenerate_sitemap(['alpha', 'beta'], out_path=str(out), site_url='https://example.com', lastmod='2026-02-01')
    assert os.path.exists(path)
    content = open(path).read()
    assert '<loc>https://example.com/?tool=alpha</loc>' in content
    assert '<loc>https://example.com/?tool=beta</loc>' in content
    assert '<loc>https://example.com/</loc>' in content
