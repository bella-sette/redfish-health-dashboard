def score_analysis(analysis: dict) -> dict:
    """
    Calculate health score and risk level.

    - 100 = Perfect (no issues)
    - HIGH issue  -> -25 points
    - MEDIUM issue -> -10 points
    """
    issues = analysis.get("issues", [])
    recommendations = analysis.get("recommendations", [])

    # Healthy system (no issues)
    if not issues:
        risk_level = "LOW"
        summary = "System is healthy with no identified issues."
        return {
            "health_score": 100,
            "risk_level": risk_level,
            "summary": summary,
            "issues": [],
            "recommendations": recommendations or [
                "System is operating normally. Continue regular monitoring."
            ],
        }

    score = 100

    for issue in issues:
        severity = issue.get("severity", "MEDIUM")
        if severity == "HIGH":
            score -= 25
        elif severity == "MEDIUM":
            score -= 10

    score = max(score, 0)

    if score >= 90:
        risk_level = "LOW"
    elif score >= 60:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    if risk_level == "LOW":
        summary = "STATUS: NOMINAL — No issues detected across monitored components."
    elif risk_level == "MEDIUM":
        summary = f"System is at MEDIUM risk with {len(issues)} identified issues. Review recommended actions."
    else:
        summary = f"System is at HIGH risk due to critical failures. Immediate attention is recommended."   

    return {
        "health_score": score,
        "risk_level": risk_level,
        "summary": summary,
        "issues": issues,
        "recommendations": recommendations,
    }