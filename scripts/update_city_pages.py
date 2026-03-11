#!/usr/bin/env python3
"""Update all 17 city pages: schema + internal linking blocks"""
import re, os, json

CITIES_DIR = 'resources/templates/landing/cities'

# City slug -> Display Name
CITY_NAMES = {
    'burnaby': 'Burnaby',
    'coquitlam': 'Coquitlam',
    'delta': 'Delta',
    'ladner': 'Ladner',
    'langley': 'Langley',
    'maple_ridge': 'Maple Ridge',
    'new_westminster': 'New Westminster',
    'north_vancouver': 'North Vancouver',
    'pitt_meadows': 'Pitt Meadows',
    'port_coquitlam': 'Port Coquitlam',
    'port_moody': 'Port Moody',
    'richmond': 'Richmond',
    'surrey': 'Surrey',
    'tsawwassen': 'Tsawwassen',
    'vancouver': 'Vancouver',
    'west_vancouver': 'West Vancouver',
    'white_rock': 'White Rock',
}

# Nearby cities (5-6 max, based on Metro Vancouver geography)
NEARBY = {
    'vancouver': ['burnaby', 'north_vancouver', 'west_vancouver', 'richmond', 'new_westminster'],
    'burnaby': ['vancouver', 'new_westminster', 'coquitlam', 'port_moody', 'north_vancouver'],
    'surrey': ['delta', 'langley', 'white_rock', 'new_westminster', 'coquitlam'],
    'richmond': ['vancouver', 'delta', 'ladner', 'tsawwassen', 'burnaby'],
    'coquitlam': ['burnaby', 'port_coquitlam', 'port_moody', 'new_westminster', 'surrey'],
    'langley': ['surrey', 'maple_ridge', 'delta', 'coquitlam', 'port_coquitlam'],
    'delta': ['surrey', 'richmond', 'ladner', 'tsawwassen', 'langley'],
    'new_westminster': ['burnaby', 'surrey', 'coquitlam', 'richmond', 'vancouver'],
    'north_vancouver': ['west_vancouver', 'vancouver', 'burnaby'],
    'west_vancouver': ['north_vancouver', 'vancouver', 'burnaby'],
    'maple_ridge': ['pitt_meadows', 'port_coquitlam', 'coquitlam', 'langley', 'surrey'],
    'pitt_meadows': ['maple_ridge', 'port_coquitlam', 'coquitlam', 'surrey'],
    'port_coquitlam': ['coquitlam', 'pitt_meadows', 'port_moody', 'maple_ridge', 'burnaby'],
    'port_moody': ['coquitlam', 'port_coquitlam', 'burnaby'],
    'white_rock': ['surrey', 'delta', 'langley'],
    'tsawwassen': ['delta', 'ladner', 'richmond'],
    'ladner': ['delta', 'tsawwassen', 'richmond'],
}

def generate_schema(slug, name, current_title):
    """Generate new schema JSON-LD for city page"""
    desc = f"Professional gutter cleaning services in {name}, BC. We also provide window washing, pressure washing, moss removal and other exterior cleaning services."
    
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebPage",
                "@id": f"https://cgc-services.ca/cities/{slug}#webpage",
                "url": f"https://cgc-services.ca/cities/{slug}",
                "name": current_title,
                "description": desc,
                "isPartOf": {"@id": "https://cgc-services.ca/#website"},
                "about": {"@id": "https://cgc-services.ca/#business"},
                "breadcrumb": {"@id": f"https://cgc-services.ca/cities/{slug}#breadcrumb"},
                "inLanguage": "en-CA"
            },
            {
                "@type": "BreadcrumbList",
                "@id": f"https://cgc-services.ca/cities/{slug}#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://cgc-services.ca/"},
                    {"@type": "ListItem", "position": 2, "name": name, "item": f"https://cgc-services.ca/cities/{slug}"}
                ]
            },
            {
                "@type": "Service",
                "@id": f"https://cgc-services.ca/cities/{slug}#service",
                "name": f"Exterior Cleaning Services in {name}",
                "provider": {"@id": "https://cgc-services.ca/#business"},
                "areaServed": {"@type": "City", "name": name},
                "serviceType": [
                    "Gutter Cleaning",
                    "Window Washing",
                    "Pressure Washing",
                    "Moss Removal",
                    "Junk Removal",
                    "Handyman Services"
                ]
            }
        ]
    }
    return json.dumps(schema, indent=2, ensure_ascii=False)

def generate_linking_block(slug, name):
    """Generate internal linking HTML block"""
    nearby = NEARBY.get(slug, [])
    
    nearby_links = '\n'.join([
        f'            <li><a href="/cities/{ns}">Exterior Cleaning in {CITY_NAMES[ns]}</a></li>'
        for ns in nearby
    ])
    
    block = f"""
    <div class="city-extras">
        <h2>Other Exterior Cleaning Services in {name}</h2>
        <p>In addition to gutter cleaning, we also provide:</p>
        <ul>
            <li><a href="/services/window_washing">Window Washing</a> in {name}</li>
            <li><a href="/services/pressure_washing">Pressure Washing</a> in {name}</li>
            <li><a href="/services/moss_removal">Roof Moss Removal</a> in {name}</li>
            <li><a href="/services/junk_removal">Junk Removal</a> in {name}</li>
            <li><a href="/services/handyman_services">Handyman Services</a> in {name}</li>
        </ul>

        <h2>Nearby Service Areas</h2>
        <ul>
{nearby_links}
        </ul>

        <h2>Get a Quote for Exterior Cleaning in {name}</h2>
        <p>Request a fast quote for gutter cleaning, window washing, pressure washing, moss removal or junk removal in {name}.</p>
        <div class="cta-row" style="margin-top:18px;">
            <a class="btn-primary btn-quote-animated" href="/quote">Get Your Quote</a>
        </div>
    </div>"""
    return block

# Process all city pages
updated = 0
for filename in sorted(os.listdir(CITIES_DIR)):
    if not filename.endswith('.html.twig'):
        continue
    
    slug = filename.replace('.html.twig', '')
    name = CITY_NAMES.get(slug)
    if not name:
        print(f"SKIP {slug}: no name defined")
        continue
    
    filepath = os.path.join(CITIES_DIR, filename)
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Extract current title
    title_match = re.search(r'{%\s*block title\s*%}(.*?){%\s*endblock\s*%}', content)
    current_title = title_match.group(1).strip() if title_match else f"Gutter Cleaning in {name} BC | Clean Gutters Crew"
    
    # 1. Replace schema block
    new_schema_json = generate_schema(slug, name, current_title)
    new_schema_block = f"""{{% block schema %}}
<script type="application/ld+json">
{new_schema_json}
</script>
{{% endblock %}}"""
    
    content = re.sub(
        r'{%\s*block schema\s*%}.*?{%\s*endblock\s*%}',
        new_schema_block,
        content,
        flags=re.DOTALL
    )
    
    # 2. Add linking blocks before {% endblock %} of content (last endblock)
    # Check if linking block already exists
    if 'city-extras' not in content:
        linking_block = generate_linking_block(slug, name)
        # Find the {% endblock %} that closes the content block
        # It's the last {% endblock %} or the one after block content
        content = re.sub(
            r'({%\s*endblock\s*%})\s*$',
            linking_block + '\n{% endblock %}\n',
            content.rstrip()
        )
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    updated += 1
    print(f"✅ {slug}: schema + linking updated")

print(f"\nTotal: {updated} city pages updated")
