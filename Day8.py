from scapy.all import ARP, Ether, srp
import socket
import pandas as pd

network = input(
    "Enter Network (Example: 192.168.1.0/24): "
)

print("\nScanning Network...\n")

arp = ARP(pdst=network)

ether = Ether(dst="ff:ff:ff:ff:ff:ff")

packet = ether / arp

result = srp(
    packet,
    timeout=2,
    verbose=False
)[0]

devices = []

for sent, received in result:

    ip = received.psrc

    mac = received.hwsrc

    try:
        hostname = socket.gethostbyaddr(ip)[0]
    except:
        hostname = "Unknown"

    devices.append({
        "IP Address": ip,
        "MAC Address": mac,
        "Hostname": hostname
    })

if devices:

    df = pd.DataFrame(devices)

    print(df)

    df.to_csv(
        "scan_report.csv",
        index=False
    )

    print("\n✅ Report Saved as scan_report.csv")

else:

    print("No Devices Found.")
