from shared_camera.server import CameraServer
from shared_camera.client import CameraClient


class Camera(object):
    def __init__(self, stream=None, host="", port=5011, authkey="",
                 stock=None):
        self.is_main = False
        # can we start camera?
        try:

            # take role of camera server
            self._camera = CameraServer(stream, host, port, authkey,
                                        stock=stock)
            self.is_main = True
        except Exception as e:
            self._camera = CameraClient(host, port, authkey)

    def set_notification_callback(self, callback):
        self._camera.send_notification = callback

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
            self.stop_stream()
            self._camera.shutdown()


