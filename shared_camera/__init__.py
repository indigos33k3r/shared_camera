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