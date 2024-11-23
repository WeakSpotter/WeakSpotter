from app.database import SessionDep
from app.jobs import complex_scan, simple_scan
from app.models.scan import Scan
from app.scoring.calculator import calculate_score
from fastapi import APIRouter, BackgroundTasks
from fastapi.exceptions import HTTPException
from sqlmodel import select

router = APIRouter()


@router.get("/scans/", tags=["scans"])
def read_scans(session: SessionDep, offset: int = 0, limit: int = 100):
    scans = session.exec(select(Scan).offset(offset).limit(limit)).all()
    return scans


@router.get("/scans/{scan_id}", tags=["scans"])
def read_scan(scan_id: int, session: SessionDep):
    return session.get(Scan, scan_id)


@router.get("/scans/{scan_id}/data", tags=["scans"])
def read_scan_data(scan_id: int, session: SessionDep) -> dict:
    scan: Scan | None = session.get(Scan, scan_id)

    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")

    return scan.data_dict


@router.get("/scans/{scan_id}/score", tags=["scans"])
def read_scan_score(scan_id: int, session: SessionDep) -> int:
    scan: Scan | None = session.get(Scan, scan_id)

    if scan is None:
        raise HTTPException(status_code=404, detail="Scan not found")

    return calculate_score(scan)


@router.post("/scans/", tags=["scans"])
def create_scan(
    url: str,
    background_tasks: BackgroundTasks,
    session: SessionDep,
    complex: bool = False,
) -> Scan:
    scan = Scan(url=url)
    session.add(scan)
    session.commit()
    session.refresh(scan)

    scanner = complex_scan if complex else simple_scan
    background_tasks.add_task(scanner.scan, scan, session)

    return scan


@router.delete("/scans/{scan_id}", tags=["scans"])
def delete_scan(scan_id: int, session: SessionDep) -> dict:
    scan = session.get(Scan, scan_id)
    session.delete(scan)
    session.commit()
    return {"message": "Scan deleted"}
