import argparse
import html
import sys
from pathlib import Path

LABEL_MAP = {
    # Core products
    "AIHypercomputer-512-color.svg": "AI Hypercomputer",
    "AlloyDB-512-color.svg": "AlloyDB",
    "Anthos-512-color.svg": "Anthos",
    "Apigee-512-color-rgb.svg": "Apigee",
    "BigQuery-512-color.svg": "BigQuery",
    "CloudRun-512-color-rgb.svg": "Cloud Run",
    "CloudSpanner-512-color.svg": "Spanner",
    "CloudSQL-512-color.svg": "Cloud SQL",
    "Cloud_Storage-512-color.svg": "Cloud Storage",
    "ComputeEngine-512-color-rgb.svg": "Compute Engine",
    "DistributedCloud-512-color.svg": "Google Distributed Cloud",
    "GKE-512-color.svg": "GKE",
    "Hyperdisk-512-color.svg": "Hyperdisk",
    "Looker-512-color.svg": "Looker",
    "Mandiant-512-color.svg": "Mandiant",
    "SecOps-512-color-rgb.svg": "Google Security Operations",
    "SecurityCommandCenter-512-color.svg": "Security Command Center",
    "ThreatIntelligence-512-color.svg": "Google Threat Intelligence",
    "VertexAI-512-color.svg": "Vertex AI",
    # Product categories
    "Agents-512-color.svg": "AI Applications & Agents",
    "AIMachineLearning-512-color.svg": "AI & Machine Learning",
    "BusinessIntelligence-512-color.svg": "Business Intelligence",
    "Collaboration-512-color.svg": "Collaboration",
    "Compute-512-color.svg": "Compute",
    "Containers-512-color.svg": "Containers",
    "DataAnalytics-512-color.svg": "Data Analytics",
    "Databases-512-color.svg": "Databases",
    "Developer_Tools-512-color.svg": "Developer Tools",
    "DevOps-512-color.svg": "DevOps",
    "HybridMulticloud-512-color.svg": "Hybrid & Multicloud",
    "IntegrationServices-512-color.svg": "Integration Services",
    "ManagementTools-512-color.svg": "Management Tools",
    "MapsGeospatial-512-color.svg": "Maps & Geospatial",
    "Marketplace-512-color.svg": "Google Cloud Marketplace",
    "MediaServices-512-color.svg": "Media Services",
    "Migration-512-color.svg": "Migration",
    "MixedReality-512-color.svg": "Mixed Reality",
    "Networking-512-color-rgb.svg": "Networking",
    "Observability-512-color.svg": "Observability",
    "Operations-512-color.svg": "Operations",
    "SecurityIdentity-512-color.svg": "Security & Identity",
    "ServerlessComputing-512-color.svg": "Serverless Computing",
    "Storage-512-color.svg": "Storage",
    "Web3-512-color.svg": "Web3",
    "WebMobile-512-color.svg": "Web & Mobile",
}

SECTION_CONFIG = [
    ("core", "Core product icons"),
    ("category", "Product category icons"),
]


def get_label(filename):
    return LABEL_MAP.get(filename, filename)


def find_icons(directory):
    dir_path = Path(directory)
    return sorted([f.name for f in dir_path.glob("*.svg")])


def build_gallery_section(title, directory, files, url_prefix):
    items = []
    for f in files:
        label = get_label(f)
        rel_path = f"{Path(directory).name}/{f}"
        img_src = html.escape(rel_path)
        copy_url = html.escape(url_prefix + rel_path)

        items.append(f'''
        <div class="item" onclick="copyToClipboard('{copy_url}')">
            <img src="{img_src}" alt="{html.escape(label)}">
            <div class="label">{html.escape(label)}</div>
        </div>
        ''')

    return f"""
<h2>{html.escape(title)}</h2>
<div class="gallery">
    {"".join(items)}
</div>
"""


def build_html(sections):
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Icon Gallery</title>

<style>
    body {{
        font-family: sans-serif;
        padding: 20px;
        background: #fafafa;
    }}
    h2 {{
        margin-top: 40px;
        margin-bottom: 20px;
    }}
    .gallery {{
        display: flex;
        flex-wrap: wrap;
        gap: 20px;
    }}
    .item {{
        width: 100px;
        text-align: center;
        cursor: pointer;
        user-select: none;
        transition: transform 0.2s ease;
    }}
    .item:hover {{
        transform: translateY(-2px);
    }}
    .item img {{
        width: 64px;
        height: 64px;
        object-fit: contain;
    }}
    .label {{
        margin-top: 6px;
        font-size: 0.9em;
        color: #444;
        overflow-wrap: anywhere;
    }}
    .toast {{
        position: fixed;
        bottom: 20px;
        right: 20px;
        background: #333;
        color: white;
        padding: 12px 20px;
        border-radius: 4px;
        opacity: 0;
        transition: opacity 0.3s ease-in-out;
        pointer-events: none;
        font-size: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }}
    .toast.show {{
        opacity: 1;
    }}
</style>

<script>
function showToast(message) {{
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 2000);
}}

function copyToClipboard(url) {{
    navigator.clipboard.writeText(url)
        .then(() => showToast('Copied to clipboard!'))
        .catch(() => showToast('Failed to copy'));
}}
</script>

</head>
<body>

<p>
  Click icons to copy their absolute URL.
  PNG versions also available.
  Google source <a href="https://cloud.google.com/icons">here</a>.
</p>

{"".join(sections)}

<div id="toast" class="toast"></div>

</body>
</html>
"""


def main():
    parser = argparse.ArgumentParser(description="Generate icon gallery HTML")
    parser.add_argument(
        "--url-prefix",
        required=True,
        help="URL prefix for icon links (e.g., https://example.com/icons/)",
    )
    parser.add_argument(
        "--top-dir",
        default="_site",
        help="Top-level directory containing icon subdirectories (default: _site)",
    )
    parser.add_argument(
        "--output", help="Output HTML file path (default: TOP_DIR/index.html)"
    )
    args = parser.parse_args()

    url_prefix = args.url_prefix
    top_dir = Path(args.top_dir)
    output_path = Path(args.output) if args.output else top_dir / "index.html"

    sections = []
    for dir_name, title in SECTION_CONFIG:
        section_dir = top_dir / dir_name
        svg_files = find_icons(section_dir)
        if svg_files:
            sections.append(
                build_gallery_section(title, section_dir, svg_files, url_prefix)
            )

    html_output = build_html(sections)
    output_path.write_text(html_output)

    return 0


if __name__ == "__main__":
    sys.exit(main())
