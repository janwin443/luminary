import time, os
from pathlib import Path
from core.dmx_engine import DMXEngine
from core.fixture_engine import FixtureEngine
from core.programmer import Programmer
from core.cue_engine import CueEngine
from core.playback import Playback
from ofl import Lexer, Parser, Resolver, Validator, Builder

os.chdir(Path(__file__).parent.parent)

# Fixture laden
source = Path("fixtures/test.ofl").read_text()
tokens = Lexer(source).tokenize()
ast = Parser(tokens).parse()
resolved = Resolver(Path("fixtures/")).resolve(ast, Path("fixtures/test.ofl"))
Validator().validate(resolved)
fixture = Builder.build(resolved)

# Alles aufbauen
engine = DMXEngine("192.168.178.74", universe=0)
engine.merger.set_level("master", 1.0)
engine.start()

fixture_engine = FixtureEngine(engine.merger)
fixture_engine.add_fixture(fixture, universe=0, start_address=0)
programmer = Programmer(engine.merger, fixture_engine)
cue_engine = CueEngine(engine.merger, programmer, fixture_engine)

# Cue 1 – voll
programmer.set(fixture.id, "intensity", 255)
cue1 = cue_engine.record("Full", fade_time=2.0)
programmer.clear()

# Cue 2 – halb
programmer.set(fixture.id, "intensity", 128)
cue2 = cue_engine.record("Half", fade_time=2.0)
programmer.clear()

# Cue 3 – aus
programmer.set(fixture.id, "intensity", 0)
cue3 = cue_engine.record("Out", fade_time=2.0)
programmer.clear()

# Playback Stack
playback = Playback(cue_engine, "Main")
playback.add_cue(cue1)
playback.add_cue(cue2)
playback.add_cue(cue3)

# Abspielen
print("Cue 1 – Full")
playback.go_next()
time.sleep(4)

print("Cue 2 – Half")
playback.go_next()
time.sleep(4)

print("Cue 3 – Out")
playback.go_next()
time.sleep(4)

engine.stop()