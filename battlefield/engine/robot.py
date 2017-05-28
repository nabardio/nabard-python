# -*- coding: utf-8 -*-


class Robot(object):
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.sock = None
        self.proc = None
