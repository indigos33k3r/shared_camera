from multiprocessing.managers import SyncManager


class CameraClient(object):
    def __init__(self, host="", port=5011, authkey="666"):
        # create connected manager
        self.send_notification("camera.connect")
        self.server = FrameServerClient(host, port, authkey)
        try:
            # do not require opencv in clients
            import cv2
            from os.path import join, dirname
            self.last_frame = cv2.imread(join(dirname(__file__),
                                              "no_feed.jpg"))
        except:
            self.last_frame = None
        self.send_notification("camera.connected")

    def get_frame(self):
        # Get the queue object
        try:
            q = self.server.get_queue()
            return q.get()
        except Exception as e:
            pass

    def send_notification(self, notification):
        print notification


def FrameServerClient(HOST, PORT, AUTHKEY):
    class FrameManager(SyncManager):
        pass
    FrameManager.register('get_queue')
    FrameManager.register('get_name')
    FrameManager.register('get_description')
    manager = FrameManager(address = (HOST, PORT), authkey = AUTHKEY)
    manager.connect() # This starts the connected client
    return manager
