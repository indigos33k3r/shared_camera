# shared camera

use webcam in several processes at once

# install

    apt-get install python-opencv
    pip install imutils
    pip install shared_camera


# usage

if you do not know if there is a camera running do

    from shared_camera import Camera

    c = Camera()
    frame = c.get()

this will try to connect to an open camera, on fail it will open the camera
and share the stream

if you know there is no camera currently open, you can open a share camera

    from shared_camera.server import CameraServer

    c = CameraServer()
    frame = c.get_frame()
    c.stop_stream()
    c.start_stream()
    sleep(5)
    c.shutdown()

if you know a camera is open and need to get frames from it

        from shared_camera.client import CameraClient

    c = CameraClient()
    frame = c.get()

raspberry pi usage

    from shared_camera import Camera
    from imutils.video import VideoStream

    camera = Camera(VideoStream(src=0, usePiCamera=True)