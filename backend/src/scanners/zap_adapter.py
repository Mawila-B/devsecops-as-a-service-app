import requests
import time
from ...config import settings

def run(target: str) -> dict:
    # Start ZAP scan
    scan_url = f"{settings.zap_proxy}/JSON/ascan/action/scan/"
    params = {
        "apikey": settings.zap_api_key,
        "url": target,
        "recurse": True,
        "inScopeOnly": True
    }
    response = requests.get(scan_url, params=params)
    response.raise_for_status()
    scan_id = response.json()["scan"]
    
    # Poll for completion
    while True:
        status_url = f"{settings.zap_proxy}/JSON/ascan/view/status/"
        status = requests.get(status_url, params={"apikey": settings.zap_api_key}).json()["status"]
        if int(status) >= 100:
            break
        time.sleep(5)
    
    # Retrieve results
    alerts_url = f"{settings.zap_proxy}/JSON/core/view/alerts/"
    alerts = requests.get(
        alerts_url, 
        params={"apikey": settings.zap_api_key, "baseurl": target}
    ).json()["alerts"]
    
    return {
        "scan_id": scan_id,
        "alerts": [{"risk": a["risk"], "name": a["name"]} for a in alerts]
    }