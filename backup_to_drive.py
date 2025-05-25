import os
from datetime import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Ανέβασε τοπικά αυτό το path για το secret σου
CLIENT_SECRET_FILE = 'client_secret.json'
SCOPES = ['https://www.googleapis.com/auth/drive.file']
DB_PATH = 'instance/gelato_erp.db' 

def backup_to_drive():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    now = datetime.now().strftime('%Y-%m-%d_%H-%M')
    file_metadata = {
        'name': f'gelato_erp_backup_{now}.db',
        'mimeType': 'application/octet-stream'
    }
    media = MediaFileUpload(DB_PATH, mimetype='application/octet-stream')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f"✅ Backup uploaded successfully with ID: {file.get('id')}")

if __name__ == '__main__':
    backup_to_drive()