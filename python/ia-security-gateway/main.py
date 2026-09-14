"""
IA Security Gateway - Main Application with Frontend
Local-first security funnel for AI workloads
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from datetime import datetime
from pathlib import Path

from app.core.config import settings
from app.api.routes import router
from app.services.traffic_control import TrafficController
from app.services.compliance import ComplianceLogger

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize services
traffic_controller = TrafficController()
compliance_logger = ComplianceLogger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("🚀 IA Security Gateway starting...")
    logger.info(f"📍 Local Ollama endpoint: {settings.OLLAMA_BASE_URL}")
    logger.info(f"🔐 Compliance logging: {'ENABLED' if settings.GDPR_ENABLED else 'DISABLED'}")
    logger.info("🚦 Traffic control: ENABLED")
    logger.info("🌐 Web Frontend: ENABLED (http://localhost:8000)")
    yield
    # Shutdown
    logger.info("🛑 IA Security Gateway shutting down...")

# Create FastAPI app with lifespan
app = FastAPI(
    title="IA Security Gateway",
    description="Local-first security funnel for AI workloads",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests and responses"""
    start_time = datetime.now()

    # Log incoming request
    compliance_logger.log_request(
        method=request.method,
        path=request.url.path,
        timestamp=start_time
    )

    try:
        response = await call_next(request)
        process_time = (datetime.now() - start_time).total_seconds() * 1000

        # Log response
        compliance_logger.log_response(
            status_code=response.status_code,
            process_time=process_time
        )

        return response
    except Exception as e:
        logger.error(f"Middleware error: {e}")
        compliance_logger.log_error("MIDDLEWARE_ERROR", 500, str(e))
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"}
        )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    compliance_logger.log_error("UNHANDLED_ERROR", 500, str(exc))
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )

# Include API routes
app.include_router(router)

# Root endpoint - serve frontend
@app.get("/", tags=["Frontend"])
async def root():
    """Serve the web frontend"""
    frontend_path = Path(__file__).parent.parent / "public" / "index.html"
    if frontend_path.exists():
        return FileResponse(frontend_path)
    else:
        return {
            "service": "IA Security Gateway",
            "status": "operational",
            "version": "1.0.0",
            "message": "Frontend not found. Place index.html in public/ folder",
            "api_docs": "http://localhost:8000/docs",
            "timestamp": datetime.now().isoformat()
        }

# Serve static files (CSS, JS, etc.)
public_path = Path(__file__).parent.parent / "public"
if public_path.exists():
    app.mount("/public", StaticFiles(directory=str(public_path)), name="public")

# Serve logs folder for log access
logs_path = Path(__file__).parent.parent / "logs"
if logs_path.exists():
    app.mount("/logs", StaticFiles(directory=str(logs_path)), name="logs")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.SERVER_HOST,
        port=settings.SERVER_PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
