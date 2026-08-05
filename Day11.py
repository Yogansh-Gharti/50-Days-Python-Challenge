import os
import time
import hashlib
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

FILE_HASHES = {}


def calculate_hash(file_path):
    try:
        sha = hashlib.sha256()

        with open(file_path, "rb") as file:

            while chunk := file.read(4096):
                sha.update(chunk)

        return sha.hexdigest()

    except:
        return None


def write_log(message):

    timestamp = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    log = f"[{timestamp}] {message}"

    print(log)

    with open(
        "integrity_log.txt",
        "a"
    ) as file:

        file.write(log + "\n")


class Monitor(FileSystemEventHandler):

    def on_created(self, event):

        if event.is_directory:
            return

        hash_value = calculate_hash(
            event.src_path
        )

        FILE_HASHES[event.src_path] = hash_value

        write_log(
            f"File Created: {event.src_path}"
        )

    def on_deleted(self, event):

        if event.is_directory:
            return

        FILE_HASHES.pop(
            event.src_path,
            None
        )

        write_log(
            f"File Deleted: {event.src_path}"
        )

    def on_modified(self, event):

        if event.is_directory:
            return

        new_hash = calculate_hash(
            event.src_path
        )

        old_hash = FILE_HASHES.get(
            event.src_path
        )

        if new_hash != old_hash:

            FILE_HASHES[event.src_path] = new_hash

            write_log(
                f"File Modified: {event.src_path}"
            )


folder = input(
    "Enter Folder to Monitor: "
)

observer = Observer()

observer.schedule(
    Monitor(),
    folder,
    recursive=True
)

observer.start()

print("\nMonitoring Started...")
print("Press CTRL + C to Stop\n")

try:

    while True:
        time.sleep(1)

except KeyboardInterrupt:

    observer.stop()

observer.join()
