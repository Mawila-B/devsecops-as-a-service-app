from jinja2 import Environment, FileSystemLoader
import os
from ..config import settings
from ..utils.ai_summary import generate_ai_summary

def generate_report(scan_id: str, findings: dict, options: dict):
    env = Environment(loader=FileSystemLoader("/app/reports/templates/jinja"))
    template = env.get_template("report_template.html")
    
    ai_summary = None
    if settings.enable_ai_summary:
        ai_summary = generate_ai_summary(findings)
    
    html = template.render(
        scan_id=scan_id,
        findings=findings,
        target=options.get("target", "Unknown"),
        ai_summary=ai_summary
    )
    
    output_path = f"/app/reports/dist/{scan_id}.html"
    with open(output_path, "w") as f:
        f.write(html)
    
    return output_path