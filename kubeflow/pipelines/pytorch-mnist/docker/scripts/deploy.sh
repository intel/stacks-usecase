#!/usr/bin/env bash

# Copyright (c) 2019 Intel Corporation
# Copyright 2018 The Kubeflow Authors
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


function get_ip() {
    EXTERNAL_IP=$(kubectl get service $1 -n kubeflow | awk '{print $4}' | tail -n 1)
    while [[ ${EXTERNAL_IP} == "<pending>" ]]; do
        EXTERNAL_IP=$(kubectl get service $1 -n kubeflow | awk '{print $4}' | tail -n 1)
    done
}

function cluster_connect() {
    if [ -z "${CLUSTER_NAME}" ]; then
      CLUSTER_NAME=$(wget -q -O- --header="Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/attributes/cluster-name)
    fi
    
    # Ensure the server name is not more than 63 characters.
    SERVER_NAME="${SERVER_NAME:0:63}"
    # Trim any trailing hyphens from the server name.
    while [[ "${SERVER_NAME:(-1)}" == "-" ]]; do SERVER_NAME="${SERVER_NAME::-1}"; done
    
    echo "Deploying ${SERVER_NAME} to the cluster ${CLUSTER_NAME}"
    
    # Connect kubectl to the local cluster
    kubectl config set-cluster "${CLUSTER_NAME}" --server=https://kubernetes.default --certificate-authority=/var/run/secrets/kubernetes.io/serviceaccount/ca.crt
    kubectl config set-credentials pipeline --token "$(cat /var/run/secrets/kubernetes.io/serviceaccount/token)"
    kubectl config set-context kubeflow --cluster "${CLUSTER_NAME}" --user pipeline
    kubectl config use-context kubeflow
}

function deploy() {
    if [ "${stage}" == "serve" ]; then
        echo "Deploying MODEL SERVER"
        sed -i "s/model\-bucket/${bucket}/g" /workdir/manifests/model-server.yaml
        sed -i "s/gcloud\_access\_token/${token}/g" /workdir/manifests/model-server.yaml
        kubectl create -f /workdir/manifests/model-server.yaml
        kubectl expose deployment -n kubeflow dlrs-mnist-model-server --type LoadBalancer --port 5059 --target-port 5059
        echo "Getting API's External IP" && get_ip "dlrs-mnist-model-server"
        echo "Finish with API's External IP: ${EXTERNAL_IP}"
    elif [ "${stage}" == "website" ]; then
        echo "Deploying WEBSITE"
        MODEL_EXTERNAL_IP=$(kubectl get service dlrs-mnist-model-server -n kubeflow | awk '{print $4}' | tail -n 1)
        echo "API's External IP: ${MODEL_EXTERNAL_IP}"
        sed -i "s/inference\_API\_endpoint/${MODEL_EXTERNAL_IP}/g" /workdir/manifests/website.yaml
        kubectl create -f /workdir/manifests/website.yaml
        kubectl expose deployment -n kubeflow dlrs-mnist-website --type LoadBalancer --port 8080 --target-port 5000
        echo "Getting Website's External IP" && get_ip "dlrs-mnist-website"
        echo "Website URL : ${EXTERNAL_IP}:8080"
    fi
}

while getopts "b:s:t:" opt; do
    case $opt in
        b)
            bucket=$OPTARG
            ;;
        s)
            stage=$OPTARG
            ;;
        t)
            token=$OPTARG
            ;;
        \?)
            echo "Invalid option: -$OPTARG" >&2
            ;;
        :)
            echo "Option -$OPTARG requires an argument." >&2
            ;;
    esac
done

echo "Connecting kubectl to local cluster" && cluster_connect
echo "Deploying ${stage} stage" && deploy
