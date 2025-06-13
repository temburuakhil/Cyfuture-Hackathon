from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "gst-assistant",
        "timestamp": datetime.datetime.now().isoformat()
    }
