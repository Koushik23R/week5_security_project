# Week 5 Automated Security Test Results & Verification

## Environment Specifications
- **Python Version:** Python 3.13 / Standard Library + `cryptography`
- **Test Framework:** `unittest`
- **Execution Command:** `python -m unittest discover -s tests -v`

---

## Complete Terminal Execution Output

```text
test_command_injection_defense (test_security_exploits.TestSecurityHardening.test_command_injection_defense)
Verify Command Injection payload is executed in vulnerable app but blocked in secure app. ... ok
test_insecure_deserialization_defense (test_security_exploits.TestSecurityHardening.test_insecure_deserialization_defense)
Verify Pickle payload executes on vulnerable app but JSON parser blocks it on secure app. ... ok
test_secure_valid_authentication (test_security_exploits.TestSecurityHardening.test_secure_valid_authentication)
Verify legitimate user authentication works as expected in secure app. ... ok
test_secure_valid_json_session (test_security_exploits.TestSecurityHardening.test_secure_valid_json_session)
Verify legitimate JSON session loading works in secure app. ... ok
test_sql_injection_defense (test_security_exploits.TestSecurityHardening.test_sql_injection_defense)
Verify SQL Injection succeeds on vulnerable app but fails cleanly on secure app. ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.308s

OK