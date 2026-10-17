import time
from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from patas_backend.database import get_db

router = APIRouter(tags=["Monitoring"])

START_TIME = time.time()


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check(
    response: Response,
    db: Annotated[AsyncSession, Depends(get_db)],
):
    uptime_seconds = int(time.time() - START_TIME)
    try:
        await db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception as e:
        db_status = f"unhealthy: {e!s}"
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    is_healthy = response.status_code == status.HTTP_200_OK
    return {
        "status": "healthy" if is_healthy else "degraded",
        "uptime_seconds": uptime_seconds,
        "checks": {
            "api": "ok",
            "database": db_status,
        },
    }
