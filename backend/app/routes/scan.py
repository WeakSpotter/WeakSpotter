from app.database import SessionDep
from app.executor.linear_executor import LinearExecutor
from app.models.scan import Scan
from app.scoring.calculator import calculate_score
from app.security import UserDep
from fastapi import APIRouter, BackgroundTasks
from fastapi.exceptions import HTTPException
from sqlmodel import select

router = APIRouter()


@router.get("/scans/", tags=["scans"])
def read_scans(session: SessionDep, current_user: UserDep):
    scans = session.exec(
        select(Scan).where((Scan.user_id == current_user.id) | (Scan.user_id.is_(None)))
    ).all()

    return scans


@router.get("/scans/{scan_id}", tags=["scans"])
def read_scan(scan_id: int, session: SessionDep, current_user: UserDep):
    scan = session.get(Scan, scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id and scan.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this scan"
        )
    return scan


@router.get("/scans/{scan_id}/data", tags=["scans"])
def read_scan_data(scan_id: int, session: SessionDep, current_user: UserDep) -> dict:
    scan = session.get(Scan, scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id and scan.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this scan"
        )
    return scan.data_dict


@router.get("/scans/{scan_id}/score", tags=["scans"])
def read_scan_score(scan_id: int, session: SessionDep, current_user: UserDep) -> int:
    scan = session.get(Scan, scan_id)
    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")
    if scan.user_id and scan.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to access this scan"
        )
    return calculate_score(scan)


@router.post("/scans/", tags=["scans"])
def create_scan(
    url: str,
    background_tasks: BackgroundTasks,
    session: SessionDep,
    current_user: UserDep,
    complex: bool = False,
) -> Scan:
    if complex and not current_user:
        raise HTTPException(
            status_code=403, detail="Authentication required for complex scan"
        )

    scan = Scan(url=url, user_id=current_user.id if current_user else None)
    session.add(scan)
    session.commit()
    session.refresh(scan)

    scan_type = "complex" if complex else "simple"
    executor = LinearExecutor(scan_type)
    background_tasks.add_task(executor.run, scan, session)

    return scan


@router.delete("/scans/{scan_id}", tags=["scans"])
def delete_scan(scan_id: int, session: SessionDep, current_user: UserDep) -> dict:
    scan = session.get(Scan, scan_id)
    if scan.user_id and scan.user_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this scan"
        )
    session.delete(scan)
    session.commit()
    return {"message": "Scan deleted"}
