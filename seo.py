import os
from datetime import datetime
from typing import Iterable

DEFAULT_SITE_URL = os.environ.get("ZTRAP_SITE_URL", "https://zwanski.streamlit.app")


def regenerate_sitemap(dynamic_tools: Iterable[str] = (), out_path: str = "static/sitemap.xml", site_url: str = None, lastmod: str = None):
    """Regenerates a sitemap.xml file including dynamic tools.

    dynamic_tools: iterable of tool names
    out_path: path to write the sitemap (default static/sitemap.xml)
    site_url: base public URL (defaults to DEFAULT_SITE_URL env or constant)
    lastmod: YYYY-MM-DD string for lastmod (defaults to today)
    """
    site_url = site_url or DEFAULT_SITE_URL
    lastmod = lastmod or datetime.utcnow().strftime("%Y-%m-%d")

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]

    # Core pages
    core_pages = [
        ('/', 'daily', '1.0'),
        ('/?page=dictionary', 'weekly', '0.8'),
        ('/?page=osint', 'monthly', '0.7'),
        ('/?page=admin-forge', 'monthly', '0.6'),
    ]

    for path, changefreq, priority in core_pages:
        lines.append('  <url>')
        lines.append(f'    <loc>{site_url}{path}</loc>')
        lines.append(f'    <lastmod>{lastmod}</lastmod>')
        lines.append(f'    <changefreq>{changefreq}</changefreq>')
        lines.append(f'    <priority>{priority}</priority>')
        lines.append('  </url>')

    # Dynamic tools
    for t in dynamic_tools:
        loc = f'{site_url}/?tool={t}'
        lines.append('  <url>')
        lines.append(f'    <loc>{loc}</loc>')
        lines.append(f'    <lastmod>{lastmod}</lastmod>')
        lines.append('    <changefreq>weekly</changefreq>')
        lines.append('    <priority>0.5</priority>')
        lines.append('  </url>')

    lines.append('</urlset>')

    # Ensure directory exists
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines) + '\n')

    return out_path
