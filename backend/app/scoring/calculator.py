from app.models.scan import Scan

def calculate_score(scan: Scan) -> int:
    if "connectivity" not in scan.data_dict:
        return 0

    if scan.data_dict["connectivity"]["status"] == "down":
        return 0

    return 100
