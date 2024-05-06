from fastapi import APIRouter

router = APIRouter(tags=["main"])


@router.get("/")
async def description():
    return "labor-exchange API 1.0"
