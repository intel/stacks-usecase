#!/bin/bash
# usage:
#       write-test.sh <ip-address>

cassandra-stress user profile=./cassandra-healthcare-stress-template.yaml ops\(insert=1\) n=8000000 cl=ONE no-warmup -pop seq=1..8000000 -mode native cql3 maxPending=256 connectionsPerHost=32 -node "$1" -rate threads=800
