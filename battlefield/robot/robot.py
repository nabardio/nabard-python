# -*- coding: utf-8 -*-


class Robot(object):
    def __init__(self):
        self.sock = None

    def step(self, data):
        raise NotImplementedError()

    @classmethod
    def name(cls):
        return cls.__name__

    def run(self):
        if 'sock' not in self.__dict__:
            raise Exception("the socket has not been injected")
        while True:
            data = self.sock.recv(1048576).decode()  # 1 KiB
            res = self.step(data)
            self.sock.send(res.encode())
