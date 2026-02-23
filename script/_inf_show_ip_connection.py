import psutil
import csv
from pathlib import Path

PATH_DATA = Path(__file__).resolve().parent.parent / "data"
PATH_WHITE_MASTER = PATH_DATA / "ip-white-master.csv"

# Hardcoded excludes that don't necessarily need to be in the CSV
DEFAULT_EXCLUDE = {"0.0.0.0", "1.1.1.1", "8.8.8.8", "9.9.9.9", "127.0.0.1", "::1"}

def load_white_list():
    """
    Load IP -> Reason mapping from ip-white-list-master.csv
    """
    ip_reason = {}

    with PATH_WHITE_MASTER.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ip_reason[row["IP"]] = row["Reason"]

    return ip_reason


def show_established_connections():
    ip_reason = load_white_list()

    # print(f"{'PID':>6}  {'Process':<20}  {'Remote IP':<15}  {'Port':>5}  Reason")
    print(f"Reason, {'Remote IP':<15}")
    print("-" * 80)

    for conn in psutil.net_connections(kind="tcp"):
        if conn.status != psutil.CONN_ESTABLISHED:
            continue

        if not conn.raddr:
            continue
        
        if conn.raddr.ip in DEFAULT_EXCLUDE:
            continue

        pid = conn.pid or "-"
        ip = conn.raddr.ip
        port = conn.raddr.port

        try:
            proc_name = psutil.Process(conn.pid).name() if conn.pid else "-"
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            proc_name = "?"

        reason = ip_reason.get(ip, "-")

        # print(
        #     f"{str(pid):>6}  "
        #     f"{proc_name:<20.20}  "
        #     f"{ip:<15}  "
        #     f"{port:>5}  "
        #     f"{reason}"
        # )
        print(
            f"{reason},"
            f"{ip:<15}"
        )


if __name__ == "__main__":
    show_established_connections()
