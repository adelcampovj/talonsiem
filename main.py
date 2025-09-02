from storage.db import init_db, insert_attempt
from parsers.auth_parser import parse_auth_line
from utils.detectors import detect_brute_force
from utils.report_exporter import export_brute_force_alerts_to_csv

LOG_FILE = "logs/auth.log"

def prorcess_log_file():
    with open(LOG_FILE, "r") as f:
        for line in f:
            try:    
                parsed = parse_auth_line(line)
                if parsed:
                    insert_attempt(
                        timestamp=parsed["timestamp"],
                        host=parsed["host"],
                        username=parsed["username"],
                        success=parsed["success"],
                        raw=parsed["raw"]
                    )
                else:
                    print("Skipping unmatched line:", line.strip())
            except Exception as e:
                print(f"Error processing lines: {line.strip()}\nReason: {e}")

if __name__ == "__main__":
    init_db()
    prorcess_log_file()
    detect_brute_force()
    export_brute_force_alerts_to_csv()
    print("Log files has been successfully checked and saved.")