# -*- coding: utf-8 -*-
"""
Created on Mon Jul  5 23:56:02 2021

@author: Kenyon
"""

#gcloud auth application-default login

import os

import GIS_SCR as sc
import GCP_STO
import GCP_UTIL as ut

#PIPELINE STEPS
INIT_IMAGES=True
INIT_BUCKET=True
INIT_TABLE=True
CREATE_PRODUCTS=True
FETCH_PRODUCTS=True
FLUSH_BUCKET=True
FLUSH_TABLE=True
FIND_BOXES=True

DOWNLOAD_IMAGES=1

#OBJECTS
sto = GCP_STO.GCP_STO()


if(INIT_IMAGES):
    ut.clear_directory('cereal_box_images_src/*')
        
    sc.downloadImages(DOWNLOAD_IMAGES)
    
    #RENAME IMAGES
    ut.clean_file_names('cereal_box_images_src/')
    
if(INIT_BUCKET):
    sto.delete_all_blobs('opencv-storage')
        
if(INIT_TABLE):
    sto.init_table()
    
if(CREATE_PRODUCTS):
    storage_names = os.listdir('cereal_box_images_src/') #change dir name to whatever
    
    for idx in range(len(storage_names)):
        p = ut.generate_product(storage_names[idx])
        sto.insert_product(p)
        sto.upload_blob('opencv-storage', 'cereal_box_images_src/{}'.format(p[0]), p[0])

    #with engine.connect() as connection:
    #    result = connection.execute("select * from product_images")
            
            
if(FETCH_PRODUCTS):
    sto.fetch_products()
if(FLUSH_BUCKET):
    sto.delete_all_blobs('opencv-storage')
if(FLUSH_TABLE):
    sto.flush_table()
    
if(FIND_BOXES):
        for count, filename in enumerate(os.listdir("cereal_box_images_dst/")):    
            try:
                ut.find_boxes(filename)
            except:
                pass