# -*- coding: utf-8 -*-
import socket

from battlefield.engine.base import Engine


class TurnEngine(Engine):
    """
    TurnEngine is for turn-based games.
    """

    turn_timeout = 1  # default timeout is 1 second
    turns = 100

    def pre_step(self, robot):
        raise NotImplementedError()

    def post_step(self, robot, response):
        raise NotImplementedError()

    def end(self):
        raise NotImplementedError()

    def run(self):
        super(TurnEngine, self).run()
        self.robot1.sock.settimeout(self.turn_timeout)
        self.robot2.sock.settimeout(self.turn_timeout)
        for i in range(1, self.turns + 1):
            for robot in (self.robot1, self.robot2):
                data = self.pre_step(robot)
                self.send(b'[ENGINE] ' + data)
                robot.sock.send(data.encode())
                try:
                    response = robot.sock.recv(1048576).decode()  # 1 KiB
                    self.send(b'[ROBOT] ' + response)
                    self.post_step(robot, response)
                except socket.timeout:
                    robot.sock.send(b'TIMEOUT')

        result = self.end()
        self.send(b'[ENGINE] ' + result)
