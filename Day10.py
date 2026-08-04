from scapy.all import sniff, wrpcap, IP, TCP, UDP, ICMP
import pandas as pd

packets = []
report = []


def analyze(packet):

    if IP not in packet:
        return

    protocol = "Other"

    if TCP in packet:
        protocol = "TCP"

    elif UDP in packet:
        protocol = "UDP"

    elif ICMP in packet:
        protocol = "ICMP"

    src = packet[IP].src
    dst = packet[IP].dst
    length = len(packet)

    print(
        f"{protocol:5} | {src:15} -> {dst:15} | {length} Bytes"
    )

    packets.append(packet)

    report.append({
        "Protocol": protocol,
        "Source": src,
        "Destination": dst,
        "Packet Size": length
    })


print("===== MINI WIRESHARK =====")
print("Capturing 25 packets...\n")

sniff(
    prn=analyze,
    count=25,
    store=False
)

wrpcap(
    "captured_packets.pcap",
    packets
)

df = pd.DataFrame(report)

df.to_csv(
    "traffic_report.csv",
    index=False
)

print("\n========== SUMMARY ==========")

print(df["Protocol"].value_counts())

print("\n✅ Packets Saved: captured_packets.pcap")
print("✅ Report Saved : traffic_report.csv")
