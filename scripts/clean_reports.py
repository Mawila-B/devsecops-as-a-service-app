import os
import time
from datetime import datetime, timedelta

REPORTS_DIR = "/app/reports/dist"

def clean_old_reports(days=7):
    now = time.time()
    cutoff = now - (days * 86400)
    
    for filename in os.listdir(REPORTS_DIR):
        file_path = os.path.join(REPORTS_DIR, filename)
        if os.path.isfile(file_path):
            file_time = os.path.getmtime(file_path)
            if file_time < cutoff:
                os.remove(file_path)
                print(f"Removed: {filename}")

if __name__ == "__main__":
    clean_old_reports()
    print("Report cleanup completed")