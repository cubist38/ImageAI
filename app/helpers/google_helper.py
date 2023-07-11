import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
import google.auth
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import io
from tqdm import tqdm
from googleapiclient.http import MediaIoBaseDownload
import re
import json
import logging
from app.dal.supabase_dao import SupabaseDAO
from app.dal.storage_dto import StorageDTO

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

connect_config = json.load(open('./app/connection_config.json'))

class GoogleHelper:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Google Drive API
            cred = None

            pickle_file = f"token_drive_v3.pickle"

            if os.path.exists(pickle_file):
                with open(pickle_file, "rb") as token:
                    cred = pickle.load(token)

            if not cred or not cred.valid:
                if cred and cred.expired and cred.refresh_token:
                    cred.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(connect_config["GOOGLE_SERVICE_CREDENTIALS"], ["https://www.googleapis.com/auth/drive"])
                    flow.redirect_uri = "urn:ietf:wg:oauth:2.0:oob"
                    auth_url, _ = flow.authorization_url(prompt='consent')
                    print(f'Please visit this URL to authorize this application: {auth_url}')
                    code = input("Enter the authorization code: ")
                    flow.fetch_token(code=code)
                    cred = flow.credentials


                with open(pickle_file, "wb") as token:
                    pickle.dump(cred, token)

            try:
                service = build('drive', 'v3', credentials=cred)
                cls._instance.service = service
                logging.info('Google Drive service created successfully')
            except Exception as e:
                logging.error(f"Unable to connect google drive api {e}")

        return cls._instance


    def download_file(self, dowid, dfilespath):
        try: 
            request = self.service.files().get_media(fileId=dowid)
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            pbar = tqdm(total=100, ncols=70)
            while done is False:
                status, done = downloader.next_chunk()
                if status:
                    pbar.update(int(status.progress() * 100) - pbar.n)
            pbar.close()

            with io.open(dfilespath, "wb") as f:
                fh.seek(0)
                f.write(fh.read())

            return True
        except Exception as e: 
            logging.error(f'Fail to download file {dowid}')
            return False

    def list_folder(self, email, storage_url, filid):
        page_token = None
        while True:
            results = (
                self.service.files()
                .list(
                    pageSize=1000,
                    q="'" + filid + "'" + " in parents",
                    fields="nextPageToken, files(id, name, mimeType)",
                )
                .execute()
            )
            page_token = results.get("nextPageToken", None)
            if page_token is None:
                folder = results.get("files", [])
                for item in folder:
                    if str(item["mimeType"]) == str("application/vnd.google-apps.folder"):
                        self.list_folder(email, item["id"])
                    else:
                        if (not item["name"].lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))): 
                            continue
                        
                        # Download image
                        image_path = f'temp.{item["name"].split(".")[-1]}'
                        logging.info(f'Downloaded user: {email}, image: {item["name"]}')

                        # Upload to database
                        if (self.download_file(item["id"], image_path)):
                            SupabaseDAO().upload_image(image_path, item["name"], storage_url)
            break
        return folder

    def download_folder(self, email, storage_url, folder_id, dest = './temp'):
        folder = self.service.files().get(fileId=folder_id).execute()
        folder_name = folder.get("name")
        page_token = None
        while True:
            results = (
                self.service.files()
                .list(
                    q=f"'{folder_id}' in parents",
                    spaces="drive",
                    fields="nextPageToken, files(id, name, mimeType)",
                )
                .execute()
            )
            page_token = results.get("nextPageToken", None)
            if page_token is None:
                items = results.get("files", [])
                if not items: # Not folder, is file
                    if (not folder_name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))): 
                        continue

                    # Download image
                    image_path = f'temp.{folder_name.split(".")[-1]}'
                    logging.info(f'Downloaded user: {email}, image: {folder_name}')

                    # Upload to database
                    if (self.download_file(folder_id, image_path)):
                        SupabaseDAO().upload_image(image_path, folder_name, storage_url)
                else:
                    logging.info(f"Start downloading folder '{folder_name}'.")

                    for index, item in enumerate(items):
                        if item["mimeType"] == "application/vnd.google-apps.folder":
                            self.list_folder(email, storage_url, item["id"])
                        else:
                            if (not item["name"].lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))): 
                                continue

                            # Download image
                            image_path = f'temp.{item["name"].split(".")[-1]}'
                            logging.info(f'Downloaded user: {email}, image: {item["name"]}')

                            # Upload to database
                            if (self.download_file(item["id"], image_path)):
                                SupabaseDAO().upload_image(image_path, item["name"], storage_url)
            break

    def extract_drive_id(self, links):
        output = []
        for link in links:
            link = link.strip()
            if "folders" in link:
                pattern = r"(?<=folders\/)[^/|^?]+"
            else:
                pattern = r"(?<=/d/|id=)[^/|^?]+"
            match = re.search(pattern, link)
            if match:
                output.append(match.group())
        if output:
            return output
        else:
            return None
        
    def import_storage(self, email, link): 
        try: 
            uniq_id = self.extract_drive_id([link])
            if ((uniq_id is None) or (len(uniq_id) == 0)): 
                return 
            SupabaseDAO().save_storage(StorageDTO(email, link))
            self.download_folder(email, link, uniq_id[0])
            return True
        except Exception as e: 
            return False
