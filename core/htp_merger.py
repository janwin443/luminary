class HTPMerger:
    def __init__(self):
        self.buffers = {}
        self.levels  = {}

    def add_playback(self, id):
        self.buffers[id] = bytearray(512)
        self.levels[id] = 0.0

    def set_level(self, id, level):
        self.levels[id] = max(0.0, min(1.0, level))

    def set_channel(self, id, channel, value):
        self.buffers[id][channel] = value

    def merge(self):
        output = bytearray(512)

        for i in range(512):
            for id, buf in self.buffers.items():
                scaled = int(buf[i] * self.levels[id])
                if scaled > output[i]:
                    output[i] = scaled


        return output