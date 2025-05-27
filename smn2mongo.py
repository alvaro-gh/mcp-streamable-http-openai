import json
import logging
import pymongo
import requests
import sys
import time

logging.basicConfig(encoding='utf-8', level=logging.INFO)
logging.info('Starting weather daemon')
base_url='https://ws.smn.gob.ar/map_items/weather'

while True:
  logging.info(f'Base URL is: {base_url}')
  logging.info('Requesting weather...')
  r = requests.get(base_url)
  if r.status_code != 200:
    logging.error("Couldn't fetch weather data")
    sys.exit(1)
  data = json.loads(r.text)

  logging.info('Connecting to MongoDB')
  client = pymongo.MongoClient('localhost', 27017)
  logging.info('Getting smn database...')
  database = client.smn
  logging.info('Listing collections')
  collections = database.list_collection_names()
  if 'weather' in collections:
    logging.info('Weather collection is present, dropping')
    database.drop_collection('weather')
  logging.info('Creating weather collection')
  collection = database.weather
  logging.info('Inserting weather data into collection')
  for i in data:
    collection.insert_one(i)
  logging.info('Sleeping...')
  time.sleep(300)