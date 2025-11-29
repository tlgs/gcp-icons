# /// script
# requires-python = ">=3.9"
# dependencies = [ "jinja2" ]
# ///

"""Generate HTML index page for GCP icon galleries.

Creates an interactive HTML gallery displaying SVG icons from configured
directories using Jinja2 templates. Icons are organized by section (core
products and categories) with click-to-copy URL functionality.
"""

import argparse
from pathlib import Path
from typing import Final, NamedTuple

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape


class IconItem(NamedTuple):
    url: str
    img_src: str
    label: str


class Section(NamedTuple):
    title: str
    items: list[IconItem]


LABEL_MAP: Final[dict[str, str]] = {
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

SECTION_CONFIG: Final[list[tuple[str, str]]] = [
    ("core", "Core product icons"),
    ("category", "Product category icons"),
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate icon gallery HTML")
    parser.add_argument("--url-prefix", required=True, help="URL prefix for icon links")
    parser.add_argument("--top-dir", required=True, help="Top-level directory")
    args = parser.parse_args()

    url_prefix = (
        args.url_prefix if args.url_prefix.endswith("/") else args.url_prefix + "/"
    )

    top_dir = Path(args.top_dir)
    output_path = top_dir / "index.html"

    # set up Jinja2 environment
    env = Environment(
        loader=FileSystemLoader("templates/"),
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
        undefined=StrictUndefined,
    )
    template = env.get_template("index.html.j2")

    # build data structure for template
    sections = []
    for dir_name, title in SECTION_CONFIG:
        section_dir = top_dir / dir_name
        items = []
        for f in sorted(f.name for f in section_dir.glob("*.svg")):
            label = LABEL_MAP.get(f, f)
            img_src = f"{dir_name}/{f}"
            copy_url = f"{url_prefix}{dir_name}/{f}"
            items.append(IconItem(url=copy_url, img_src=img_src, label=label))
        sections.append(Section(title=title, items=items))

    # Render template and write output
    html_output = template.render(sections=sections)
    output_path.write_text(html_output, encoding="utf-8")


if __name__ == "__main__":
    main()
