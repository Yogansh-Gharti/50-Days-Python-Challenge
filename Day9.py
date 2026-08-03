import socket
import time
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm

SERVICES = {
    20: "FTP Data",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    8080: "HTTP Proxy"
}

results = []


def scan_port(host, port):
    try:
        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(0.5)

        status = sock.connect_ex((host, port))

        if status == 0:

            service = SERVICES.get(
                port,
                "Unknown"
            )

            results.append({
                "Port": port,
                "Service": service,
                "Status": "Open"
            })

        sock.close()

    except:
        pass


host = input("Enter Host/IP: ")

start_port = int(
    input("Start Port: ")
)

end_port = int(
    input("End Port: ")
)

start = time.time()

with ThreadPoolExecutor(max_workers=100) as executor:

    tasks = []

    for port in range(
        start_port,
        end_port + 1
    ):

        tasks.append(
            executor.submit(
                scan_port,
                host,
                port
            )
        )

    for task in tqdm(tasks):
        task.result()

end = time.time()

if results:

    df = pd.DataFrame(results)

    print(df)

    df.to_csv(
        "scan_report.csv",
        index=False
    )

    print("\nReport Saved: scan_report.csv")

else:

    print("\nNo Open Ports Found.")

print(
    f"\nScan Time: {round(end-start,2)} seconds"
)
