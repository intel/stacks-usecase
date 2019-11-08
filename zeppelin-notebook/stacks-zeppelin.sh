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

set -o pipefail -o noclobber

IMAGE_NAME='stacks_zeppelin'
CONTAINER_NAME='stacks_zeppelin_container'
CONTAINER_HOSTNAME='zeppelindars'


build_zeppelin () {
    git clone https://github.com/apache/zeppelin.git
    cd zeppelin && mvn clean package -Pspark-2.4 -Pscala-2.12 -DskipTests | fgrep -v "[INFO]" | fgrep -v "Download" | fgrep -v "[SECURITY]"
    if [[ $? -ne 0 ]]; then echo "[ERROR] Zeppelin build" && exit 1; fi
}

function replace_hostname_in_conf_files () {
    sed -i "s|<value>127.0.0.1</value>|<value>${CONTAINER_HOSTNAME}</value>|g" zeppelin/conf/zeppelin-site.xml
    if [[ $? -ne 0 ]]; then echo "[ERROR] Replace hostname ${CONTAINER_HOSTNAME} in zeppelin-site.xml" && exit 1; fi
    sed -i "s|spark://127.0.0.1:7077|spark://${CONTAINER_HOSTNAME}:7077|g" zeppelin/conf/interpreter.json
    if [[ $? -ne 0 ]]; then echo "[ERROR] Replace spark master URL spark://${CONTAINER_HOSTNAME}:7077 in interpreter.json" && exit 1; fi
}

copy_files () {
    cp conf/* zeppelin/conf
    if [[ $? -ne 0 ]]; then echo "[ERROR] Copy Configuration files" && exit 1; fi
    replace_hostname_in_conf_files
    cp -r notebooks/* zeppelin/notebook
    if [[ $? -ne 0 ]]; then echo "[WARNING] Copy Notebook example files" && exit 1; fi
    replace_hostname_in_conf_files
}

build_image () {
    docker build . -t ${IMAGE_NAME}
    if [[ $? -ne 0 ]]; then echo "[ERROR] Docker build ${IMAGE_NAME}" && exit 1; fi
}

start_zeppelin () {
    docker run -dit \
    --ulimit nofile=1000000:1000000 \
    -e SPARK_MASTER_IP=${CONTAINER_HOSTNAME} \
    -p 4040:4040 -p 7077:7077 -p 8080:8080 -p 8081:8081 -p 8082:8082 \
    --mount type=bind,src=$(pwd)/zeppelin,dst=/opt/zeppelin \
    -h ${CONTAINER_HOSTNAME} \
    --name ${CONTAINER_NAME} ${IMAGE_NAME}
    if [[ $? -ne 0 ]]; then echo "[ERROR] Docker run ${CONTAINER_NAME}" && exit 1; fi
}

stop_zeppelin () {
    docker stop ${CONTAINER_NAME}
    if [[ $? -ne 0 ]]; then echo "[ERROR] Docker stop container ${CONTAINER_NAME}" && exit 1; fi
    docker rm ${CONTAINER_NAME}
    if [[ $? -ne 0 ]]; then echo "[ERROR] Docker remove container ${CONTAINER_NAME}" && exit 1; fi
}

run_all (){
    build_zeppelin
    copy_files
    build_image
    start_zeppelin
}

action=-

main () {
    parse_options $@
    echo [INFO] Action: $action
    $action
}


help () {
    echo "stacks-zeppelin.sh [(-h|--help) | -a <action>]"
    echo "action: build_zeppelin, copy_files, build_image, start_zeppelin, stop_zeppelin, run_all"
    echo "e.g.  $ ./stacks-zeppelin.sh -a run_all"
}

parse_options () {
    OPTIONS=a:h
    LONG_OPTIONS=action:,verbose:,help
    ! PARSED=$(getopt --options=$OPTIONS --longoptions=$LONG_OPTIONS --name "$0" -- "$@")
    if [[ ${PIPESTATUS[0]} -ne 0 ]]; then
	# e.g. return value is 1
	#  then getopt has complained about wrong arguments to stdout
	exit 2
    fi

    # read getopt’s output this way to handle the quoting right:
    eval set -- "$PARSED"

    # now enjoy the options in order and nicely split until we see --
    show_help=0
    while true; do
	case "$1" in
            -h|--help)
        show_help=1
        shift
		;;
            -a|--action)
		action="$2"
		shift 2
		;;
            *)
          break
        ;;
	esac
    done
    if [[ $show_help == 1 ]]; then help && exit 0;fi
    if [[ "x$action" == "x-" ]]; then help && exit 1;fi
}

main $@