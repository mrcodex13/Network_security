import os
import sys
import json
import pymongo
import certifi
import pandas as pd

from dotenv import load_dotenv

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

load_dotenv()
MONGO_DB_URL=os.getenv("MONGODB_URI")
print(MONGO_DB_URL)

import certifi
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self,file_path):
        try:
            data=pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records=list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.mongo_client = pymongo.MongoClient(
                MONGO_DB_URL,
                tls=True,
                tlsCAFile=certifi.where(),
                serverSelectionTimeoutMS=30000
            )

        # Test connection
            self.mongo_client.admin.command("ping")
            print("MongoDB connection successful")

            # Select database and collection
            self.database = self.mongo_client[database]
            self.collection = self.database[collection]

            # Insert records
            self.collection.insert_many(records)

            return len(records)

        except Exception as e:
            raise NetworkSecurityException(e, sys)    
        
if __name__=='__main__':
    FILE_PATH="Network_Data/phisingData.csv"
    DATABASE="Kartik"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)

    print("all records are collected and ready to insert into mongodb")
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print( "Total records inserted:", no_of_records)