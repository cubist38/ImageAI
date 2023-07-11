import supabase
import os 
import json
import logging
from app.dal.image_dto import ImageDTO
from app.dal.storage_dto import StorageDTO
from app.helpers.image_helper import resize_image
from app.helpers.encoder import ImageNTextEncoder

connect_config = json.load(open('./app/connection_config.json'))

class SupabaseDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            try: 
                cls._instance.supabase = supabase.create_client(
                    "https://kghukcserwconiuwgboq.supabase.co",
                    connect_config['SUPABASE_PUBLIC_KEY']
                )
                logging.info('Connected to Supabase!!')
            except Exception as e:
                logging.error("Error while connecting to Supabase: ", e)
        return cls._instance

    def save_storage(self, storage: StorageDTO):
        table = "storages"
        storage_data = {
            "email": storage.email,
            "storage_url": storage.storage_url
        }
        try: 
            data, count = self.supabase.table(table).insert(storage_data).execute()

            logging.info(f'Save storage {storage} result: {data}')
            return data[1]
        except Exception as e:
            logging.error(f'Fail to save storage {storage}')
            return None
        
    def save_image(self, image: ImageDTO):
        table = "images"
        image_data = {
            "storage_url": image.storage_url,
            "image": image.image,
            "embedded": image.embedded
        }
        try: 
            data, count = self.supabase.table(table).insert(image_data).execute()

            logging.info(f'Save image {image} result: {data}')
            return data[1][0]["id"] 
        except Exception as e:
            logging.error(f'Fail to save image {image}')
            return None

    def get_storage_by_email(self, email):
        logging.info(f'Get storage by email {email}')

        table = "storages"
        data, count = self.supabase.table(table).select('*').eq("email", email).execute()

        logging.info(f'Get storage by email {email} result: {data}')
        
        data = data[1]
        return [StorageDTO(item['email'], item['storage_url']) for item in data]

    def get_image_by_storage_url(self, storage_url):
        logging.info(f'Get image by storage URL {storage_url}')

        table = "images"
        data, count = self.supabase.table(table).select('*').eq("storage_url", storage_url).execute()
        
        logging.info(f'Get image by storage URL {storage_url} successful')

        data = data[1]
        return [ImageDTO(item['storage_url'], item['image'], item['embedded'], item['id']) for item in data]
    
    def get_image_by_email(self, email): 
        storages = self.get_storage_by_email(email) 
        storages_url = [item.storage_url for item in storages]

        images = [] 
        for storage_url in storages_url: 
            images_in_storage = self.get_image_by_storage_url(storage_url) 
            for image in images_in_storage: 
                images.append(image)
        
        return images

    def upload_image(self, image_path, image_name, storage_url): 
        if (not os.path.isfile(image_path)): 
            logging.info(f'{image_path} is not a file')
            return None
        
        try: 
            logging.info('hello1')
            resize_image(image_path, 448, 448)
            logging.info('hello2')
            image_embedded = ImageNTextEncoder().encode_image_by_path(image_path).tolist()
            logging.info('hello3')
            image_id = self.save_image(ImageDTO(storage_url, image_name, image_embedded)) 
            logging.info('hello4')
            res = self.supabase.storage.from_('images').upload(f'{image_id}.{image_path.split(".")[-1]}', image_path)
            logging.info('hello5')
            logging.info(f'Upload {storage_url}/{image_name} successful!!')
            return f'https://kghukcserwconiuwgboq.supabase.co/storage/v1/object/public/images/{image_id}.{image_path.split(".")[-1]}'
        except Exception as e: 
            logging.error(f'Error to upload {storage_url}/{image_name}')
            return None
    