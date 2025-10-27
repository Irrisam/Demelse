from fs_gcsfs import GCSFS
from fs.osfs import OSFS
from fs.copy import copy_fs
import os
from dotenv import load_dotenv
import pandas as pd


def local_dev_data_fetcher():
    if os.getenv('GOOGLE_CLOUD_BUCKET_ADDRESS'):
        gcsfs = GCSFS(bucket_name=os.getenv('GOOGLE_CLOUD_BUCKET_ADDRESS'))
        local_fs = OSFS("training_datas")
        copy_fs(gcsfs, local_fs)
    else:
        pass


def fs_file_opener(dataset_path):
    fs = fs_opener()
    with fs.open(dataset_path, "rb") as file:
        dataset = pd.read_csv(file)
    return dataset


def fs_opener():
    load_dotenv()
    if os.getenv('GOOGLE_CLOUD_BUCKET_ADDRESS'):
        fs = GCSFS(bucket_name=os.getenv('GOOGLE_CLOUD_BUCKET_ADDRESS'))
    else:
        print("local_dev")
        fs = OSFS("./training_datas")
    return fs
