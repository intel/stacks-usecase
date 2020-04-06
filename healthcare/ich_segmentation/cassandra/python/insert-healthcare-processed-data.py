#!/usr/bin/python
#This script is an example of how to insert data into the DB, it assumes the DB is already created.
#How to run:
#
#   insert-healthcare-processed-data.py <cassandra-host> <img-file> 

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os, uuid, argparse,ssl

parser = argparse.ArgumentParser()
parser.add_argument("host", help="Cassandra host where the file will be stored")
parser.add_argument("imageFilePath", help="Path of the file to be stored on cassandra")
args = parser.parse_args()

#SSL options
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = False
ssl_context.load_verify_locations('cassandra.cer')

# Auth
ap = PlainTextAuthProvider(username=os.getenv("DB_USER"), password=os.getenv("DB_PASSWD"))

#Connection to the DB
cluster = Cluster([args.host],auth_provider=ap,ssl_context=ssl_context)
session = cluster.connect('healthcare_keyspace')

#Reading image file
imageFile = os.path.join(args.imageFilePath)
if os.path.isfile(imageFile):
   imageFileName = os.path.basename(imageFile)
   imageFileSize = os.path.getsize(imageFile)
   f = open(imageFile, 'rb')
   data = f.read()
   imageBlob = bytearray(data)
else:
   sys.exit("The image file does not exists")

#Setting insertion values
is_label=0
patient_number=10
slice_number=9
epidural=0
intraparenchymal=0
intraventricular=0
subarachnoid=1
subdural=0
no_hemorrhage=0
fracture_yes_no=0

#Preparing query for insertion
blob_insertion = session.prepare("INSERT INTO processed_data (id, date, is_label, patient_number, slice_number, intraventricular, intraparenchymal, subarachnoid, epidural, subdural, no_hemorrhage, fracture_yes_no, image_filename, image_blob) VALUES ( UUID() , TOUNIXTIMESTAMP(now()), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )")

#Executing query
session.execute(blob_insertion, [is_label,patient_number,slice_number,intraventricular,intraparenchymal,subarachnoid,epidural,subdural,no_hemorrhage,fracture_yes_no,imageFileName, imageBlob])
print("image " + imageFileName  + " of size " + str(imageFileSize) + " bytes were inserted on cassandra hosted at " + args.host + "\n")

