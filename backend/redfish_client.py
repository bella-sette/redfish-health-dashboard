"""
Redfish Client - Mock Version with Multiple Scenarios
"""

def get_system_health(ip: str, username: str, password: str, scenario: str = "mixed") -> dict:
    scenarios = {
        "healthy":  {"state": "Enabled", "health": "OK", "health_rollup": "OK"},
        "warning":  {"state": "Enabled", "health": "Warning", "health_rollup": "Warning"},
        "critical": {"state": "Enabled", "health": "Critical", "health_rollup": "Critical"},
        "mixed":    {"state": "Enabled", "health": "Warning", "health_rollup": "Warning"}
    }
    return scenarios.get(scenario.lower(), scenarios["mixed"])


def get_secure_boot_status(ip: str, username: str, password: str, scenario: str = "mixed") -> dict:
    scenarios = {
        "healthy":  {"enabled": True, "mode": "UserMode"},
        "warning":  {"enabled": True, "mode": "UserMode"},
        "critical": {"enabled": False, "mode": "UserMode"},
        "mixed":    {"enabled": False, "mode": "UserMode"}
    }
    return scenarios.get(scenario.lower(), scenarios["mixed"])


def get_sel_logs(ip: str, username: str, password: str, scenario: str = "mixed") -> list[dict]:
    scenarios = {
        "healthy": [
            {"severity": "OK", "message": "System operating normally", "created": "2026-04-15T10:00:00Z"}
        ],
        "warning": [
            {"severity": "Warning", "message": "CPU temperature exceeded recommended threshold", "created": "2026-04-15T10:15:00Z"},
            {"severity": "OK", "message": "System boot completed", "created": "2026-04-15T09:00:00Z"}
        ],
        "critical": [
            {"severity": "Critical", "message": "Power supply redundancy lost", "created": "2026-04-15T10:23:45Z"},
            {"severity": "Critical", "message": "Fan failure in zone 2", "created": "2026-04-15T10:20:10Z"}
        ],
        "mixed": [
            {"severity": "Critical", "message": "Power supply redundancy lost", "created": "2026-04-15T10:23:45Z"},
            {"severity": "Warning", "message": "CPU temperature exceeded recommended threshold", "created": "2026-04-15T10:15:12Z"},
            {"severity": "OK", "message": "System boot completed successfully", "created": "2026-04-15T09:00:00Z"}
        ]
    }
    return scenarios.get(scenario.lower(), scenarios["mixed"])