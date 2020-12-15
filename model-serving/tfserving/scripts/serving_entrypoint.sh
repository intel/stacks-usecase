#! /usr/bin/env bash

# Uncomment below lines as required

# TensorFlow Serving basic configuration 
tensorflow_model_server --rest_api_port=8501 \
	--model_name=${MODEL_NAME} --model_base_path=${MODEL_DIR}/ \
       	"$@"

# TensorFlow Serving for multiple models
#tensorflow_model_server --rest_api_port=8501 \
#	--model_config_file=/workspace/multi_models.conf \
#        "$@"

# TensorFlow Serving for multiple versions
#tensorflow_model_server --rest_api_port=8501 \
#       --model_name=${MODEL_NAME} --model_base_path=${MODEL_DIR} \
#       --model_config_file=/workspace/multi_versions.conf \
#       --allow_version_labels_for_unavailable_models=true \
#	"$@"

# TensorFlow Serving for monitoring
#tensorflow_model_server --rest_api_port=8501 \
#	--model_name=${MODEL_NAME} --model_base_path=${MODEL_DIR}/ \
#	--monitoring_config_file=/workspace/monitoring.conf \
#        "$@"
