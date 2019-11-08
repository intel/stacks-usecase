#!/bin/bash
#
# Copyright (c) 2019 Intel Corporation
#
# Main author:
#   * lfponcen <luis.f.ponce.navarro@intelcom>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# echo commands to the terminal output
set -ex

case "$@" in
  spark-standalone)
    shift 1
    echo "spark-standalone starting Spark master and worker" && \
    ${SPARK_HOME}/sbin/start-master.sh && \
    ${SPARK_HOME}/sbin/start-slave.sh spark://${SPARK_MASTER_IP}:${SPARK_MASTER_PORT}
    tail -F /var/log/spark/* &
    while true; do sleep 1000; done
    ;;
  spark-master)
    shift 1
    echo "spark-master starting Spark master" && \
    ${SPARK_HOME}/sbin/start-master.sh
    tail -F /var/log/spark/* &
    while true; do sleep 1000; done
    ;;
  spark-worker)
    shift 1
    echo "spark-worker starting Spark worker" && \
    ${SPARK_HOME}/sbin/start-slave.sh spark://${SPARK_MASTER_IP}:${SPARK_MASTER_PORT}
    tail -F /var/log/spark/* &
    while true; do sleep 1000; done
    ;;
  zeppelin-master)
    shift 1
    echo "zeppelin-master starting Spark master, Zeppelin server" && \
    ${SPARK_HOME}/sbin/start-master.sh && \
    ${ZEPPELIN_HOME}/bin/zeppelin.sh
    ;;

  *)
    echo "No arguments given, starting by default: Spark master, worker and Zeppelin server" && \
    ${SPARK_HOME}/sbin/start-master.sh && \
    ${SPARK_HOME}/sbin/start-slave.sh spark://${SPARK_MASTER_IP}:${SPARK_MASTER_PORT} && \
    ${ZEPPELIN_HOME}/bin/zeppelin.sh
    ;;
esac