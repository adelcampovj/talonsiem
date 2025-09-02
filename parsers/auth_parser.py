import re

def parse_auth_line(line):
    pattern = re.compile(
        r'(?P<timestamp>\w+ \d+ \d+:\d+:\d+).*sshd.*(Failed|Accepted) password for (invalid user )?(?P<username>\w+) from (?P<ip>[\d.]+)'
    )

    match = pattern.search(line)
    if match:
        return {
            "timestamp": match.group("timestamp"),
            "username": match.group("username"),
            "host": match.group("ip"),
            "success": "Accepted" in line,
            "raw": line.strip()
        }
    return None