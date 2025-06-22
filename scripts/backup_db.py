import os
import datetime
import subprocess
import boto3
from ..config import settings

def backup_database():
    """Create and upload database backup"""
    timestamp = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    backup_file = f"/backups/db_backup_{timestamp}.sql"
    
    # Create backup
    try:
        subprocess.run([
            "pg_dump",
            "-h", settings.db_host,
            "-U", settings.db_user,
            "-d", settings.db_name,
            "-f", backup_file
        ], check=True, env={"PGPASSWORD": settings.db_password})
    except subprocess.CalledProcessError as e:
        logger.error(f"Backup failed: {str(e)}")
        return False
    
    # Upload to S3
    if settings.backup_s3_bucket:
        try:
            s3 = boto3.client(
                's3',
                aws_access_key_id=settings.aws_access_key,
                aws_secret_access_key=settings.aws_secret_key
            )
            s3.upload_file(
                backup_file,
                settings.backup_s3_bucket,
                f"backups/{os.path.basename(backup_file)}"
            )
            logger.info(f"Backup uploaded to S3: {backup_file}")
        except Exception as e:
            logger.error(f"S3 upload failed: {str(e)}")
            return False
    
    # Local retention (keep last 7 backups)
    if settings.backup_local_retention > 0:
        backup_dir = os.path.dirname(backup_file)
        backups = sorted(
            [f for f in os.listdir(backup_dir) if f.startswith("db_backup_")],
            reverse=True
        )
        for old_backup in backups[settings.backup_local_retention:]:
            os.remove(os.path.join(backup_dir, old_backup))
    
    return True

if __name__ == "__main__":
    backup_database()