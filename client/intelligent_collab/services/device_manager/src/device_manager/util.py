import subprocess

def exec(cmd):
    process = subprocess.Popen(cmd.split(),
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               universal_newlines=True)
    return process.communicate()

def get_video_resolutions(device):
    resolutions = []
    out, err = exec('v4l2-ctl  -d {} --list-formats-ext'.format(device))
    output_format = {}

    for line in out.split('\n'):
        if line:
            if line.find('[') > 0:
                if output_format != {}:
                    resolutions.append(output_format)
                name = line.split('\'')[1]
                output_format = {
                    'format': name,
                    'resolutions': [],
                }
            elif line.find('Size') > 0 and output_format != {}:
                resolution = line.split()[-1]
                output_format['resolutions'].append(resolution)

    if output_format != {}:
        resolutions.append(output_format)

    return resolutions

def get_cameras_list(all_cameras=False):
    cameras = []
    out, err = exec('v4l2-ctl --list-devices')
    camera = {}

    for line in out.split('\n'):
        if line:
            if not line.find('/dev/') >= 0:
                if camera != {}:
                    if camera['label'] != 'icollab' or all_cameras:
                        cameras.append(camera)
                [label, bus_info] = line.split(' (')
                camera = {
                    'label': label,
                    'bus_info': bus_info[:-2],
                    'devices': [],
                    'resolutions': []}
            else:
                device = line.strip()
                camera['devices'].append(device)
                resolutions = get_video_resolutions(device)
                if resolutions:
                    camera['resolutions'] += resolutions

    if camera != {}:
        cameras.append(camera)
    return cameras

def get_camera(device_id):
    matched_devices = [camera for camera in get_cameras_list()
                       if '/dev/video{}'.format(device_id) in camera['devices']
                       ]
    camera = {}
    if matched_devices:
        camera = matched_devices[0]

    return camera

def create_camera():
    return exec('./scripts/enable_virtual_camera.sh')

def delete_camera():
    # TODO: Investigate a method to delete a single device
    return exec('sudo rmmod v4l2loopback')
