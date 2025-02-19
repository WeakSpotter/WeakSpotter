import os

from fastapi import APIRouter

router = APIRouter()


def get_version():
    return os.getenv("COMMIT_HASH", "unknown")


@router.get("/version/", tags=["version"])
def read_version():
    return {"version": get_version()}
