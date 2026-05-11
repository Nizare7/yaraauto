#!/usr/bin/env python3
"""
Generate city landing pages from templates/landing_template.html
Run: python scripts/generate_city_pages.py
This will create <slug>.html files and update sitemap.xml
"""
import os
from datetime import date

BASE = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_PATH = os.path.join(BASE, 'templates', 'landing_template.html')
SITEMAP_PATH = os.path.join(BASE, 'sitemap.xml')

CITIES = [
    ("Milano", "Milano", "MI"),
    ("Torino", "Torino", "TO"),
    ("Bergamo", "Bergamo", "BG"),
    ("Brescia", "Brescia", "BS"),
    ("Verona", "Verona", "VR"),
    ("Venezia", "Venezia", "VE"),
    ("Padova", "Padova", "PD"),
    ("Genova", "Genova", "GE"),
    ("Bologna", "Bologna", "BO"),
    ("Monza", "Monza", "MB"),
]


def slugify(name: str) -> str:
    return name.lower().replace(' ', '-')


def generate_pages():
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        tpl = f.read()

    generated = []
    for city, province_full, province_code in CITIES:
        slug = slugify(city)
        out = tpl.replace('{{CITY}}', city).replace('{{PROVINCE_FULL}}', province_full).replace('{{SLUG}}', slug)
        out_path = os.path.join(BASE, f'{slug}.html')
        with open(out_path, 'w', encoding='utf-8') as g:
            g.write(out)
        print('Wrote', out_path)
        generated.append((slug, city))

    update_sitemap(generated)


def update_sitemap(generated):
    # read existing sitemap and preserve index/privacy/cookie if present
    entries = []
    if os.path.exists(SITEMAP_PATH):
        with open(SITEMAP_PATH, 'r', encoding='utf-8') as f:
            txt = f.read()
        # naive: keep the header/footer and rebuild inner urls
    # build new sitemap
    today = date.today().isoformat()
    urls = [
        ('https://yaraauto.it/', today, 'weekly', '1.0'),
        ('https://yaraauto.it/privacy.html', today, 'yearly', '0.2'),
        ('https://yaraauto.it/cookie.html', today, 'yearly', '0.2'),
    ]
    for slug, city in generated:
        urls.append((f'https://yaraauto.it/{slug}.html', today, 'monthly', '0.6'))

    with open(SITEMAP_PATH, 'w', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n\n')
        for loc, lastmod, changefreq, priority in urls:
            f.write('  <url>\n')
            f.write(f'    <loc>{loc}</loc>\n')
            f.write(f'    <lastmod>{lastmod}</lastmod>\n')
            f.write(f'    <changefreq>{changefreq}</changefreq>\n')
            f.write(f'    <priority>{priority}</priority>\n')
            f.write('  </url>\n\n')
        f.write('</urlset>\n')
    print('Updated sitemap at', SITEMAP_PATH)


if __name__ == '__main__':
    generate_pages()
