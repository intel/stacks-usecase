from minio import Minio
from minio.error import ResponseError

import logging

import os
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

client = Minio(os.getenv("S3_ENDPOINT"),
               access_key=os.getenv("AWS_ACCESS_KEY_ID"),
               secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"), secure=False)

bucket = os.getenv("S3_BUCKET")
outdir = os.getenv('OUT_DIR')
prefix = re.sub("s3://%s/"%(bucket), '', outdir)

def upload_objects():

    try:
        root_path = '/workdir/models/' # local folder for upload

        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\","/")
            directory_name = path.replace(root_path,"")
            for file in files:
                client.fput_object(bucket, prefix + '/' + directory_name+'/'+file, os.path.join(path, file), 'text/plain')
    except Exception as err:
        logger.exception(err)
if __name__ == '__main__':
    upload_objects()
