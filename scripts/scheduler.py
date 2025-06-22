import time
import schedule
from .backup_db import backup_database
from .clean_reports import clean_old_reports
from .clean_logs import clean_old_logs
from ..utils.logging import logger

def run_scheduler():
    # Daily backup at 2 AM UTC
    schedule.every().day.at("02:00").do(backup_database)
    
    # Hourly cleanup
    schedule.every().hour.do(clean_old_reports)
    schedule.every(6).hours.do(clean_old_logs)
    
    logger.info("Scheduler started")
    
    while True:
        schedule.run_pending()
        time.sleep(60)