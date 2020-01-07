#!/usr/bin/env bash

function usage() {
    cat << EOF
\$ $(basename $0) OPTIONS [SERIES]

where OPTIONS are

    -b <bucket> : GCP Storage Bucket where your pretrained model will be accessed
    -c <cloud>  : Set cloud mode
    -s <stage>  : Stage to deploy <train or serve>
    -t <token>  : GCP Access token --> `gcloud auth print-access-token`

EOF
>&2

    exit 1
}

function fetch_model() {
    echo "Fetching model from ${bucket}"
    curl -H "Authorization: Bearer ${token}" \
    https://www.googleapis.com/storage/v1/b/${bucket}/o/mnist_cnn.pt?alt=media \
    --output /workdir/models/mnist_cnn.pt
}

function upload_model() {
    echo "Uploading model to ${bucket}"
    curl -v --upload-file /workdir/models/mnist_cnn.pt \
    -H "Authorization: Bearer ${token}" \
    https://storage.googleapis.com/${bucket}/mnist_cnn.pt
}

while getopts "cb:s:t:h" opt; do
    case $opt in
	b)
	    bucket=$OPTARG
	    ;;
	c)
	    cloud=true
	    ;;
	s)
	    stage=$OPTARG
	    ;;
	t)
	    token=$OPTARG
	    ;;
	h)
	    usage
	    ;;
	\?)
	    echo "Invalid option: -$OPTARG" >&2
	    usage
	    ;;
	:)
	    echo "Option -$OPTARG requires an argument." >&2
	    usage
	    ;;
    esac
done

if [[ ! -d "/workdir/models/" ]]; then
    mkdir /workdir/models/
fi

cd python/

if [[ ${cloud} ]]; then
    echo "Deploying ${stage} stage on cloud mode"
    if [[ ${stage} == "serve" ]]; then
        fetch_model && python ${stage}.py
    elif [[ ${stage} == "train" ]]; then
        python ${stage}.py && upload_model
    fi
else
    echo "Deploying ${stage} stage"
    python ${stage}.py
fi
