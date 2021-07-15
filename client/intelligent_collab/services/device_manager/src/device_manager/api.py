from fastapi import FastAPI
import uvicorn

import config, util

app = FastAPI()


@app.get("/ping")
async def ping():
    """ping function"""
    return {"message": "Ok"}


@app.get("/cameras")
async def list_cameras():
    """list_cameras function"""
    return util.get_cameras_list()


@app.post("/cameras")
async def create_camera():
    """create_camera function"""
    cameras = util.get_cameras_list(all_cameras=True)
    icollab_cameras = [camera for camera in cameras if camera["label"] == "icollab"]

    if icollab_cameras:
        device_id = icollab_cameras[0]['devices'][0][-1:]
    else:
        device_id, err = util.create_camera()
        # TODO: handle error

    return {
        "device_id": device_id.rstrip(),
    }


@app.get("/cameras/{camera_id}")
async def get_camera(camera_id):
    """get_camera function"""
    return util.get_camera(camera_id)


@app.delete("/cameras/{camera_id}")
async def delete_camera(camera_id):
    """delete_camera function"""
    util.delete_camera()
    return {"message": "Delete camera device"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=config.API_PORT)
