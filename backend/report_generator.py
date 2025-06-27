import json
import os
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = "reports/templates"
OUTPUT_HTML = "report.html"

def generate_report(scan_id, scan_results, output_dir):
    """
    Read raw scan JSON files, parse important info,
    render an HTML report using Jinja2 templates.
    Returns the path to the generated HTML file.
    """

    # Load JSON results
    tfsec_data = _load_json(scan_results.get("tfsec"))
    trivy_data = _load_json(scan_results.get("trivy"))
    gitleaks_data = _load_json(scan_results.get("gitleaks"))

    # Summarize findings for report
    summary = {
        "tfsec": len(tfsec_data.get("results", [])) if tfsec_data else 0,
        "trivy": len(trivy_data) if trivy_data else 0,
        "gitleaks": len(gitleaks_data.get("Leaks", [])) if gitleaks_data else 0,
    }

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("report.html")

    report_html = template.render(
        scan_id=scan_id,
        summary=summary,
        tfsec=tfsec_data,
        trivy=trivy_data,
        gitleaks=gitleaks_data,
    )

    output_path = os.path.join(output_dir, OUTPUT_HTML)
    with open(output_path, "w") as f:
        f.write(report_html)

    return output_path


def _load_json(path):
    if not path or not os.path.isfile(path):
        return None
    with open(path, "r") as f:
        try:
            return json.load(f)
        except Exception:
            return None
