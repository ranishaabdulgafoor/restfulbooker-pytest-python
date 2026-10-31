import os
import logging
from datetime import datetime

# Ensure log output directories exist automatically
os.makedirs("reports", exist_ok=True)

def log_failure_transaction(test_name, response, request_payload=None):
    """Captures explicit network details on assertion failure to serve as diagnostic artifacts."""
    log_filename = f"reports/FAILURE_{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    with open(log_filename, "w", encoding="utf-8") as f:
        f.write(f"=== RECREATION REPORT: FAILURE INTERCEPTED INSIDE [{test_name}] ===\n")
        f.write(f"Timestamp: {datetime.now().isoformat()}\n")
        f.write(f"Target Endpoint URL: {response.url}\n")
        f.write(f"HTTP Method Request: {response.request.method}\n")
        f.write(f"Server Status Code Returned: {response.status_code}\n\n")

        f.write("--- OUTBOUND HEADERS SENT ---\n")
        f.write(f"{dict(response.request.headers)}\n\n")

        if request_payload:
            f.write("--- OUTBOUND PAYLOAD BODY MAILED ---\n")
            f.write(f"{request_payload}\n\n")

        f.write("--- INBOUND SERVER RESPONSE BODY RECEIVED ---\n")
        f.write(f"{response.text}\n")
        f.write("=====================================================================\n")
    print(f"\n[ARTIFACT GENERATED] Network pipeline log captured at: {log_filename}")
