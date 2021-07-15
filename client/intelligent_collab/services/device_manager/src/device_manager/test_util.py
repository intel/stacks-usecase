import util

def test_exec():
    out, err = util.exec('ls')
    assert len(out) > 0
    assert err == ''

def test_create_camera():
    out, err = util.create_camera()
    assert out != ''
    assert err == ''

def test_get_video_resolutions():
    resolutions = util.get_video_resolutions(0)
    assert len(resolutions) > 0

def test_get_cameras_list_all_cameras():
    cameras = util.get_cameras_list(all_cameras=True)
    assert len(cameras) > 0

def test_get_cameras_list():
    cameras = util.get_cameras_list()
    assert len(cameras) > 0

def test_get_camera():
    camera = util.get_camera(1)
    assert '/dev/video1' in camera['devices']

def test_delete_camera():
    out, err = util.delete_camera()
    assert out == err == ''
