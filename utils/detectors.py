import sqlite3
from datetime import datetime, timedelta
from config import THRESHOLD, WINDOW_SECONDS
from alerts.email_alerts import send_email_alert

DB_NAME ="talonsiem.db"

def detect_brute_force(threshold=THRESHOLD, window_seconds=WINDOW_SECONDS):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
        SELECT timestamp, host, username FROM login_attempts
        WHERE success = 0
    ''')
    rows = c.fetchall()
    conn.close()

    failed_logins = {}

    for row in rows:
        ts_str, ip, username = row
        ts = datetime.strptime(ts_str, "%b %d %H:%M:%S")
        ts = ts.replace(year=datetime.now().year)

        key = (ip, username)
        if key not in failed_logins:
            failed_logins[key] = []
        failed_logins[key].append(ts)

    for (ip, username), attempts in failed_logins.items():
        attempts.sort()
        for i in range(len(attempts) - threshold + 1):
            window = attempts[i + threshold - 1] - attempts[i]
            if window <= timedelta(seconds=window_seconds):
                print(f"Brute force alert: {threshold} failed logins from IP {ip} (user: {username}) within {window_seconds} seconds")
                insert_brute_force_alert(ip=ip, username=username, host=ip, attempts=threshold, window_seconds=window_seconds)
                break

    send_email_alert(
        subject="TalonSIEM Alert: Brute Force Detected",
        body=f"{threshold} failed logins from IP {ip} (user: {username}) within {window_seconds} seconds"
    )

def insert_brute_force_alert(ip, username, host, attempts, window_seconds):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO brute_force_alerts (timestamp, ip, username, host, attempts, window_seconds)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (timestamp, ip, username, host, attempts, window_seconds))
    conn.commit()
    conn.close()