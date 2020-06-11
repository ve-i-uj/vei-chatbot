# -*- coding: utf-8 -*-
"""Настройки логирования."""

import logging
import sys

FORMAT = u'%(levelname)-7s [%(filename)s:%(lineno)s - %(funcName)s()] %(message)s'


def setup_root_logger(level_name):
    level = logging.getLevelName(level_name)
    logger = logging.getLogger()
    logger.setLevel(level)
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(FORMAT)
    stream_handler.setFormatter(formatter)
    logger.handlers = [stream_handler]
