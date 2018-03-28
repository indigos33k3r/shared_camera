from multiprocessing.managers import SyncManager
from imutils.video import VideoStream


class SharedCamera(SyncManager):
    def __init__(self, stream=None, address=("127.0.0.1", 5000), authkey=""):
        super(SharedCamera, self).__init__(address, authkey)
        self.stream = stream or VideoStream()
        self.register("get", self.get_stream)
        self.start_stream()
        self.start()

    def get_stream(self):
        return self.stream.read()

    def start_stream(self):
        self.stream.start()

    def stop_stream(self):
        self.stream.stop()


class CameraFeed(SyncManager):
    def __init__(self, address=("127.0.0.1", 5000), authkey=""):
        super(CameraFeed, self).__init__(address, authkey)
        self.register("get")
        self.connect()


class Camera(object):
    def __init__(self, stream=None, address=("127.0.0.1", 5000), authkey=""):
        self.address = address
        self.authkey = authkey
        self.is_main = False
        self._camera_server = None
        # can we connect?
        try:
            self._camera = CameraFeed(address, authkey)
            self._camera.get()
        except Exception as e:
            # no camera server to connect, take the role of server
            self._camera_server = SharedCamera(stream=stream, address=address,
                                               authkey=authkey)
            self.is_main = True

    def get(self):
        if self.is_main:
            return self._camera_server.get_stream().copy()
        return self._camera.get().copy()

    def stop_stream(self):
        if self.is_main:
            self._camera_server.stop_stream()

    def start_stream(self):
        if self.is_main:
            self._camera_server.start_stream()

    def shutdown(self):
        if self.is_main:
            self._camera_server.shutdown()
