import subprocess
import json
from ...config import settings
from ...utils.logging import logger

def run(target: str) -> dict:
    try:
        # Run tfsec scan
        cmd = [
            "tfsec",
            target,
            "--format=json",
            "--no-color"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0 and result.returncode != 1:
            raise RuntimeError(result.stderr)
            
        # Parse results
        return json.loads(result.stdout) if result.stdout else {}
    except Exception as e:
        logger.error(f"TFSec scan failed: {str(e)}")
        return {"error": str(e)}