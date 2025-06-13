from fastapi import APIRouter
import datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "invoice-processor",
        "timestamp": datetime.datetime.now().isoformat()
    }
