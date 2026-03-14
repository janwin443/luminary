import threading
import time

from artnet import ArtNetSender
from htp_merger import HTPMerger

class DMXEngine:
    def __init__(self, ip, universe):
        self.artnet = ArtNetSender(ip=ip, universe=universe)
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._stop_event = threading.Event()
        self.merger = HTPMerger()
        self.merger.add_playback("master")

    def start(self):
        self.artnet.connect()
        self._thread.start()

    def stop(self):
        self._stop_event.set()
        self._thread.join()
        self.artnet.close()

    def set_channel(self, channel, value):
        self.merger.set_channel("master", channel, value)

    def _loop(self):
        while not self._stop_event.is_set():
            self.artnet.send_dmx(self.merger.merge())
            time.sleep(1/44)