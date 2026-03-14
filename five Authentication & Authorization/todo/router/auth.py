from fastapi import APIRouter

router = APIRouter()

@router.get("/auth/")
def read_root():
    return {"user": "authenticated"}

