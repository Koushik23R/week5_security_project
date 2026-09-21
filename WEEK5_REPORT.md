# Week 5 Security Hardening Report

**Student:** Koushik R
**Project:** AI/ML Model Vault and Certification Gateway
**Language:** Python
**Test framework:** Python `unittest`

## Objective

The project audits an intentionally vulnerable Python application and compares
it with a hardened implementation. The work demonstrates how unsafe SQL
construction, shell execution, and object deserialization can be exploited and
how each path can be reduced with safer input handling and APIs.

## Repository deliverables

| Path | Purpose |
| --- | --- |
| `vulnerable_version/app.py` | Baseline application with intentional security weaknesses |
| `secure_version/app.py` | Hardened comparison implementation |
| `security_audit/audit_runner.py` | Manual exploit demonstration for the baseline |
| `tests/test_security_exploits.py` | Five automated comparisons and valid-use checks |
| `docs/SECURITY_AUDIT.md` | Detailed findings, evidence, remediation, and limitations |
| `docs/TEST_RESULTS.md` | Captured output from the test run |

## Findings

1. **SQL injection:** The baseline interpolates credentials into a SQL
   statement. The secure version validates the username and uses a
   parameterized query.
2. **Command injection:** The baseline passes a user-controlled backup tag to
   `os.system()`. The secure version accepts only a restricted tag format and
   does not invoke a shell.
3. **Unsafe deserialization:** The baseline loads untrusted data with
   `pickle.loads()`. The secure version accepts JSON instead.
4. **Plaintext storage observation:** The baseline stores credentials and API
   keys directly in SQLite. The secure version replaces these with password
   digests and encrypted API keys. This storage change is documented but is
   not covered by a dedicated automated test.

## Verification

The test suite contains five tests:

- SQL injection is successful in the baseline and rejected by the secure
  version.
- A command-injection payload is accepted by the baseline and rejected by the
  secure version.
- A crafted pickle payload is loaded by the baseline and rejected by the
  secure version.
- Valid secure authentication succeeds.
- Valid JSON session data succeeds.

Run the suite with:

```bash
python -m unittest discover -s tests -v
```

The captured result in `docs/TEST_RESULTS.md` reports **5 tests passed**.
The audit runner can be executed separately with:

```bash
python -m security_audit.audit_runner
```

## Conclusion

The secure implementation blocks the three exploit scenarios covered by the
automated tests while preserving the tested valid authentication and JSON
session flows. It should be treated as a teaching example, not a
production-ready security design. In particular, production password storage
should use a password-specific hash such as Argon2id, scrypt, or bcrypt, and
the Fernet key should be managed through a persistent protected key store.
