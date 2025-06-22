from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from ..core.scanner_service import ScannerService
from ..utils.logging import logger

router = APIRouter()

class ScanRequest(BaseModel):
    target: str
    scan_type: str  # "web", "infra", "container", "full"
    options: dict = {}

@router.post("/scans/")
async def create_scan(request: ScanRequest, background_tasks: BackgroundTasks):
    scan_id = f"scan_{uuid.uuid4().hex[:8]}"
    try:
        scanner = ScannerService()
        background_tasks.add_task(
            scanner.run_scan,
            scan_id,
            request.target,
            request.scan_type,
            request.options
        )
        return {"scan_id": scan_id, "status": "queued"}
    except Exception as e:
        logger.error(f"Scan failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scans/{scan_id}")
async def get_scan_results(scan_id: str):
    # In production, use DB instead of file check
    report_path = f"/app/reports/dist/{scan_id}.html"
    if os.path.exists(report_path):
        return FileResponse(report_path)
    return {"status": "processing"}