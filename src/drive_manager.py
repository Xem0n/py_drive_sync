from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account
import time

class DriveManager:
    SERVICE_SCOPES = [
        # todo: set better scopes
        'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/drive.metadata.readonly',
        'https://www.googleapis.com/auth/drive.readonly',
    ]

    def __init__(self, file_id, credentials_file):
        self.__file_id = file_id
        self.__credential_file = credentials_file
        self.__last_modified_time = None
        self.__ignore_changes = False

        creds = service_account.Credentials.from_service_account_file(
            self.__credential_file, scopes=self.SERVICE_SCOPES)
        self.__service = build('drive', 'v3', credentials=creds)

    def watch(self, on_change):
        # accessing same service on multiple threads is not safe, so we create a new service instance
        creds = service_account.Credentials.from_service_account_file(
            self.__credential_file, scopes=['https://www.googleapis.com/auth/drive.metadata.readonly'])
        service = build('drive', 'v3', credentials=creds)
        self.__last_modified_time = None

        while True:
            try:
                file = service.files().get(fileId=self.__file_id, fields='modifiedTime').execute()
                modified_time = file['modifiedTime']

                if self.__last_modified_time is None:
                    self.__last_modified_time = modified_time
                elif modified_time > self.__last_modified_time:
                    print(f"Drive file changed: {self.__file_id}")
                    on_change()
                    self.__last_modified_time = modified_time
            except Exception as e:
                raise Exception(f"Error watching Drive file: {e}")

            time.sleep(1)

    def upload(self, local_file_path):
        media = MediaFileUpload(local_file_path, resumable=True)
        file = self.__service.files().update(fileId=self.__file_id, media_body=media, fields='id').execute()
        print(f"File uploaded: {file.get('id')}")

    def download(self, local_file_path):
        request = self.__service.files().get_media(fileId=self.__file_id)
        fh = open(local_file_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)

        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f"Download {int(status.progress() * 100)}%.")

        fh.close()
        print(f"File downloaded to: {local_file_path}")

    def ignore_changes(self, should_ignore):
        self.__ignore_changes = should_ignore
        self.__last_modified_time = None if should_ignore else None
        print(f"Ignoring drive changes: {should_ignore}")
