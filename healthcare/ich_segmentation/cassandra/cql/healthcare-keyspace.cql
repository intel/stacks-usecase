CREATE KEYSPACE healthcare_keyspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor' :'3'} AND DURABLE_WRITES = true;

USE healthcare_keyspace;

CREATE TABLE  processed_data (
    id uuid,
    date timestamp,
    is_label boolean,
    patient_number int,
    slice_number smallint,
    intraventricular boolean,
    intraparenchymal boolean,
    subarachnoid boolean,
    epidural boolean,
    subdural boolean,
    no_hemorrhage boolean,
    fracture_yes_no boolean,
    image_filename text,
    image_blob blob,
    PRIMARY KEY (patient_number,date)
);

