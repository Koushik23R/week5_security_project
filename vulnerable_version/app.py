import sqlite3
import os
import pickle
import base64


class VulnerableVaultApp:
    """Baseline application containing intentional security vulnerabilities."""

    def __init__(self, db_path="vulnerable_vault.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS users
                       (
                           id
                           INTEGER
                           PRIMARY
                           KEY
                           AUTOINCREMENT,
                           username
                           TEXT,
                           password
                           TEXT,
                           role
                           TEXT,
                           api_key
                           TEXT
                       )
                       """)
        cursor.execute("DELETE FROM users")
        # Hardcoded plaintext credentials and API keys
        cursor.execute(
            "INSERT INTO users (username, password, role, api_key) VALUES ('admin', 'admin123', 'admin', 'RAW_API_KEY_SECRET_99')")
        cursor.execute(
            "INSERT INTO users (username, password, role, api_key) VALUES ('student', 'student123', 'user', 'RAW_API_KEY_STUDENT_01')")
        conn.commit()
        conn.close()

    def authenticate_user(self, username, password):
        """Vulnerability 1: SQL Injection via raw string concatenation."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Unsafe query construction allowing SQLi (e.g. username = "admin' --")
        query = f"SELECT role, api_key FROM users WHERE username = '{username}' AND password = '{password}'"

        try:
            cursor.execute(query)
            result = cursor.fetchone()
            conn.close()
            if result:
                return {"status": "SUCCESS", "role": result[0], "api_key": result[1]}
            return {"status": "FAILED", "error": "Invalid credentials"}
        except Exception as e:
            conn.close()
            return {"status": "ERROR", "raw_exception": str(e)}

    def execute_system_backup(self, backup_tag):
        """Vulnerability 2: Command Injection via unsanitized input formatting."""
        # Unsafe command string allows appending commands using ';' or '&&'
        command = f"echo Backing up model metadata for tag: {backup_tag}"

        # Executing shell command directly
        exit_code = os.system(command)
        return {"status": "COMPLETED", "command_executed": command, "exit_code": exit_code}

    def load_user_session(self, session_payload_b64):
        """Vulnerability 4: Insecure Deserialization using Python pickle."""
        try:
            # Unsafe deserialization of untrusted user input
            raw_bytes = base64.b64decode(session_payload_b64)
            session_data = pickle.loads(raw_bytes)
            return {"status": "SUCCESS", "session": session_data}
        except Exception as e:
            return {"status": "ERROR", "raw_exception": str(e)}