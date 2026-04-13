"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      REST API MODULE (FASTAPI)                              ║
║   Provides REST API interface for automated scanning and integration        ║
╚══════════════════════════════════════════════════════════════════════════════╝

Installation: pip install fastapi uvicorn pydantic

Usage:
    python api_server.py
    
Then access at: http://localhost:8000
Swagger UI: http://localhost:8000/docs
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl
from enum import Enum


# Pydantic Models for Request/Response Validation

class ScanModeEnum(str, Enum):
    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"
    STEALTH = "stealth"
    TARGETED = "targeted"


class PayloadProfileEnum(str, Enum):
    ALL = "all"
    WAF_BYPASS = "waf_bypass"
    POLYGLOT = "polyglot"
    DOM = "dom"
    BLIND = "blind"
    QUICK = "quick"


class ScanRequest(BaseModel):
    """Request model for initiating an XSS scan."""
    
    url: HttpUrl = Field(..., description="Target URL to scan")
    endpoint: Optional[str] = Field(None, description="Specific endpoint")
    known_param: Optional[str] = Field(None, description="Known parameter name")
    mode: ScanModeEnum = Field(ScanModeEnum.STANDARD, description="Scan intensity")
    profile: PayloadProfileEnum = Field(PayloadProfileEnum.ALL, description="Payload profile")
    depth: int = Field(2, ge=1, le=5, description="Crawl depth")
    threads: int = Field(5, ge=1, le=20, description="Concurrent threads")
    delay: float = Field(0.0, ge=0, description="Delay between requests")
    timeout: int = Field(10, ge=1, le=60, description="Request timeout")
    cookies: Optional[str] = Field(None, description="Session cookies")
    headers: Optional[Dict[str, str]] = Field(None, description="Custom headers")
    proxy: Optional[str] = Field(None, description="Proxy URL")
    blind_callback: Optional[str] = Field(None, description="Blind XSS callback")
    skip_headers: bool = Field(False, description="Skip header testing")
    test_dom: bool = Field(True, description="Test DOM sinks")
    verbose: bool = Field(False, description="Verbose output")


class Vulnerability(BaseModel):
    """Model for discovered vulnerability."""
    
    url: str
    parameter: str
    payload: str
    context: str
    method: str = "GET"
    severity: str = "HIGH"
    discovered_at: datetime


class ScanResult(BaseModel):
    """Model for scan results."""
    
    scan_id: str
    status: str  # "pending", "running", "completed", "failed"
    target_url: str
    mode: str
    profile: str
    start_time: datetime
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    vulnerabilities: List[Vulnerability] = Field(default_factory=list)
    metrics: Dict[str, Any] = Field(default_factory=dict)
    error: Optional[str] = None


class HealthStatus(BaseModel):
    """Health check response."""
    
    status: str
    version: str = "5.0"
    timestamp: datetime
    features: List[str] = Field(
        default_factory=lambda: [
            "web_crawling",
            "context_detection",
            "payload_generation",
            "waf_detection",
            "dom_analysis",
            "multi_threading",
            "report_export",
        ]
    )


# FastAPI Application Setup



