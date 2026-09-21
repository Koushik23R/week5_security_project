# Security Audit

## Scope

This audit compares the intentionally vulnerable implementation in
`vulnerable_version/app.py` with the hardened implementation in
`secure_version/app.py`. The audit covers authentication, model-backup
commands, session loading, and storage of credentials and API keys.

The automated checks are in `tests/test_security_exploits.py`. They verify
the three exploit paths and two valid secure-application paths described
below.

## Findings and remediation

| ID | Finding | Evidence in baseline | Remediation in secure version | Verification |
| --- | --- | --- | --- | --- |
| VULN-01 | SQL injection | `authenticate_user()` builds a SQL query by interpolating `username` and `password`. The payload `admin' --` bypasses the password condition. | Validates the username and uses a parameterized query with `?` placeholders. | Automated test passes: the payload succeeds in the baseline and fails in the secure version. |
| VULN-02 | OS command injection | `execute_system_backup()` passes user-controlled text to `os.system()`. Shell operators such as `;` can append commands. | Validates the backup tag against an allow-list and formats a log message without invoking a shell. | Automated test passes: the injection payload is accepted by the baseline and rejected by the secure version. |
| VULN-03 | Unsafe deserialization | `load_user_session()` calls `pickle.loads()` on a base64-decoded payload. A crafted pickle can execute code during loading. | Decodes the payload as UTF-8 JSON with `json.loads()`. | Automated test passes: the pickle payload loads in the baseline and is rejected by the secure version; a valid JSON session still loads. |
| OBS-01 | Plaintext credentials and API keys | The baseline database stores `admin123`, `student123`, and API keys directly in the `users` table. | The secure version stores SHA-256 password digests and Fernet-encrypted API keys. | Observed by source inspection. No separate automated test measures this storage change. |

## Before and after examples

### SQL injection

```python
# Baseline
query = f"SELECT role, api_key FROM users WHERE username = '{username}' AND password = '{password}'"
cursor.execute(query)

# Secure version
query = "SELECT password_hash, role, encrypted_api_key FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

### Command injection

```python
# Baseline
command = f"echo Backing up model metadata for tag: {backup_tag}"
os.system(command)

# Secure version
if not backup_tag or not re.match(r"^[a-zA-Z0-9_\-]{1,30}$", backup_tag):
    return {"status": "REJECTED", "error": "Invalid backup tag format. Only alphanumeric characters allowed."}
```

### Deserialization

```python
# Baseline
session_data = pickle.loads(base64.b64decode(session_payload_b64))

# Secure version
session_data = json.loads(
    base64.b64decode(session_payload_b64).decode("utf-8")
)
```

## Limitations and follow-up recommendations

- The secure version uses SHA-256 for passwords. A production system should
  use a password-specific, salted hash such as Argon2id, scrypt, or bcrypt.
- The Fernet key is generated when `SecureVaultApp` starts and is not
  persisted or loaded from a protected key store. Existing encrypted values
  therefore cannot be decrypted after a restart.
- The secure implementation catches broad exceptions in a few application
  methods. Production code should log diagnostic details securely while
  returning generic errors to callers.
- The included tests demonstrate the intended exploit behavior; they are not
  a complete penetration test or a guarantee that the application is secure
  in every deployment.

## Reproduction

Run the baseline exploit demonstration:

```bash
python -m security_audit.audit_runner
```

Run the automated checks:

```bash
python -m unittest discover -s tests -v
```
