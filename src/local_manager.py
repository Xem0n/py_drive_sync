import os
import time

class LocalManager:
    def __init__(self, file_path):
        self.__file_path = file_path
        self.__ignore_changes = False
        self.__last_mtime = None

    def watch(self, on_change):
        while True:
            try:
                mtime = os.path.getmtime(self.__file_path)

                if self.__last_mtime is None:
                    self.__last_mtime = mtime
                elif mtime > self.__last_mtime:
                    print(f"Local file changed")
                    on_change()
                    self.__last_mtime = mtime
            except FileNotFoundError:
                raise Exception(f"File not found: {self.__file_path}")

            time.sleep(1)

    def ignore_changes(self, should_ignore):
        self.__ignore_changes = should_ignore
        self.__last_mtime = None if should_ignore else os.path.getmtime(self.__file_path)
        print(f"Ignoring local changes: {should_ignore}")

