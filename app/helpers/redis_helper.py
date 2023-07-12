import redis
import json 
import logging
import pickle
import hashlib

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

connection_config = json.load(open('./app/connection_config.json'))

class RedisHelper: 
  _instance = None 

  IMAGE_URL_SUFFIX = 'image_url'
  FAISS_INDEX_SUFFIX = 'faiss_index'
  STORAGE_VERSION_SUFFIX = 'storage_ver'

  def __new__(cls):
    if (cls._instance == None):  
      try: 
        cls._instance = super().__new__(cls)

        cls._instance.redis = redis.Redis(host=connection_config['REDIS_HOST'], port=connection_config['REDIS_PORT'])
        logging.info(f'Connected to redis server {connection_config["REDIS_HOST"]}:{connection_config["REDIS_PORT"]}')
      except Exception as e: 
        logging.error(f'Fail to connect to redis server {connection_config["REDIS_HOST"]}:{connection_config["REDIS_PORT"]}')

    return cls._instance
  
  def save_object(self, key: str, value: object): 
    dumped_value = pickle.dumps(value)
    self.redis.set(key, dumped_value)
    

  def delete_object(self, key: str): 
    self.redis.delete(key) 

  def load_object(self, key: str):
    if (self.redis.exists(key)): 
      dumped_value = self.redis.get(key) 
      value = pickle.loads(dumped_value)
      return value
    else: 
      return None
    
  def get_storage_version(self, username): 
    key = f'{username}|{RedisHelper.STORAGE_VERSION_SUFFIX}'
    if (self.redis.exists(key)):
      return self.redis.get(key)
    return 0
    
  def update_storage_version(self, username): 
    key = f'{username}|{RedisHelper.STORAGE_VERSION_SUFFIX}'
    new_version = self.load_object(key)
    if (new_version is None): 
      new_version = 0
    else: 
      new_version += 1
    self.save_object(key, new_version)
    
  def save_faiss(self, username, image_url, faiss_index): 
    try: 
      self.update_storage_version(username)
      storage_version = self.get_storage_version(username)
      self.save_object(f'{username}|{RedisHelper.IMAGE_URL_SUFFIX}|storage_ver{storage_version}', image_url)
      self.save_object(f'{username}|{RedisHelper.FAISS_INDEX_SUFFIX}|storage_ver{storage_version}', faiss_index)
    except Exception as e: 
      logging.error(e)

  def load_faiss(self, username): 
    storage_version = self.get_storage_version(username)
    image_url = self.load_object(f'{username}|{RedisHelper.IMAGE_URL_SUFFIX}|storage_ver{storage_version}')
    faiss_index = self.load_object(f'{username}|{RedisHelper.FAISS_INDEX_SUFFIX}|storage_ver{storage_version}')
    return image_url, faiss_index
  
  def save_search_result(self, username, query, result): 
    storage_version = self.get_storage_version(username)
    key = hashlib.md5(f'{username}|this_is_salt^^X_X<(")|{query}|this_is_another_salt*_*|{storage_version}'.encode()).hexdigest()
    self.save_object(key, result)

  def load_search_result(self, username, query): 
    storage_version = self.get_storage_version(username)
    key = hashlib.md5(f'{username}|this_is_salt^^X_X<(")|{query}|this_is_another_salt*_*|{storage_version}'.encode()).hexdigest()
    return self.load_object(key)
  
# For testing 
# import faiss
# import numpy as np
# from numpy import random

# len = 8

# index = faiss.IndexFlatL2(len)

# temp = np.array([[random.rand() for _ in range(len)] for __ in range(3)])

# urls = ['url1', 'url2', 'url3']

# for tt in temp: 
#   index.add(np.array([tt]))

# RedisHelper().save_faiss('temp', urls, index)

# print(temp)

# dists, ids = index.search(np.array([temp[1]]), index.ntotal)
# print(dists, ids, urls)

# urls2, index2 = RedisHelper().load_faiss('temp')

# dists, ids = index2.search(np.array([temp[1]]), index.ntotal)
# print(dists, ids, urls2)

# RedisHelper().save_search_result('temp', 'text', ['123123123', '11111', 'Hello'])

# result = RedisHelper().load_search_result('temp', 'text')
# print(result)