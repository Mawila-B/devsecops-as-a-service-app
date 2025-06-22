import subprocess
import threading
import queue
import time
import os
import json
import signal
from .report_service import generate_report
from .notification_service import send_notification
from ..scanners import zap_adapter, tfsec_adapter, gitleaks_adapter, trivy_adapter
from ..config import settings
from ..utils.logging import logger
from ..core.database import SessionLocal
from ..core.models import Scan

# Timeout configuration per scanner (seconds)
SCANNER_TIMEOUTS = {
    "zap": 1800,     # 30 minutes
    "tfsec": 600,    # 10 minutes
    "gitleaks": 900, # 15 minutes
    "trivy": 1200    # 20 minutes
}

# Priority scanning queue
scan_queue = queue.PriorityQueue()
MAX_CONCURRENT_SCANS = settings.max_concurrent_scans or 5

class ScannerService:
    def __init__(self):
        # Start worker threads
        for i in range(MAX_CONCURRENT_SCANS):
            worker = threading.Thread(target=self._scan_worker)
            worker.daemon = True
            worker.start()

    def run_scan(self, scan_id: str, target: str, scan_type: str, options: dict, priority: int):
        scan_queue.put((priority, (scan_id, target, scan_type, options)))
        logger.info(f"Scan {scan_id} added to queue with priority {priority}")

    def _scan_worker(self):
        while True:
            priority, (scan_id, target, scan_type, options) = scan_queue.get()
            db = SessionLocal()
            try:
                scan = db.query(Scan).filter(Scan.id == scan_id).first()
                if not scan:
                    logger.error(f"Scan {scan_id} not found in database")
                    continue
                
                scan.status = "processing"
                db.commit()
                
                logger.info(f"Starting scan {scan_id} for {target}")
                results = {}
                
                # Run scanners based on type with individual timeouts
                try:
                    if scan_type in ["web", "full"]:
                        results["zap"] = self._run_with_timeout(
                            zap_adapter.run, 
                            [target], 
                            SCANNER_TIMEOUTS["zap"]
                        )
                    
                    if scan_type in ["infra", "full"]:
                        results["tfsec"] = self._run_with_timeout(
                            tfsec_adapter.run, 
                            [target], 
                            SCANNER_TIMEOUTS["tfsec"]
                        )
                        results["gitleaks"] = self._run_with_timeout(
                            gitleaks_adapter.run, 
                            [target], 
                            SCANNER_TIMEOUTS["gitleaks"]
                        )
                    
                    if scan_type in ["container", "full"]:
                        results["trivy"] = self._run_with_timeout(
                            trivy_adapter.run, 
                            [target], 
                            SCANNER_TIMEOUTS["trivy"]
                        )
                except TimeoutError as e:
                    scan.status = "failed"
                    scan.error = f"Scan timed out: {str(e)}"
                    db.commit()
                    logger.error(f"Scan {scan_id} timed out")
                    continue
                
                # Generate report
                report_path = generate_report(scan_id, results, options)
                
                # Update scan status
                scan.status = "completed"
                scan.report_path = report_path
                scan.completed_at = datetime.utcnow()
                db.commit()
                
                # Send notification
                user = db.query(User).filter(User.id == scan.user_id).first()
                if user:
                    send_notification(
                        user.email,
                        "Scan Completed",
                        f"Your security scan for {target} is complete",
                        report_path
                    )
                
                logger.info(f"Scan {scan_id} completed successfully")
                
            except Exception as e:
                logger.error(f"Scan {scan_id} failed: {str(e)}")
                if scan:
                    scan.status = "failed"
                    scan.error = str(e)
                    db.commit()
            finally:
                db.close()
                scan_queue.task_done()
                time.sleep(1)  # Brief pause between scans

    def _run_with_timeout(self, func, args, timeout):
        """Run a function with timeout handling"""
        class TimeoutException(Exception):
            pass
        
        def handler(signum, frame):
            raise TimeoutException(f"Operation timed out after {timeout} seconds")
        
        # Set the timeout handler
        signal.signal(signal.SIGALRM, handler)
        signal.alarm(timeout)
        
        try:
            result = func(*args)
            signal.alarm(0)  # Cancel the alarm
            return result
        except TimeoutException as e:
            raise e
        finally:
            signal.alarm(0)  # Ensure alarm is always cleared

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