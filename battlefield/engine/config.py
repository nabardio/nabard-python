# -*- coding: utf-8 -*-
import os


class Config(object):
    """
        A basic configuration class containing required values that can be
        extended and override the default configurations.
    """

    def __init__(self, prefix):
        self.__conf = dict(
            MQ_HOST='localhost',
            MQ_VHOST='battlefield',
            MQ_USERNAME='username',
            MQ_PASSWORD='password',
        )
        for key in os.environ:
            if key.startswith(prefix + '_'):
                self.__conf[key] = os.environ[key]
                os.environ.unsetenv(key)

    def __getattr__(self, item):
        return self.__conf.get(item)
