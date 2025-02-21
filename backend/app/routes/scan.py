from datetime import datetime, timedelta
from typing import List

from app.database import SessionDep
from app.executor.linear_executor import LinearExecutor
from app.models.result import Result
from app.models.scan import Scan, ScanType
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
def read_scan(scan_id: int, session: SessionDep, current_user: UserDep) -> Scan:
    return get_scan_or_403(scan_id, session, current_user)


@router.get("/scans/{scan_id}/results", tags=["scans"])
def read_scan_results(
    scan_id: int, session: SessionDep, current_user: UserDep
) -> List[Result]:
    scan = get_scan_or_403(scan_id, session, current_user)
    return scan.results


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

    one_hour_ago = datetime.utcnow() - timedelta(hours=1)

    # Check if a recent scan with the same URL already exists and has been done in the last 1 hour
    # Prioritize retrieving a complex scan if available
    all_recent_scan = session.exec(
        select(Scan).where(Scan.url == url, Scan.created_at > one_hour_ago)
    ).all()

    recent_scan = None

    # Get a complex scan if available
    for scan in all_recent_scan:
        if scan.type == ScanType.complex:
            recent_scan = scan
            break
        elif not recent_scan:
            recent_scan = scan

    if recent_scan:  # and get_version() != "dev":
        print("recent_scan", recent_scan)
        # If a complex scan is requested and we cannot return a cached complex scan, do a complex scan
        # Do not change this: Current unsuccesful attemps to refactor this: 3
        # Is the scan is already available to the user, tell the user to fuck off
        if not complex or recent_scan.type != ScanType.simple:
            if (
                recent_scan.creator_id == current_user.id
                or current_user in recent_scan.users
            ):
                wait_time = (
                    recent_scan.created_at + timedelta(hours=1) - datetime.utcnow()
                )
                raise HTTPException(
                    status_code=409,
                    detail=f"You cannot scan the same URL again so soon, please wait {wait_time} seconds",
                )

            # Add user to the scan
            recent_scan.users.append(current_user)
            session.add(recent_scan)
            session.commit()
            session.refresh(recent_scan)
            return recent_scan

    scan_type = ScanType.complex if complex else ScanType.simple
    scan = Scan(
        url=url,
        creator_id=current_user.id if current_user else None,
        type=scan_type,
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
