#!/bin/bash
#This script helps to create the files required to enable communication encryption on cassandra, you need to enable server_encryption_options, internode_encryption and client_encryption_options on the custom cassandra.yaml
#    keystore and truststore: files used by cassandra nodes to perform encryption
#    cassandra.cer: file requried by the clients connecting to cassandra
set -xe
keytool -genkeypair -alias cassandra -keyalg RSA -validity 365 -keystore keystore
keytool -list -v -keystore keystore
keytool -export -alias cassandra -keystore keystore -rfc -file cassandra.cer
keytool -import -alias cassandracert -file cassandra.cer -keystore truststore
keytool -list -v -keystore truststore

