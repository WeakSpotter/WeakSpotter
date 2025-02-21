from app.executor.linear_executor import LinearExecutor
from fastapi import APIRouter
from sqlmodel import SQLModel

router = APIRouter()


class JobInfo(SQLModel):
    name: str
    license_name: str
    license_url: str
    license_gpl_compatible: bool


@router.get("/info/", tags=["info"], response_model=dict[str, list[JobInfo]])
def read_info():
    scan_features = {"simple": [], "complex": []}

    for key, value in scan_features.items():
        scan_features[key] = []
        for job in LinearExecutor(key).get_jobs():
            scan_features[key].append(
                JobInfo(
                    name=job.name,
                    license_name=job.license.value.name,
                    license_url=job.license.value.url,
                    license_gpl_compatible=job.license.value.gpl_compatible,
                )
            )

    return scan_features
