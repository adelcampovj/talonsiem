import sqlite3
import csv

DB_NAME = "talonsiem.db"

def export_brute_force_alerts_to_csv(filename="brute_force_report.csv"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM brute_force_alerts")
    rows = c.fetchall()

    headers = [description[0] for description in c.description]

    with open(filename, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(rows)

    conn.close()
    print(f"Alerts exported to CSV: {filename}")
