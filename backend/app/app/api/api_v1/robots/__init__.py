from fastapi import APIRouter
from app.api.api_v1.robots import search

router = APIRouter()
router.include_router(search.router, prefix="/robots", tags=["robots"])
