#!/bin/bash

: ${PREFIX:=/usr}

### C O M M O N  T A S K S ###
# Directory to find config artifacts
CONFIG_DIR="/tmp/config"

# Copy config files from volume mount
for f in $CONFIG_DIR/* ; do
  if [[ -e $f ]]; then
    if [[ "${HOSTNAME}" =~ "hdfs" || "${HOSTNAME}" =~ "yarn" ]]; then
      cp $f $HADOOP_CONF_DIR
    elif [[ "${HOSTNAME}" =~ "master" || "${HOSTNAME}" =~ "worker" ]]; then
      cp $f $SPARK_CONF_DIR
    else
       echo "ERROR: Could not copy $f in $CONFIG_DIR"
    fi
  else
    echo "ERROR: Could not find $f in $CONFIG_DIR"
    exit 1
  fi
done

# Check if native libraries available
# [  -z $(hadoop checknative -a | grep hadoop: | grep true | cut -d ':' -f1) ] && echo "No haddop native libraries exiting." && exit 1 || echo "Hadoop using native libraries"

### H A D O O P  T A S K S ###
if [[ "${HOSTNAME}" =~ "hdfs-nn" ]]; then
  mkdir -p /root/hdfs/namenode
  rm -rf /root/hdfs/namenode
  hdfs namenode -format -force -nonInteractive
  hdfs --daemon start namenode
  sleep 3
  yarn --config $HADOOP_CONF_DIR --daemon start resourcemanager
fi

if [[ "${HOSTNAME}" =~ "hdfs-dn" ]]; then
  mkdir -p /root/hdfs/datanode
  rm -rf /root/hdfs/datanode
  #  wait up to 50 seconds for namenode
  swupd bundle-add curl
  count=0 && while [[ $count -lt 50 && -z `curl -sf http://hdfs-nn:9870` ]]; do echo "Waiting for hdfs-nn" ; ((count=count+1)) ; sleep 2; done
  [[ $count -eq 50 ]] && echo "Timeout waiting for hdfs-nn, exiting." && exit 1
  hdfs --daemon start datanode
  pip install -r /mnt/data/requirements.txt
  yarn --config $HADOOP_CONF_DIR --daemon start nodemanager
fi

### S P A R K  T A S K S ###
mkdir -p $SPARK_LOG_DIR/spark-events
cat >> $SPARK_CONF_DIR/spark-defaults.conf <<EOL
spark.eventLog.enabled           true
spark.eventLog.dir               file:/var/log/spark/spark-events
spark.history.fs.logDirectory    file:/var/log/spark/spark-events
EOL

if [[ "${SPARK_MODE}" =~ "master" ]]; then
  $PREFIX/share/apache-spark/sbin/start-master.sh
fi

#if [[ "${SPARK_MODE}" =~ "worker" ]]; then
#  $PREFIX/share/apache-spark/sbin/start-slave.sh $SPARK_MASTER_URL
#fi

### L O G   T A S K S ###
if [[ $1 == "-h" ]]; then
  until find /var/log/hadoop -mmin -1 | egrep -q '.*'; echo "`date`: Waiting for logs..." ; do sleep 2 ; done
  tail -F /var/log/hadoop/* &
  while true; do sleep 1000; done
fi

if [[ $1 == "-d" ]]; then
  until find $SPARK_LOG_DIR -mmin -1 | egrep -q '.*'; echo "`date`: Waiting for logs..." ; do sleep 10 ; done
  tail -F $SPARK_LOG_DIR/* &
  while true; do sleep 1000; done
fi

if [[ $1 == "-bash" ]]; then
  /bin/bash
fi
