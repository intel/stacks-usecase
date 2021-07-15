#!/usr/bin/python3

"""Runner for Intelligent Collaboration App"""

import sys
import subprocess
import json
import requests
import re
import time
import yaml
import os
import tarfile
import shutil
import threading


MODELS_DIR = os.environ.get("MODELS_DIR", "./saved_models")
# Format for models lists is [(file_url, directory_name), ...]
TAR_MODELS = [("https://tfhub.dev/tensorflow/ssd_mobilenet_v2/2\
?tf-hub-format=compressed", "ssd_mobilenet_v2_2"),
              ("https://tfhub.dev/google/magenta/arbitrary-image-stylization\
-v1-256/2?tf-hub-format=compressed",
               "magenta_arbitrary-image-stylization-v1-256_2")]
PB_MODELS = [("https://github.com/IntelAI/models/raw/master/models/object_\
detection/tensorflow/ssd-mobilenet/inference/ssdmobilenet_preprocess.pb",
              "ssdmobilenet_preprocess"),
             ("https://storage.googleapis.com/intel-optimized-tensorflow/\
models/v1_8/ssdmobilenet_int8_pretrained_model_combinedNMS_s8.pb",
              "ssdmobilenet_int8_pretrained_model_combinedNMS_s8")]
INT8_MODELS_PATH = "/ssd_mobilenet_int8"


def check_folder(folder):
    exists = os.path.isdir(folder)
    return exists


def wait_for_request(request):
    count = 0
    while request.ok is False and count < 100:
        time.sleep(2)
        count += 1
    if count == 100:
        print("ERROR: Model file " + file_path + " could not be downloaded.")
        return False
    return True


def download_targz_model(url, base_dir, model_dir):
    if not check_folder(base_dir + "/" + model_dir):
        os.makedirs(base_dir + "/" + model_dir)
    model = requests.get(url)
    completed = wait_for_request(model)
    if completed:
        with open(base_dir + "/" + model_dir + ".tar.gz", 'wb') as m:
            m.write(model.content)
        untar_model(base_dir + "/" + model_dir + ".tar.gz", base_dir + "/" +
                    model_dir)


def download_pb_model(url, base_dir, model_name):
    if not check_folder(base_dir + INT8_MODELS_PATH):
        os.makedirs(base_dir + INT8_MODELS_PATH)
    model = requests.get(url)
    completed = wait_for_request(model)
    if completed:
        with open(base_dir + INT8_MODELS_PATH + "/" + model_name + ".pb",
                  'wb') as m:
            m.write(model.content)
        print("INFO: Model is available at " + base_dir + INT8_MODELS_PATH)


def untar_model(file_path, target_path):
    model_tar = tarfile.open(file_path)
    model_tar.extractall(target_path)
    model_tar.close()
    os.remove(file_path)
    print("INFO: Model is available at " + target_path)


def download_models():
    # Create temporary directory
    if not check_folder(MODELS_DIR):
        os.makedirs(MODELS_DIR)
    for model in TAR_MODELS:
        model_exists = os.path.exists(MODELS_DIR + "/" + model[1] +
                                     "/" + "saved_model.pb")
        if not model_exists:
            thread = threading.Thread(target=download_targz_model(
                                      model[0], MODELS_DIR,
                                      model[1]))
            thread.daemon = True
            thread.start()
        else:
            print("INFO: Model " + model[1] + " found locally. Skipping \
download.")
    for model in PB_MODELS:
        model_exists = os.path.exists(MODELS_DIR + INT8_MODELS_PATH + "/" +
                                      model[1] + ".pb")
        if not model_exists:
            thread = threading.Thread(target=download_pb_model(
                                      model[0], MODELS_DIR,
                                      model[1]))
            thread.daemon = True
            thread.start()
        else:
            print("INFO: Model " + model[1] + " found locally. Skipping \
download.")


def clean_models():
    folder_exists = check_folder(MODELS_DIR)
    if folder_exists:
        try:
            shutil.rmtree(MODELS_DIR)
        except shutil.Error as e:
            print("WARNING: Could not remove temporary models directory. \
You might need to remove it manually.")
    print("INFO: All Intelligent Collaboration Models were removed.")


compose_file = './docker-compose.yml'


def register_services(backend_port: int):
    # Wait for main_controller API to be ready to accept requests
    time.sleep(2)
    with open(compose_file, 'r') as yml_file:
        compose = yaml.safe_load(yml_file)

    headers = {'Content-type': 'application/json',
               'accept': 'application/json'}

    net_name = list(compose['networks'].keys())[0]

    for svc_name, config in compose['services'].items():
        name = config['container_name']
        ip = config['networks'][net_name]['ipv4_address']
        port = 8000
        if svc_name != 'effects_controller':
            for env_var in config["environment"]:
                if env_var.startswith("API_PORT="):
                    port = int(env_var.split("=")[1])
                    break
        else:
            port = 80

        data = {
            "name": name,
            "ip": ip,
            "port": port
        }
        # Register service
        try:
            response = requests.post(f"http://localhost:{backend_port}/services/",
                                     data=json.dumps(data), headers=headers)
        except Exception as e:
            print(e)
            continue


