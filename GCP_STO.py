# -*- coding: utf-8 -*-
"""
Created on Thu Jul  8 03:31:09 2021

@author: Kenyon
"""
import CONFIG
import datetime
import pandas as pd
import time
import json
import sqlalchemy
import pymysql
from google.cloud import storage
from google.cloud.sql.connector import connector
import mysql.connector
from mysql.connector.constants import ClientFlag
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

class GCP_STO:
        
    def __init__(self):
        self.engine = self.init_connection_engine()
    def init_connection_engine(self) -> sqlalchemy.engine.Engine:
        def getconn() -> pymysql.connections.Connection:
            conn: pymysql.connections.Connection = connector.connect(
                CONFIG.gcp['conn'],
                CONFIG.gcp['driver'],
                user=CONFIG.gcp['user'],
                password=CONFIG.gcp['password'],
                db=CONFIG.gcp['db'],
            )
            return conn
    
        engine = sqlalchemy.create_engine(
            "mysql+pymysql://",
            creator=getconn,
            echo=False)
    
        return engine
    
    def upload_blob(self, bucket_name, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        # The ID of your GCS bucket
        # bucket_name = "your-bucket-name"
        # The path to your file to upload
        # source_file_name = "local/path/to/file"
        # The ID of your GCS object
        # destination_blob_name = "storage-object-name"
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
    
        blob.upload_from_filename(source_file_name)
    
        print(
            "File {} uploaded to {}.".format(
                source_file_name, destination_blob_name
            )
        )
        
        
    def download_all_blobs(self, bucket_name, destination_file_name):
        """Downloads a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # source_blob_name = "storage-object-name"
        # destination_file_name = "local/path/to/file"
    
        storage_client = storage.Client()
    
        bucket = storage_client.bucket(bucket_name)
    
        # Construct a client side representation of a blob.
        # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
        # any content from Google Cloud Storage. As we don't need additional data,
        # using `Bucket.blob` is preferred here.
        #blob = bucket.blob(source_blob_name)
        #bucket.get_blob
        blob_list = bucket.list_blobs()
        for b in blob_list:
            b.download_to_filename(destination_file_name)
    
    def delete_all_blobs(self, bucket_name):
        """Downloads a blob from the bucket."""
    
        storage_client = storage.Client()
    
        bucket = storage_client.bucket(bucket_name)
    
        # Construct a client side representation of a blob.
        # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
        # any content from Google Cloud Storage. As we don't need additional data,
        # using `Bucket.blob` is preferred here.
        blob_list = bucket.list_blobs()
        for b in blob_list:
            b.delete()
            
    def download_blob(self, bucket_name, source_blob_name, destination_file_name):
        """Downloads a blob from the bucket."""
        # bucket_name = "your-bucket-name"
        # source_blob_name = "storage-object-name"
        # destination_file_name = "local/path/to/file"
    
        storage_client = storage.Client()
    
        bucket = storage_client.bucket(bucket_name)
    
        # Construct a client side representation of a blob.
        # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
        # any content from Google Cloud Storage. As we don't need additional data,
        # using `Bucket.blob` is preferred here.
        blob = bucket.blob(source_blob_name)
        blob.download_to_filename(destination_file_name)
    
        print(
            "Blob {} downloaded to {}.".format(
                source_blob_name, destination_file_name
            )
        )
    def insert_product(self, p):
        
        with self.engine.connect() as connection:
            insert_string = "insert into product_images (storage_name, timestamp, store_name, camera_id, barcode_information) values(\'{}\',\'{}\',\'{}\',\'{}\',\'{}\')".format(p[0], p[1], p[2], p[3], p[4])
            connection.execute(insert_string)
    
    def flush_table(self):
        with self.engine.connect() as connection:
            result = connection.execute("delete from product_images")
        
    def init_table(self): 
        with self.engine.connect() as connection:
            result = connection.execute("drop table if exists product_images")
            #[print(row) for row in result]
        
        meta = MetaData()
        #timestamp, store name, camera id, barcode information 
        product_images = Table(
            'product_images', meta, 
            Column('storage_name', String(256)), 
            Column('timestamp', String(20)), 
            Column('store_name', String(20)), 
            Column('camera_id', String(1)),
            Column('barcode_information', String(13)), 
        )
        meta.create_all(self.engine)
    def fetch_products(self, path='cereal_box_data/'):
        # initialize list of lists
        data = []
         
        with self.engine.connect() as connection:
            result = connection.execute("select * from product_images")
            for row in result:
                self.download_blob('opencv-storage', row[0], 'cereal_box_images_dst/{}'.format(row[0]))
                data.append(row.values())
        
        # Create the pandas DataFrame
        if(path):
            df = pd.DataFrame(data, columns = ['storage_name', 'timestamp', 'store_name', 'camera_id', 'barcode_information'])
            df_name = str(int(datetime.datetime.now().timestamp()))
            df.to_csv('{}/{}.csv'.format(path, df_name))