def create_app():
    """Create and configure FastAPI application."""
    try:
        from fastapi import FastAPI, BackgroundTasks, HTTPException
        from fastapi.responses import JSONResponse
        import uuid
    except ImportError:
        raise ImportError(
            "FastAPI required. Install with: pip install fastapi uvicorn"
        )

    app = FastAPI(
        title="AutoXSS API",
        description="XSS Discovery Framework REST API",
        version="5.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json",
    )

    # In-memory scan storage (use database in production)
    active_scans: Dict[str, ScanResult] = {}
    scan_results: Dict[str, ScanResult] = {}

    
    # Health & Info Endpoints
    

    @app.get("/health", response_model=HealthStatus)
    async def health_check():
        """Health check endpoint."""
        return HealthStatus(status="healthy", timestamp=datetime.now())

    @app.get("/info")
    async def info():
        """Get API information."""
        return {
            "name": "AutoXSS API",
            "version": "5.0",
            "author": "R0b3rt0",
            "modes": ["quick", "standard", "deep", "stealth", "targeted"],
            "profiles": ["all", "waf_bypass", "polyglot", "dom", "blind", "quick"],
            "endpoints": [
                "/health",
                "/info",
                "/scan (POST)",
                "/scan/{scan_id} (GET)",
                "/scan/{scan_id}/results (GET)",
                "/scans/active (GET)",
            ],
        }

    # Scan Endpoints

    @app.post("/scan", response_model=Dict[str, str])
    async def start_scan(
        request: ScanRequest,
        background_tasks: BackgroundTasks,
    ):
        """
        Start a new XSS scan.
        
        Returns scan ID for status tracking.
        """
        scan_id = str(uuid.uuid4())
        
        # Create scan result record
        scan_result = ScanResult(
            scan_id=scan_id,
            status="queued",
            target_url=str(request.url),
            mode=request.mode.value,
            profile=request.profile.value,
            start_time=datetime.now(),
            vulnerabilities=[],
            metrics={}
        )
        
        active_scans[scan_id] = scan_result
        
        # Queue scan in background
        background_tasks.add_task(
            _run_scan,
            scan_id=scan_id,
            request=request,
            active_scans=active_scans,
            scan_results=scan_results,
        )
        
        return {
            "scan_id": scan_id,
            "status": "queued",
            "message": "Scan queued. Use /scan/{scan_id} to check status."
        }

    @app.get("/scan/{scan_id}", response_model=ScanResult)
    async def get_scan_status(scan_id: str):
        """Get current scan status."""
        if scan_id in active_scans:
            return active_scans[scan_id]
        elif scan_id in scan_results:
            return scan_results[scan_id]
        else:
            raise HTTPException(status_code=404, detail=f"Scan {scan_id} not found")

    @app.get("/scan/{scan_id}/results")
    async def get_scan_results(scan_id: str):
        """Get detailed scan results."""
        if scan_id in scan_results:
            return scan_results[scan_id]
        elif scan_id in active_scans and active_scans[scan_id].status == "completed":
            return active_scans[scan_id]
        else:
            raise HTTPException(status_code=404, detail=f"Results not found")

    @app.get("/scans/active")
    async def list_active_scans():
        """List all active scans."""
        return {
            "active_scans": len(active_scans),
            "completed_scans": len(scan_results),
            "scans": [
                {"scan_id": sid, "status": scan.status, "target": scan.target_url}
                for sid, scan in active_scans.items()
            ]
        }

    # Background task

    async def _run_scan(
        scan_id: str,
        request: ScanRequest,
        active_scans: Dict,
        scan_results: Dict,
    ):
        """Run scan in background (placeholder)."""
        try:
            scan = active_scans[scan_id]
            scan.status = "running"
            
            # TODO: Implement actual scanning logic here
            # For now, this is a placeholder
            
            scan.status = "completed"
            scan.end_time = datetime.now()
            scan.duration_seconds = (
                scan.end_time - scan.start_time
            ).total_seconds()
            
            scan_results[scan_id] = scan
            del active_scans[scan_id]
            
        except Exception as e:
            scan = active_scans[scan_id]
            scan.status = "failed"
            scan.error = str(e)
            scan.end_time = datetime.now()
            scan_results[scan_id] = scan
            del active_scans[scan_id]

    return app


# Server Entry Point


if __name__ == "__main__":
    import uvicorn
    
    app = create_app()
    
    print("""
    ╔════════════════════════════════════════════════════════════════╗
    ║          AutoXSS REST API Server                              ║
    ╠════════════════════════════════════════════════════════════════╣
    ║  Starting server on http://localhost:8000                  ║
    ║  Documentation: http://localhost:8000/docs                 ║
    ║  Swagger UI: http://localhost:8000/redoc                  ║
    ║  Hot reload enabled (dev mode)                             ║
    ╚════════════════════════════════════════════════════════════════╝
    """)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes
        access_log=True,
    )
