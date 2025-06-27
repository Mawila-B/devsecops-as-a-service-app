from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
from scan_runner import run_all_scans
from report_generator import generate_report
from utils.helpers import save_upload_file
from utils.alerts import send_slack_alert, send_jira_issue

app = FastAPI(title="DevSecOps as a Service API")

# Allow CORS from frontend origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update to your frontend domain in production
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory setup
UPLOAD_DIR = "uploads"
REPORT_DIR = "reports/outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)


@app.post("/api/scan")
async def scan_code(
    repo_url: str = Form(None),
    file: UploadFile = File(None),
):
    """
    Trigger security scans on uploaded code or Git repo URL.
    Provide either repo_url or a zip file upload.
    """

    if not repo_url and not file:
        raise HTTPException(status_code=400, detail="Must provide repo_url or upload a zip file.")

    # Unique ID per scan
    scan_id = str(uuid.uuid4())

    # Save uploaded file if present
    local_path = None
    if file:
        filename = f"{scan_id}_{file.filename}"
        local_path = os.path.join(UPLOAD_DIR, filename)
        await save_upload_file(file, local_path)

    # Run scans: takes repo_url or local_path, saves output under reports/outputs/{scan_id}/
    try:
        output_dir = os.path.join(REPORT_DIR, scan_id)
        os.makedirs(output_dir, exist_ok=True)

        # Run scan runner returns dict of tool results paths
        results = run_all_scans(repo_url=repo_url, local_path=local_path, output_dir=output_dir)

        # Generate report (HTML) path
        report_path = generate_report(scan_id, results, output_dir)

        # Send alerts (Slack, Jira) with scan summary
        send_slack_alert(scan_id, results)
        send_jira_issue(scan_id, results)

        return {"scan_id": scan_id, "report_url": f"/api/report/{scan_id}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


@app.get("/api/report/{scan_id}")
def get_report(scan_id: str):
    """
    Serve the HTML report for a given scan_id.
    """
    report_path = os.path.join(REPORT_DIR, scan_id, "report.html")
    if not os.path.isfile(report_path):
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(report_path, media_type="text/html")


@app.get("/health")
def health():
    return {"status": "ok"}
