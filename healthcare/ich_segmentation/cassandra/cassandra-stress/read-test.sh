#!/bin/bash
# usage:
#       read-test.sh <ip-address>

cassandra-stress user profile=./cassandra-healthcare-stress-template.yaml ops\(simple1=1\) duration=5m cl=ONE no-warmup -pop dist=UNIFORM\(1..8000000\) -mode native cql3 maxPending=256 connectionsPerHost=32 -node "$1" -rate threads=800
