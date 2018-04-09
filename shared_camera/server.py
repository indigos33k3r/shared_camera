from multiprocessing import Queue
from multiprocessing.managers import SyncManager
from imutils.video import VideoStream
import cv2
from os.path import join, dirname
from threading import Thread


class CameraServer(object):
    def __init__(self, stream=None, host="", port=5011, authkey="666",
                 name="camera server",
                 description="shared camera feed", stock=None, callback=None):
        stock = stock or join(dirname(__file__), "no_feed.jpg")

        if callback is not None:
            self.send_notification = callback
        # create connected manager
        self.server = CreateFrameServer(host, port, authkey, name,
                                        description)
        try:
            self.last_frame = cv2.imread(stock)
        except:
            self.last_frame = None
        self.streaming = False
        self.stream = stream or VideoStream()
        self.stream.start()
        self.t = None
        self.start_stream()

    def send_notification(self, notification):
        print notification

    def stop_stream(self):
        self.send_notification("camera.stop")
        self.streaming = False
        if self.t is not None:
            self.t.join(3)
        self.stream.stop()
        self.send_notification("camera.stopped")

    def start_stream(self):
        self.send_notification("camera.open")
        self.streaming = True
        if self.t is not None:
            self.t.join(3)
        else:
            self.t = Thread(target=self.read_stream)
            self.t.setDaemon(True)
        self.t.start()
        self.stream.start()

        self.send_notification("camera.opened")

    def read_stream(self):
        while self.streaming:
            self.put_frame(self.stream.read().copy())

    def put_frame(self, frame=None):
        if frame is not None:
            q = self.server.get_queue()
            # keep one frame only
            try:
                while q.qsize():
                    self.last_frame = q.get_nowait().copy()
            except Exception as e:
                pass
            q.put_nowait(frame.copy())
            self.last_frame = frame.copy()

    def get_frame(self):
        # Get the queue object
        try:
            q = self.server.get_queue()
            return q.get()
        except Exception as e:
            return self.last_frame

    def shutdown(self):
        self.stop_stream()


def CreateFrameServer(HOST, PORT, AUTHKEY, name = None, description = None):
    name = name
    description = description
    q = Queue()

    class FrameManager(SyncManager):
        pass

    FrameManager.register('get_queue', callable = lambda: q)
    FrameManager.register('get_name', callable = name)
    FrameManager.register('get_description', callable = description)
    manager = FrameManager(address = (HOST, PORT), authkey = AUTHKEY)
    manager.start() # This actually starts the server

    return manager

