#!/usr/bin/env python3
try:
  from pymongo import MongoClient
except ModuleNotFoundError:
  print('pymongo module must be install via pip')
  exit(1)

def get_mongo_client(mongo_host, mongo_port):
  mongo_client = MongoClient(mongo_host, mongo_port)
  return(mongo_client)

def setup_mongo(mongo_host, mongo_port):
  mongo = get_mongo_client(mongo_host, mongo_port)
  db = mongo.compliance
  scans_col = db.scans
  return(scans_col)

def insert_devices_into_db(devices_col, devices_dict):
  [ ( devices_col.insert_one(x) ) for x in devices_dict.get('devices') if not devices_col.find_one({"IP Address": x.get('IP Address')}) ]
  print('Devices in collection: ' + str(devices_col.count()))
