import os
import hashlib
import pandas as pd


def get_hash(file_path):
    sha = hashlib.sha256()

    try:
        with open(file_path, "rb") as file:
            while chunk := file.read(4096):
                sha.update(chunk)

        return sha.hexdigest()

    except:
        return None


folder = input("Enter Folder Path: ")

hashes = {}
duplicates = []

for root, dirs, files in os.walk(folder):

    for file in files:

        path = os.path.join(root, file)

        file_hash = get_hash(path)

        if file_hash is None:
            continue

        size = os.path.getsize(path)

        if file_hash in hashes:

            duplicates.append({
                "Duplicate File": path,
                "Original File": hashes[file_hash],
                "Size (KB)": round(size / 1024, 2)
            })

        else:

            hashes[file_hash] = path

if duplicates:

    df = pd.DataFrame(duplicates)

    df.to_csv(
        "duplicate_report.csv",
        index=False
    )

    total_size = df["Size (KB)"].sum()

    print("\n========= DUPLICATE REPORT =========")

    print(f"Duplicate Files : {len(df)}")

    print(f"Recoverable Space : {round(total_size/1024,2)} MB")

    print("\nReport Saved: duplicate_report.csv")

else:

    print("\nNo Duplicate Files Found.")
