from app.models.scan import Scan

def calculate_score(scan: Scan) -> int:
    if "http_status" not in scan.data_dict:
        return 0

    if scan.data_dict["http_status"]["status"] >= 400:
        return 0

    return 100
