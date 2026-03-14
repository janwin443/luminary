from ofl import Fixture, Attribute
from htp_merger import HTPMerger

class FixtureEngine:
    def __init__(self, merger: HTPMerger):
        self.fixtures = {}
        self.merger = merger

    def add_fixture(self, fixture, universe, start_address):
        self.fixtures[fixture.id] = (fixture, universe, start_address)
        self.merger.add_playback(fixture.id)
        self.merger.set_level(fixture.id, 1.0)

    def set_attribute(self, fixture_id, attribute, value):
        fixture, universe, start_address = self.fixtures[fixture_id]
        for ch in fixture.channels:
            if ch.attribute.value == attribute or ch.attribute == attribute:
                dmx_channel = start_address + fixture.channels.index(ch)
                self.merger.set_channel(fixture_id, dmx_channel, value)

    def _get_dmx_channel(self, fixture_id, attribute):
        fixture, universe, start_address = self.fixtures[fixture_id]
        for ch in fixture.channels:
            if ch.attribute.value == attribute or ch.attribute == attribute:
                return start_address + fixture.channels.index(ch)
            return None