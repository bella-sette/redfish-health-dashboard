def analyze_server_data(data: dict) -> dict:
    """
    Analyze Redfish data and generate issues + recommendations.
    
    Fully implements the requested rules:
    - Secure Boot disabled → HIGH issue
    - Critical SEL logs → HIGH issue  
    - Warnings (system or SEL) → MEDIUM issue
    - No issues → Clean healthy state
    """
    issues = []
    recommendations = []
    seen_recs = set()

    system_health = data.get("system_health", {})
    secure_boot = data.get("secure_boot", {})
    sel_logs = data.get("sel_logs", [])

    # === System Health ===
    health = system_health.get("health", "Unknown")

    if health == "Critical":
        issues.append({
            "type": "system_health",
            "severity": "HIGH",
            "message": "Overall system health is critical."
        })
        rec = "Investigate hardware issues immediately using iDRAC."
        if rec not in seen_recs:
            recommendations.append(rec)
            seen_recs.add(rec)

    elif health == "Warning":
        issues.append({
            "type": "system_health",
            "severity": "MEDIUM",
            "message": "Overall system health reports warnings."
        })
        rec = "Review system health warnings and address affected components."
        if rec not in seen_recs:
            recommendations.append(rec)
            seen_recs.add(rec)

    # === Secure Boot ===
    if not secure_boot.get("enabled", False):
        issues.append({
            "type": "secure_boot",
            "severity": "HIGH",
            "message": "Secure Boot is disabled."
        })
        rec = "Enable Secure Boot in BIOS/iDRAC to improve boot security."
        if rec not in seen_recs:
            recommendations.append(rec)
            seen_recs.add(rec)

    # === SEL Logs ===
    for log in sel_logs:
        severity = log.get("severity", "OK")
        message = log.get("message", "No message provided.")

        if severity == "Critical":
            issues.append({
                "type": "sel_log",
                "severity": "HIGH",
                "message": f"Critical SEL event: {message}"
            })
            rec = "Review critical SEL events and resolve underlying hardware problems."
            if rec not in seen_recs:
                recommendations.append(rec)
                seen_recs.add(rec)

        elif severity == "Warning":
            issues.append({
                "type": "sel_log",
                "severity": "MEDIUM",
                "message": f"Warning SEL event: {message}"
            })
            rec = "Review warning SEL events to prevent future failures."
            if rec not in seen_recs:
                recommendations.append(rec)
                seen_recs.add(rec)

    # === Healthy System Case ===
    if not issues:
        recommendations.append("System is operating normally. Continue regular monitoring.")

    return {
        "issues": issues,
        "recommendations": recommendations,
    }