import sqlite3
import re
import json
import base64
import hashlib
from cryptography.fernet import Fernet


class SecureVaultApp:
    """Hardened secure application implementing defense-in-depth measures."""

    def __init__(self, db_path="secure_vault.db"):
        self.db_path = db_path
        # Generate or initialize encryption key
        self.encryption_key = Fernet.generate_key()
        self.cipher = Fernet(self.encryption_key)
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
                           TEXT
                           UNIQUE,
                           password_hash
                           TEXT,
                           role
                           TEXT,
                           encrypted_api_key
                           TEXT
                       )
                       """)
        cursor.execute("DELETE FROM users")

        # Hardening: Hash passwords with SHA-256 and encrypt API keys using Fernet
        admin_pass_hash = hashlib.sha256("admin123".encode()).hexdigest()
        enc_admin_key = self.cipher.encrypt("SECURE_API_KEY_SECRET_99".encode()).decode()

        # Hardening: Parameterized INSERT query
        cursor.execute(
            "INSERT INTO users (username, password_hash, role, encrypted_api_key) VALUES (?, ?, ?, ?)",
            ('admin', admin_pass_hash, 'admin', enc_admin_key)
        )
        conn.commit()
        conn.close()

    def authenticate_user(self, username, password):
        """Hardening 1: Parameterized SQL query + Password Hash verification + Error masking."""
        # Hardening: Input validation on username
        if not username or not re.match(r"^[a-zA-Z0-9_]{3,30}$", username):
            return {"status": "FAILED", "error": "Invalid username format."}

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Hardening: Safe parameterized query prevents SQL Injection completely
        query = "SELECT password_hash, role, encrypted_api_key FROM users WHERE username = ?"

        try:
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            conn.close()

            if result:
                stored_hash, role, enc_api_key = result
                input_pass_hash = hashlib.sha256(password.encode()).hexdigest()

                if stored_hash == input_pass_hash:
                    # Decrypt API key on-demand for authenticated session
                    decrypted_key = self.cipher.decrypt(enc_api_key.encode()).decode()
                    return {"status": "SUCCESS", "role": role, "api_key": decrypted_key}

            # Hardening: Generic error message to prevent user enumeration
            return {"status": "FAILED", "error": "Invalid credentials."}
        except Exception:
            conn.close()
            # Hardening: Mask internal raw exceptions to prevent data leakage
            return {"status": "ERROR", "error": "An internal system error occurred."}

    def execute_system_backup(self, backup_tag):
        """Hardening 2: Strict input regex whitelisting preventing Command Injection."""
        # Hardening: Enforce strict alphanumeric tag validation
        if not backup_tag or not re.match(r"^[a-zA-Z0-9_\-]{1,30}$", backup_tag):
            return {"status": "REJECTED", "error": "Invalid backup tag format. Only alphanumeric characters allowed."}

        # Safe log formatting without subshell execution
        message = f"Backing up model metadata for tag: {backup_tag}"
        return {"status": "COMPLETED", "log": message}

    def load_user_session(self, session_payload_b64):
        """Hardening 3: Safe JSON deserialization replacing dangerous pickle loads."""
        try:
            raw_bytes = base64.b64decode(session_payload_b64)
            # Hardening: JSON parsing prevents arbitrary code execution
            session_data = json.loads(raw_bytes.decode('utf-8'))
            return {"status": "SUCCESS", "session": session_data}
        except Exception:
            return {"status": "REJECTED", "error": "Invalid or untrusted session payload structure."}