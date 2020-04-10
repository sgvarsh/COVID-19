#!/usr/bin/env python
"""
Program: solr_ingestor.py
Purpose: Used for ingesting documents to solr
Author:  Sharad Varshney
Created: Mar 26, 2020
"""
import os
import argparse
import json
from pathlib import Path
import pysolr

from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

config = {
    "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=account_name;AccountKey=somekey",
    "storage_account":"account_name",
    "container_name": "data",
    "solr_url" : "http://localhost:8983/solr/covid19"
}

def get_blob_client():
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_name = config["container_name"]
    local_file_name = "datafiles"
    # Create a blob client using the local file name as the name for the blob
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=local_file_name)
    return blob_client

def get_files_from_blob():
    connect_str = config['AZURE_STORAGE_CONNECTION_STRING']
    container_client = ContainerClient.from_connection_string(connect_str, container_name="data")

    # List the blobs in the container
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        print("\t" + blob.name)
        print(blob)
        # print(data)

def send_for_solr_indexing(doc):
    # post to solr for indexing
    solr = pysolr.Solr(config["solr_url"], timeout=10)
    # How you'd index data.
    solr.add(doc)

    # You can optimize the index when it gets fragmented, for better speed.
    solr.optimize()  # Optimize also do commit 'solr/clst5/update/?commit=true' (post) with body '<optimize '


def solr_indexing_optimization():
    # post to solr for indexing
    solr = pysolr.Solr(config["solr_url"], timeout=10)
    # You can optimize the index when it gets fragmented, for better speed.
    solr.optimize()  # Optimize also do commit 'solr/clst5/update/?commit=true' (post) with body '<optimize '




def main(basepath):
    print("Path : " + basepath)
    for entry in os.listdir(basepath):
        #if os.path.isdir(os.path.join(basepath, entry)):
        if os.path.isfile(os.path.join(basepath, entry)):
            print(entry)
            with open(os.path.join(basepath, entry), "r") as file:
                doc = json.loads(file.read())
                actual_body = ""
                for body in doc["body_text"]:
                    actual_body = body["text"]
                    actual_body = "".join(actual_body)
                print(actual_body)
                abstract = ""
                if doc["abstract"] is not None:
                    if len(doc["abstract"]) > 0:
                        abstract = doc["abstract"][0]["text"]
                map1 = { "paperid" : doc["paper_id"],
                         "title": doc["metadata"]["title"],
                         "abstract": abstract,
                         "body": actual_body
                         }
                print(map1)
                send_for_solr_indexing([map1])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--azure", help="Whether to read from Azure Blob",
                        type=str,
                        choices=["./CORD-19-research-challenge/"],
                        default="./CORD-19-research-challenge/comm_use_subset/comm_use_subset/")
    parser.add_argument("-p", "--path", help="Path of the dir",
                        type=str,
                        choices=["./CORD-19-research-challenge/"],
                        default="./CORD-19-research-challenge/comm_use_subset/comm_use_subset/")
    args = parser.parse_args()

    main(args.path)
