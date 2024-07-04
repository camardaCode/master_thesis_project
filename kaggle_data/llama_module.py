import time
import json
import os
from datetime import datetime
from kaggle.api.kaggle_api_extended import KaggleApi


def create_dataset_metadata_file(files_path):
    metadata_file = './kaggle_data/mydataset/dataset-metadata.json'
    data = {
        "title": "DepositionsAndReports",
        "id": "lessiashadow/depositionsandreports",
        "resources": []
    }
    for file in files_path:
        new_resource = {
            "path": file
        }
        data['resources'].append(new_resource)
    with open(metadata_file, 'w') as file:
        json.dump(data, file, indent=2)


def get_translation(folder_path, files_path):
    create_dataset_metadata_file(files_path)

    api = KaggleApi()
    api.authenticate()

    api.dataset_create_version(folder_path, datetime.now())

    api.kernels_pull("lessiashadow/notebooka7c9c2c15d", "./kaggle_data/mynotebook", metadata=False)
    api.kernels_push_cli("./kaggle_data/mynotebook")
    status = api.kernels_status("lessiashadow/notebooka7c9c2c15d")['status']
    while status in ["running", "queued"]:
        time.sleep(10)
        status = api.kernels_status("lessiashadow/notebooka7c9c2c15d")['status']

    api.kernels_output("lessiashadow/notebooka7c9c2c15d", "./kaggle_data/mynotebook")
