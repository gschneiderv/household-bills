import os
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.http import MediaIoBaseDownload

# Provide the path to your service account key JSON file
SERVICE_ACCOUNT_FILE = 'bills-390910-64d970a32421.json'

# Scopes for accessing Google Drive
SCOPES = ['https://www.googleapis.com/auth/drive.readonly']

# ID of the folder to fetch files from
FOLDER_ID = 'ticket_compras'

# Destination folder to save downloaded files
DESTINATION_FOLDER = 'household-bills/tickets'

def fetch_files_from_drive():
    # Authenticate and create a Drive API service client
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    # Fetch files from the specified folder
    results = drive_service.files().list().execute()

    files = results.get('files', [])
    tickets_text = [google_file for google_file in results.get('files', []) if google_file['mimeType'] == 'application/vnd.google-apps.document']

    if not tickets_text:
        print('No tickets found.')
    else:
        print('Downloading tickets...')
        for ticket in tickets_text:
            file_directory = 
            file_id = ticket['id']
            file_name = f"{ticket['name']}.txt"
            file_path = os.path.join(DESTINATION_FOLDER, file_name)

            request = drive_service.files().export_media(fileId=file_id, mimeType='text/plain')
            fh = open(file_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False

            while not done:
                status, done = downloader.next_chunk()
                print(f"Downloading {file_name} - {int(status.progress() * 100)}%")

            print(f"{file_name} downloaded successfully.")

        print(f"Download completed. Total number of tickets {len(tickets_text)}")
