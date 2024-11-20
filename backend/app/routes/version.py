import os

from fastapi import APIRouter

router = APIRouter()

@router.get("/version/")
def read_version():
    return {"version": os.getenv("COMMIT_HASH", "unknown")}
