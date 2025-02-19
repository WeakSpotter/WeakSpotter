from datetime import datetime, timedelta

from app.database import SessionDep
from app.executor.linear_executor import LinearExecutor
from app.models.scan import Scan, ScanRead, ScanType
from app.routes.version import get_version
from app.scoring.calculator import calculate_score
from app.security import UserDep
from fastapi import APIRouter, BackgroundTasks
from fastapi.exceptions import HTTPException
from sqlmodel import select

router = APIRouter()


def get_scan_or_403(scan_id: int, session: SessionDep, current_user: UserDep) -> Scan:
    scan = session.get(Scan, scan_id)
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")

    if (
        scan.creator_id
        and scan.creator_id != current_user.id
        and current_user not in scan.users
    ):
        raise HTTPException(
            status_code=403, detail="Not authorized to access this scan"
        )
    return scan


@router.get("/scans/", tags=["scans"])
def read_scans(session: SessionDep, current_user: UserDep):
    # Get scans where user is either creator or has access
    scans = session.exec(
        select(Scan).where(
            (Scan.creator_id == current_user.id) | (Scan.users.any(id=current_user.id))
        )
    ).all()
    return scans


@router.get("/scans/{scan_id}", tags=["scans"])
def read_scan(scan_id: int, session: SessionDep, current_user: UserDep) -> ScanRead:
    scan = get_scan_or_403(scan_id, session, current_user)

    scan_read = ScanRead.model_validate(scan)
    scan_read.score = calculate_score(scan)

    return scan_read


@router.get("/scans/{scan_id}/data", tags=["scans"])
def read_scan_data(scan_id: int, session: SessionDep, current_user: UserDep) -> dict:
    scan = get_scan_or_403(scan_id, session, current_user)
    return scan.data_dict


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

    # Check if a recent scan with the same URL already exists and has been done in the last 1 hour
    recent_scan = session.exec(
        select(Scan).where(
            Scan.url == url, Scan.created_at > datetime.utcnow() - timedelta(hours=1)
        )
    ).first()

    print(f"Found recent scan: {recent_scan}")

    if recent_scan and get_version() != "dev":
        if (
            recent_scan.creator_id == current_user.id
            or current_user in recent_scan.users
        ):
            raise HTTPException(
                status_code=409,
                detail=f"You cannot scan the same URL again so soon, please wait {recent_scan.created_at + timedelta(hours=1) - datetime.utcnow()} seconds",
            )

        # Add user to the scan
        recent_scan.users.append(current_user)
        session.add(recent_scan)
        session.commit()
        return recent_scan

    scan = Scan(
        url=url,
        creator_id=current_user.id if current_user else None,
        type=ScanType.complex if complex else ScanType.simple,
    )

    if current_user:
        scan.users.append(current_user)  # Add creator as a user with access

    session.add(scan)
    session.commit()
    session.refresh(scan)

    scan_type = "complex" if complex else "simple"
    executor = LinearExecutor(scan_type)
    background_tasks.add_task(executor.run, scan, session)

    return scan


@router.delete("/scans/{scan_id}", tags=["scans"])
def delete_scan(scan_id: int, session: SessionDep, current_user: UserDep) -> dict:
    scan = get_scan_or_403(scan_id, session, current_user)

    if scan.creator_id and scan.creator_id != current_user.id:
        raise HTTPException(
            status_code=403, detail="Not authorized to delete this scan"
        )
    session.delete(scan)
    session.commit()
    return {"message": "Scan deleted"}
