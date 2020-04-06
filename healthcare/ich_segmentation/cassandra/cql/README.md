# CQL files

## Creating the database
In order to create the database you should run the cassandra client `cqlsh` passing `healthcare-keyspace.cql` as argument.

```bash
cqlsh -f ./healthcare-keyspace.cql
```

## Enabling SSL on nodetool and cqlsh
If the cassandra cluster has SSL enabled, you need to configure nodetool and cqlsh, in this directory there are two examples on how to configure the clients. Once modified according to your needs `cqlshrc` and `nodetool-ssl.properties`  must be placed on `~/.cassandra`. 

To use nodetool with SSL:

```bash
nodetool -h <cassandra-host> -u jmx_user -pw <jmx-password>  --ssl status
```

To use cqlsh with SSL:

```bash
cqlsh --ssl
```

## Backing up the database
You can backup the database using `nodetool snapshot` and `sstableloader` or using the cql command `COPY` to create a csv file with all table contents, generally speaking using  the first method is more compute efficient than using `COPY` but if your data size is relatively small it should be easier to use `COPY`.

```bash
# To backup a table
cqlsh -e "COPY healthcare_keyspace.processed_data to '/tmp/healthcare-table.csv' WITH HEADER = true;"

# To restore a table
cqlsh -e "COPY healthcare_keyspace.processed_data from '/tmp/healthcarec-table.csv' WITH HEADER = true ;"
```
