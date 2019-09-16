from minio import Minio
from minio.error import ResponseError

import os

client = Minio(os.getenv("S3_ENDPOINT"),
               access_key=os.getenv("AWS_ACCESS_KEY_ID"),
               secret_key=os.getenv("AWS_SECRET_ACCESS_KEY"), secure=False)

prefix = os.getenv('OUT_DIR').replace("s3://dkube/",'')

def upload_objects():

    try:
        root_path = '/workdir/models/' # local folder for upload

        for path, subdirs, files in os.walk(root_path):
            path = path.replace("\\","/")
            directory_name = path.replace(root_path,"")
            for file in files:
                client.fput_object(os.getenv("S3_BUCKET"), prefix + '/' + directory_name+'/'+file, os.path.join(path, file), 'text/plain')
    except Exception as err:
        print(err)

if __name__ == '__main__':
    upload_objects()

