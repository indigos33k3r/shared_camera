from shared_camera.server import CameraServer
from shared_camera.client import CameraClient


class Camera(object):
    def __init__(self, stream=None, host="", port=5011, authkey="",
                 stock=None, autostart=True):
        self.stream = stream
        self.host = host
        self.port = port
        self.authkey = authkey
        self.stock = stock
        if autostart:
            self.start()

    def start(self):
        self.is_main = False
        # can we start camera?
        try:

            # take role of camera server
            self._camera = CameraServer(self.stream, self.host, self.port,
                                        self.authkey, stock=self.stock)
            self.is_main = True
        except Exception as e:
            self._camera = CameraClient(self.host, self.port, self.authkey)

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


