import random

from nabard.engine import TurnEngine
from nabard.robot import Robot


class SampleRobot(Robot):
    def step(self, data):
        return f"echo: {data}"


class SampleEngine(TurnEngine):
    def step(self, robot):
        data = random.randint(1, 1000)
        resp = yield str(data)
        assert resp == f"echo: {data}"

    def end(self):
        return "DRAW"


def test__turn_engine():
    eng = SampleEngine(SampleRobot("robot_1"), SampleRobot("robot_2"))

    eng.run()
