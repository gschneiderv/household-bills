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
DESTINATION_FOLDER = 'tickets'

def fetch_files_from_drive():
    # Authenticate and create a Drive API service client
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    # Fetch files from the specified folder
    results = drive_service.files().list().execute()

    files = results.get('files', [])
    ticket_images = [aticket_image for aticket_image in results.get('files', []) if aticket_image['mimeType'] == 'image/jpeg']

    if not ticket_images:
        print('No tickets found.')
    else:
        print('Downloading tickets...')
        for ticket in ticket_images:
            file_id = ticket['id']
            file_name = ticket['name']
            file_path = os.path.join(DESTINATION_FOLDER, file_name)

            request = drive_service.files().get_media(fileId=file_id)
            fh = open(file_path, 'wb')
            downloader = MediaIoBaseDownload(fh, request)
            done = False

            while not done:
                status, done = downloader.next_chunk()
                print(f"Downloading {file_name} - {int(status.progress() * 100)}%")

            print(f"{file_name} downloaded successfully.")

        print(f"Download completed. Total number of tickets {len(ticket_images)}")

fetch_files_from_drive()
