from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from redfish_client import get_system_health, get_secure_boot_status, get_sel_logs
from analyzer import analyze_server_data
from scorer import score_analysis

app = FastAPI(title="Dell Redfish Health Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScanRequest(BaseModel):
    ip: str
    username: str
    password: str


@app.get("/")
def root():
    return {"message": "Redfish Health Analyzer API is running"}


@app.post("/scan")
def scan_server(
    request: ScanRequest,
    scenario: str = Query("mixed")
):
    try:
        system_health = get_system_health(
            request.ip, request.username, request.password, scenario
        )
        secure_boot = get_secure_boot_status(
            request.ip, request.username, request.password, scenario
        )
        sel_logs = get_sel_logs(
            request.ip, request.username, request.password, scenario
        )

        collected_data = {
            "ip": request.ip,
            "system_health": system_health,
            "secure_boot": secure_boot,
            "sel_logs": sel_logs,
        }

        analysis = analyze_server_data(collected_data)
        result = score_analysis(analysis)

        return result

    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Server scan failed: {str(exc)}")
    