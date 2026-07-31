import os
import shutil
import hashlib
from datetime import datetime

def file_hash(path):
    sha = hashlib.sha256()

    with open(path, "rb") as file:
        while chunk := file.read(4096):
            sha.update(chunk)

    return sha.hexdigest()


def sync_folders(source, backup):

    if not os.path.exists(backup):
        os.makedirs(backup)

    copied = 0
    updated = 0

    for root, dirs, files in os.walk(source):

        relative = os.path.relpath(root, source)

        backup_root = os.path.join(backup, relative)

        os.makedirs(backup_root, exist_ok=True)

        for file in files:

            src_file = os.path.join(root, file)

            dst_file = os.path.join(backup_root, file)

            if not os.path.exists(dst_file):

                shutil.copy2(src_file, dst_file)

                copied += 1

            else:

                if file_hash(src_file) != file_hash(dst_file):

                    shutil.copy2(src_file, dst_file)

                    updated += 1

    with open("backup_log.txt", "a") as log:

        log.write(
            f"{datetime.now()} | Copied:{copied} Updated:{updated}\n"
        )

    print("\n========== BACKUP COMPLETE ==========")

    print(f"New Files Copied : {copied}")

    print(f"Files Updated    : {updated}")

    print("Backup Log Saved")


source = input("Enter Source Folder: ")

backup = input("Enter Backup Folder: ")

sync_folders(source, backup)
