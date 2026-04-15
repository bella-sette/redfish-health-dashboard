# Redfish Health Dashboard

Interactive full-stack dashboard that simulates and visualizes Redfish/iDRAC server health, including health scoring, risk classification, and actionable remediation insights.

## Overview

This project simulates infrastructure health monitoring using a FastAPI backend and a responsive HTML/CSS/JavaScript frontend. It allows users to run mock server scans and view a health score, risk level, detected issues, and recommended actions.

## Screenshot

![Dashboard](assets/dashboard.png)

## Features

- FastAPI backend with `/scan` endpoint
- Scenario-based mock scans (healthy, warning, mixed, critical)
- Health scoring and risk classification
- Detection of system issues with actionable remediation recommendations
- Dynamic dashboard UI with animated updates

## Example Output

- Health Score: 72%
- Risk Level: Medium
- Issues Detected:
  - High CPU temperature
  - Warning system status
- Recommended Actions:
  - Check cooling system
  - Review system logs

## Tech Stack

- Python (FastAPI)
- HTML
- CSS
- JavaScript

## Run Locally

### Backend

```bash
cd backend
pip install -r requirements.txt

# Windows
py -m uvicorn app:app --reload

# Mac/Linux
python3 -m uvicorn app:app --reload

```

### Frontend

Open `frontend/index.html` using **VS Code Live Server**.

> In VS Code: right-click `index.html` → "Open with Live Server"
