from dataclasses import dataclass
from uuid import uuid4
import threading, time

from core.fixture_engine import FixtureEngine
from programmer import Programmer
from htp_merger import HTPMerger

@dataclass
class Cue:
    id:        str
    name:      str
    fade_time: float
    data:      dict    # {(fixture_id, attribute): value}

class CueEngine:
    def __init__(self, merger: HTPMerger, programmer: Programmer, fixture_engine: FixtureEngine):
        self.merger = merger
        self.programmer = programmer
        self.fixture_engine = fixture_engine
        self.cues = {}

    def record(self, name, fade_time):
        data = self.programmer.capture()
        cue = Cue(id=str(uuid4()), name=name, fade_time=fade_time, data=data)
        self.cues[cue.id] = cue
        return cue.id

    def go(self, cue_id):
        cue = self.cues[cue_id]
        t = threading.Thread(target=self._fade, args=(cue,), daemon=True)
        t.start()

    def _fade(self, cue):
        steps = int(cue.fade_time * 44)
        if steps == 0:
            steps = 1

        # Startwerte sammeln
        start_values = {}
        for (fixture_id, attribute) in cue.data:
            dmx_ch = self.fixture_engine._get_dmx_channel(fixture_id, attribute)
            if dmx_ch is not None:
                start_values[(fixture_id, attribute)] = self.merger.buffers[fixture_id][dmx_ch]

        # Faden
        for step in range(steps + 1):
            for (fixture_id, attribute), target in cue.data.items():
                start = start_values.get((fixture_id, attribute), 0)
                value = int(start + (target - start) * (step / steps))
                self.fixture_engine.set_attribute(fixture_id, attribute, value)
            time.sleep(1 / 44)