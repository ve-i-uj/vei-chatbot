#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Входная точка для запуска бота."""

import logging

from chatbot.misc import log
from chatbot import pizzaorder


def main():
    log.setup_root_logger('DEBUG')
    logging.getLogger('transitions').setLevel(logging.ERROR)
    model = pizzaorder.PizzaOrderModel(1)
    model.on_get_message(u'Большую')
    model.on_get_message(u'Картой')
    model.on_get_message(u'да')
    

if __name__ == '__main__':
    main()
