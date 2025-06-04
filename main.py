import argparse
import threading
from src.local_manager import LocalManager
from src.drive_manager import DriveManager

def main():
    parser = argparse.ArgumentParser(description="Sync local and Google Drive file.")
    parser.add_argument("local_file", type=str, help="Path to the local file")
    parser.add_argument("drive_file", type=str, help="Path to the file on Google Drive")
    args = parser.parse_args()

    print(f"Local file: {args.local_file}")
    print(f"Drive file: {args.drive_file}")

    local_manager = LocalManager(args.local_file)
    drive_manager = DriveManager(args.drive_file)

    # make sure the local file is up to date
    drive_manager.download(args.local_file)

    def run_local_watch():
        local_manager.watch(lambda: (
            drive_manager.ignore_changes(True),
            drive_manager.upload(args.local_file),
            drive_manager.ignore_changes(False)
        ))

    def run_drive_watch():
        drive_manager.watch(lambda: (
            local_manager.ignore_changes(True),
            drive_manager.download(args.local_file),
            local_manager.ignore_changes(False)
        ))

    t1 = threading.Thread(target=run_local_watch, daemon=True)
    t2 = threading.Thread(target=run_drive_watch, daemon=True)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
