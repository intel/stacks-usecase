#!/usr/bin/python
#This script is an example on how to read from cassandra DB, it assumes that the DB is already created
#how to run:
#     get-healthcare-processed-data <cassandra-host> <img-filename>

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import os, uuid, argparse, ssl

parser = argparse.ArgumentParser()
parser.add_argument("host", help="Cassandra host where the file is stored")
parser.add_argument("imageFileName", help="filename of the file to be retrieved from cassandra")
args = parser.parse_args()

#SSL options
ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.verify_mode = ssl.CERT_REQUIRED
ssl_context.check_hostname = False
ssl_context.load_verify_locations('cassandra.cer')

# Auth
ap = PlainTextAuthProvider(username=os.getenv("DB_USER"), password=os.getenv("DB_PASS"))

#Connection to the DB
cluster = Cluster([args.host],auth_provider=ap,ssl_context=ssl_context)
session = cluster.connect('healthcare_keyspace')
query = "SELECT * FROM processed_data WHERE image_filename=\'" + args.imageFileName + "\'"
rows = session.execute(query)
for processed_data_row in rows:
    new_image_filename = processed_data_row.image_filename + ".out"
    with open(new_image_filename, 'wb') as file:
        file.write(processed_data_row.image_blob)
    print("Retrieved image file written into: ", new_image_filename, "\n")
    print("id: " + str(processed_data_row.id))
    print("date: " + str(processed_data_row.date))
    print("image_filename: " + processed_data_row.image_filename)

