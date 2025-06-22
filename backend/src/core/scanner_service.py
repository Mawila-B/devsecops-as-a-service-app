import subprocess
import json
import os
from .report_service import generate_report
from ..scanners import zap_adapter, tfsec_adapter, gitleaks_adapter, trivy_adapter
from ..config import settings
from ..utils.logging import logger

class ScannerService:
    def run_scan(self, scan_id: str, target: str, scan_type: str, options: dict):
        try:
            results = {}
            # Run appropriate scanners
            if scan_type in ["web", "full"]:
                results["zap"] = zap_adapter.run(target)
            
            if scan_type in ["infra", "full"]:
                results["tfsec"] = tfsec_adapter.run(target)
                results["gitleaks"] = gitleaks_adapter.run(target)
            
            if scan_type in ["container", "full"]:
                results["trivy"] = trivy_adapter.run(target)
            
            # Generate report
            generate_report(scan_id, results, options)
            
        except Exception as e:
            logger.error(f"Scan {scan_id} failed: {str(e)}")
            # Generate error report
            generate_report(scan_id, {"error": str(e)}, options)

    def _run_command(self, cmd: list, timeout: int = 600):
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout
        )
        if result.returncode != 0:
            raise RuntimeError(result.stderr.decode("utf-8"))
        return result.stdout.decode("utf-8")