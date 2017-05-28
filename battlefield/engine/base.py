# -*- coding: utf-8 -*-
import json
import socket
import sys
import multiprocessing as mp

import pika

from battlefield.engine.robot import Robot
from .config import Config


class Engine(object):
    """
    Engine is the base class of a game engine that creates a connection to a
    rabbitMQ and is able to send message to a queue.
    """

    PREFIX = 'BATTLEFIELD'

    def __init__(self, robot1, robot2):
        self.conf = Config(Engine.PREFIX)

        self.robot1 = Robot(robot1.name())
        self.robot2 = Robot(robot2.name())
        self.robot1.sock, robot1.sock = socket.socketpair()
        self.robot2.sock, robot2.sock = socket.socketpair()
        self.robot1.proc = mp.Process(target=robot1.run)
        self.robot2.proc = mp.Process(target=robot2.run)

        try:
            self._mq_connection = pika.SelectConnection(
                pika.ConnectionParameters(
                    host=self.conf.MQ_HOST,
                    virtual_host=self.conf.MQ_VHOST,
                    credentials=pika.PlainCredentials(
                        username=self.conf.MQ_USERNAME,
                        password=self.conf.MQ_PASSWORD
                    )
                ),
                on_open_callback=self._on_connection_open,
            )
        except Exception as e:
            print(e)
            sys.exit(1)

    def _on_connection_open(self, connection):
        self._mq_channel = connection.channel(self._on_channel_open)

    def _on_channel_open(self, channel):
        self._mq_channel = channel
        channel.basic_qos(prefetch_count=1)
        channel.queue_declare(queue=self.name(), auto_delete=True)

    @classmethod
    def name(cls):
        """
        Name the class that is calling this method
        """
        return cls.__name__

    def send(self, message):
        """
            sends a message to the queue
        """
        self._mq_channel.basic_publish(exchange='',
                                       routing_key=self.name(),
                                       body=json.dumps(message))

    def run(self):
        """
            Runs the engine
        """
        self.robot1.proc.start()
        self.robot2.proc.start()
        self._mq_connection.ioloop.start()