def register_iccam(backend_port: int):
    headers = {'Content-type': 'application/json',
               'accept': 'application/json'}
    response = requests.post(f"http://localhost:{backend_port}/iccam/",
                             headers=headers)


def get_port_fwd():
    ui_port = None
    backend_port = None
    services = subprocess.check_output(['docker-compose', 'ps', '-a'])
    lines = services.decode().split("\n")
    for line in lines:
        if line.startswith('icollab-efx-control'):
            ui_port = int(line.split()[-1].split('->')[0].split(":")[1])
        if line.startswith('icollab-main-service'):
            backend_port = int(line.split()[-1].split('->')[0].split(":")[1])
        if ui_port and backend_port:
            break

    return ui_port, backend_port


def tear_down():
    stop_app()
    down_app()
    print("ERROR: Something went wrong, services were rolled back")
    sys.exit(1)


def start_app():
    if not os.path.exists(MODELS_DIR):
        os.mkdir(MODELS_DIR)
    result = subprocess.call(['docker-compose up -d'],
                             shell=True, stderr=subprocess.STDOUT)
    if result != 0:
        print("ERROR: docker-compose failed")
        tear_down()

    ui_port, backend_port = get_port_fwd()

    if not ui_port or not backend_port:
        print("ERROR: backend service is not well defined")
        tear_down()

    try:
        register_services(backend_port)
        register_iccam(backend_port)
    except:
        print("ERROR: backend service is not reachable")
        tear_down()

    try:
        download_models()
    except:
        print("ERROR: effect models couldn't be downloaded")
        tear_down()

    print(f"INFO: Intelligent Collaboration App started. Effects Controller \
UI is at http://localhost:{ui_port}, and backend API at http://localhost:{backend_port}/docs.")


def stop_app():
    subprocess.call(['docker-compose stop'],
                    shell=True, stderr=subprocess.STDOUT)
    print("INFO: Intelligent Collaboration App stopped")


def down_app():
    stop_app()
    subprocess.call(['docker-compose down'],
                    shell=True, stderr=subprocess.STDOUT)
    print("INFO: All Intelligent Collaboration Resources were removed. Downloa\
ded models are kept at " + MODELS_DIR + ". Use \"clean\" option to also remove\
 that directory.")


def list_services():
    subprocess.call(['docker-compose ps'],
                    shell=True, stderr=subprocess.STDOUT)


def display_help():
    print("\nThis script allows you to interact with Intelligent Collaboration\
.\n\nThere are 6 supported actions:\n\nstart - Initializes and start all Intel\
ligent Collaboration basic services.\n\nstop - Stops all running Intelligent C\
ollaboration services.\n\ndown - Stops and removes all Intelligent Collaborati\
on services and containers.\n\nlist - Lists all running services originated fr\
om current project directory.\n\nclean - Removes temporary directory where mo\
dels are saved.\n        By default, this script will look for the models loc\
ally and will\n        only attempt to download them if not found.\n\nhelp - \
Display this help.\n\nSyntaxis is as follows:\n\n    python icollab.py [start\
|stop|down|list|clean|help]\n\nAfter initializing the app, you can take a look\
 at the UI at\n\n    http://localhost:8080.\n\nBy default the port 8080 is ass\
igned to the UI and the port 8000 is assigned\nto the backend.\nIf you want to\
 use different ports use the environment variables UI_PORT and BACKEND_PORT r\
espectively.\n\nExample:\n\n    UI_PORT=8081 BACKEND_PORT=8001 python icollab.\
py start\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('ERROR: Please provide action to execute. Options are\
 \"start\", \"stop\", \"clean\", \"list\" and \"down\"')

    dcompose = subprocess.call(['docker-compose -v'], shell=True,
                               stdout=subprocess.PIPE)
    if dcompose != 0:
        print('ERROR: \"docker-compose\" not found. Please ensure that it is \
appropriately installed. Aborting icollab.')
        sys.exit()

    if (sys.argv[1] == "start" or sys.argv[1] == "--start"):
        start_app()
    elif (sys.argv[1] == "stop" or sys.argv[1] == "--stop"):
        stop_app()
    elif (sys.argv[1] == "clean" or sys.argv[1] == "--clean"):
        clean_models()
    elif (sys.argv[1] == "down" or sys.argv[1] == "--down"):
        stop_app()
        down_app()
    elif (sys.argv[1] == "list" or sys.argv[1] == "--list"):
        list_services()
    elif (sys.argv[1] == "help" or sys.argv[1] == "-h" or
          sys.argv[1] == "--help"):
        display_help()
    else:
        raise ValueError('ERROR: Action \"%s\" not recognized. Options are \
\"start\", \"stop\", \"down\" and \"list\".' % sys.argv[1])

    sys.exit()
