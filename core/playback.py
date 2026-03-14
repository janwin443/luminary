from uuid import uuid4

from core.cue_engine import CueEngine


class Playback:
    def __init__(self, cue_engine: CueEngine, name):
        self.cue_ids = []
        self.current_index = -1
        self.name = name
        self.cue_engine = cue_engine
        self._level = 1.0
        self.loop = False
        self.id = str(uuid4())
        self.cue_engine.merger.add_playback(self.id)
        self.cue_engine.merger.set_level(self.id, self._level)

    def add_cue(self, cue_id):
        self.cue_ids.append(cue_id)

    def go_next(self):
        self.current_index += 1
        if self.current_index >= len(self.cue_ids):
            if self.loop:
                self.current_index = 0
            else:
                self.current_index = len(self.cue_ids) - 1
                return
        self.go_to(self.current_index)

    def go_to(self, index):
        self.cue_engine.go(self.cue_ids[index])

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        self._level = max(0.0, min(1.0, value))
        self.cue_engine.merger.set_level(self.id, self._level)