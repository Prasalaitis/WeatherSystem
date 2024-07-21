from config import LoggerSetup, db_config
import os
import subprocess
from datetime import datetime
import time
from typing import List


class DatabaseBackup:
    """Handling of database backup operations using PostgreSQL's pg_dump utility."""

    def __init__(self) -> None:
        """
        Initializes the DatabaseBackup instance with configuration from db_config
        and sets up logging and backup file path.
        """
        self.logger = LoggerSetup(
            "DatabaseBackup", "logging", f"backup.log"
        ).logger
        self.host: str = db_config["host"]
        self.port: str = db_config["port"]
        self.user: str = db_config["user"]
        self.password: str = db_config["password"]
        self.database: str = db_config["database"]

        self.backup_file_path: str = ""
        self.setup_backup_path()

    def setup_backup_path(self) -> None:
        """
        The path for storing backup files relative to the script's location.
        Ensures that the backup directory exists.
        """
        script_dir = os.path.dirname(os.path.realpath(__file__))
        backup_dir = os.path.join(script_dir, "..", "backups")
        os.makedirs(backup_dir, exist_ok=True)
        self.backup_file_path = os.path.join(
            backup_dir,
            f"fullbackups_{datetime.now().strftime('%Y-%m-%d')}.sql",
        )

    def run_command(self, command: List[str]):
        """
        Executes a shell command using subprocess and captures its output.

        Args:
            command (List[str]): The command to be executed as a list of strings.
        """
        start_time = time.time()
        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )
        stdout, stderr = process.communicate()
        end_time = time.time()
        duration = end_time - start_time
        return process.returncode, stdout, stderr, duration

    def full_backup(self) -> None:
        """
        Performs a full backup of the configured database using the pg_dump command.
        Logs the outcome and any errors encountered during the backup process.
        """
        command = [
            "pg_dump",
            "-h",
            self.host,
            "-p",
            self.port,
            "-U",
            self.user,
            "--data-only",
            "-f",
            self.backup_file_path,
            self.database,
        ]
        self.logger.info("Performing full backup...")
        os.environ["PGPASSWORD"] = self.password
        returncode, stdout, stderr, duration = self.run_command(command)
        os.environ.pop("PGPASSWORD", None)

        if returncode == 0:
            self.logger.info(
                f"Backup successful. Total time: {duration:.2f} seconds"
            )
            if os.path.exists(self.backup_file_path):
                file_size = os.path.getsize(self.backup_file_path)
                self.logger.info(
                    f"Backup file '{self.backup_file_path}' created, size: {file_size} bytes"
                )
            else:
                self.logger.error(
                    f"Backup file '{self.backup_file_path}' not found after successful backup."
                )
        else:
            self.logger.error(
                f"Backup failed with return code {returncode}. Errors: {stderr.strip()}"
            )


if __name__ == "__main__":
    backup = DatabaseBackup()
    backup.full_backup()
