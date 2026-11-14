import time
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from patas_backend.database import get_db

router = APIRouter(tags=["Monitoring"])

START_TIME = time.time()
# Global variables to cache the database check
LAST_DB_CHECK_TIME = 0.0
LAST_DB_STATUS = "unchecked"
DB_CHECK_INTERVAL = 3600  # 1 hour in seconds

@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    global LAST_DB_CHECK_TIME, LAST_DB_STATUS
    uptime_seconds = int(time.time() - START_TIME)
    current_time = time.time()

    # Only actually ping the database if 1 hour has passed
    if current_time - LAST_DB_CHECK_TIME >= DB_CHECK_INTERVAL:
        try:
            await db.execute(text("SELECT 1"))
            LAST_DB_STATUS = "connected"
            LAST_DB_CHECK_TIME = current_time
        except Exception as e:
            LAST_DB_STATUS = f"unhealthy: {e!s}"
            LAST_DB_CHECK_TIME = current_time  # Still update time so we don't spam a broken DB
    
    # If the last known status was bad, fail the health check
    if "unhealthy" in LAST_DB_STATUS:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    is_healthy = response.status_code == status.HTTP_200_OK
    return {
        "status": "healthy" if is_healthy else "degraded",
        "uptime_seconds": uptime_seconds,
        "checks": {
            "api": "ok",
            "database": LAST_DB_STATUS,
            "next_db_check_in_seconds": int(DB_CHECK_INTERVAL - (current_time - LAST_DB_CHECK_TIME))
        },
    }