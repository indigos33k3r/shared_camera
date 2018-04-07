from shared_camera.server import CameraServer
from shared_camera.client import CameraClient


class Camera(object):
    def __init__(self, stream=None, host="", port=5011, authkey="",
                 stock=None):
        self.is_main = False
        # can we start camera?
        try:
            print "attempting to serve camera"
            # take role of camera server
            self._camera = CameraServer(stream, host, port, authkey,
                                        stock=stock)
            self.is_main = True
            print "serving camera"
        except Exception as e:
            print "failed to serve camera, attempting to connect"
            self._camera = CameraClient(host, port, authkey)
            print "connected to camera"

    def get(self):
        return self._camera.get_frame()

    def stop_stream(self):
        if self.is_main:
            self._camera.stop_stream()

    def start_stream(self):
        if self.is_main:
            self._camera.start_stream()

    def shutdown(self):
        if self.is_main:
            self._camera.shutdown()

