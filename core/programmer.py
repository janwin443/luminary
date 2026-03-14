from core.htp_merger import HTPMerger


class Programmer:
    def __init__(self, merger: HTPMerger, fixture_engine):
        self._data = {}
        self.merger = merger
        self.merger.add_playback("programmer")
        self.merger.set_level("programmer", 1.0)
        self.fixture_engine = fixture_engine

    def set(self, fixture_id, attribute, value):
        self._data[(fixture_id, attribute)] = value
        dmx_channel = self.fixture_engine._get_dmx_channel(fixture_id, attribute)
        if dmx_channel is not None:
            self.merger.set_channel("programmer", dmx_channel, value)

    def clear(self):
        self._data = {}
        self.merger.buffers["programmer"] = bytearray(512)

    def capture(self):
        return self._data.copy()