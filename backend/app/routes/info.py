from app.executor.linear_executor import LinearExecutor
from fastapi import APIRouter

router = APIRouter()


@router.get("/info/", tags=["info"], response_model=dict[str, list[str]])
def read_info():
    scan_features = {"simple": [], "complex": []}

    for key, value in scan_features.items():
        scan_features[key] = LinearExecutor(key).get_jobs()

    return scan_features
