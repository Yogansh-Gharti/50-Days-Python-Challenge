import sqlite3
import qrcode
import cv2
from pyzbar.pyzbar import decode
from datetime import datetime
import os

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect("history.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
id INTEGER PRIMARY KEY AUTOINCREMENT,
data TEXT,
time TEXT
)
""")

conn.commit()


def generate_qr():

    text = input("Enter Text/URL: ")

    img = qrcode.make(text)

    img.save("output/qr_code.png")

    print("\n✅ QR Code Saved as output/qr_code.png")


def scan_image():

    path = input("Enter Image Path: ")

    image = cv2.imread(path)

    if image is None:
        print("Image Not Found!")
        return

    codes = decode(image)

    if not codes:
        print("No QR/Barcode Found.")
        return

    for code in codes:

        data = code.data.decode()

        print("\nDetected:", data)

        cursor.execute(
            "INSERT INTO history(data,time) VALUES(?,?)",
            (data, datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
        )

    conn.commit()


def webcam_scan():

    cap = cv2.VideoCapture(0)

    print("Press Q to Exit")

    while True:

        ret, frame = cap.read()

        codes = decode(frame)

        for code in codes:

            data = code.data.decode()

            print("Detected:", data)

            cursor.execute(
                "INSERT INTO history(data,time) VALUES(?,?)",
                (data, datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
            )

            conn.commit()

        cv2.imshow("Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()

    cv2.destroyAllWindows()


while True:

    print("\n===== QR & BARCODE TOOL =====")

    print("1.Generate QR")
    print("2.Scan Image")
    print("3.Scan Webcam")
    print("4.Exit")

    choice = input("Choice: ")

    if choice == "1":
        generate_qr()

    elif choice == "2":
        scan_image()

    elif choice == "3":
        webcam_scan()

    elif choice == "4":
        break

    else:
        print("Invalid Choice")

conn.close()
