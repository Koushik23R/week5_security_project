# AI/ML Model Vault & Certification Gateway (Security Hardening Suite)

A comprehensive Python security engineering project demonstrating OWASP Top 10 vulnerability identification, exploit simulation, and defense-in-depth code hardening.

---

## Quick Deliverables & Evidence Index

| Deliverable                  | File Location                                                          | Description                                                                                             |
| ---------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| **Primary Project Report**   | [`WEEK5_REPORT.md`](./WEEK5_REPORT.md)                                 | Comprehensive root report for evaluation                                                                |
| **Security Audit Matrix**    | [`docs/SECURITY_AUDIT.md`](./docs/SECURITY_AUDIT.md)                   | OWASP vulnerability details and before/after code                                                       |
| **Test Results**             | [`docs/TEST_RESULTS.md`](./docs/TEST_RESULTS.md)                       | Automated test execution results                                                                        |
| **Vulnerable Baseline Code** | [`vulnerable_version/app.py`](./vulnerable_version/app.py)             | Baseline SQL Injection, Command Injection, Pickle deserialization, and plaintext secret vulnerabilities |
| **Hardened Secure Code**     | [`secure_version/app.py`](./secure_version/app.py)                     | Parameterized SQL, input validation, Fernet encryption, JSON parsing, and masked errors                 |
| **Exploit Audit Runner**     | [`security_audit/audit_runner.py`](./security_audit/audit_runner.py)   | Security exploit simulation script                                                                      |
| **Automated Test Suite**     | [`tests/test_security_exploits.py`](./tests/test_security_exploits.py) | `unittest` suite verifying security defenses                                                            |
| **Word Report**              | [`report.docx`](./report.docx)                                         | Formal project report                                                                                   |

---

## Repository Structure

```text
week5_security_project/
├── WEEK5_REPORT.md
├── README.md
├── requirements.txt
├── report.docx
├── .gitignore
│
├── vulnerable_version/
│   ├── __init__.py
│   └── app.py
│
├── secure_version/
│   ├── __init__.py
│   └── app.py
│
├── security_audit/
│   ├── __init__.py
│   └── audit_runner.py
│
├── tests/
│   ├── __init__.py
│   └── test_security_exploits.py
│
└── docs/
    ├── SECURITY_AUDIT.md
    └── TEST_RESULTS.md
```

---

## Security Vulnerabilities Demonstrated

The vulnerable baseline demonstrates the following security weaknesses:

* SQL Injection
* OS Command Injection
* Insecure Pickle Deserialization
* Plaintext Credentials and API Keys

The secure implementation addresses these issues using:

* Parameterized SQL queries
* Regex-based input validation
* JSON-based data parsing
* Fernet encryption
* Generic error messages to prevent sensitive information disclosure

---

## Running the Security Tests

Install the required dependency:

```bash
pip install -r requirements.txt
```

Run the complete automated security test suite:

```bash
python -m unittest discover -s tests -v
```

### Expected Result

```text
Ran 5 tests in 0.308s

OK
```

---

## Project Purpose

This project demonstrates the complete security-hardening workflow:

**Identify → Exploit → Fix → Test → Document**

It provides both vulnerable and hardened implementations along with automated security tests and supporting audit documentation for evaluation.
