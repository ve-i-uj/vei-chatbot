#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Входная точка для запуска бота."""

from __future__ import unicode_literals

import argparse
import logging

from chatbot.misc import log
from chatbot import pizzaorder


def read_args():
    """Прочитать аргументы командной стоки."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--ui', dest='ui', type=str, choices=['cli', 'tlgrm'],
                        help='User Interface of the bot')
    parser.add_argument('--log-level-name', dest='log_level', type=str,
                        choices=[n for n in logging._levelNames.values() if isinstance(n, str)],
                        help='Logging level')
    parser.set_defaults(log_level='ERROR',
                        ui='cli')

    return parser.parse_args()


def main():
    namespace = read_args()
    
    log.setup_root_logger(namespace.log_level)
    if namespace.ui == 'cli':
        from chatbot.ui import cli
        ui = cli.CLI(model_cls=pizzaorder.PizzaOrderModel)
        ui.run()
    elif namespace.ui == 'tlgrm':
        from chatbot.ui import tlgrm
        ui = tlgrm.TelegramUI(model_cls=pizzaorder.PizzaOrderModel)
        ui.run()
        

if __name__ == '__main__':
    main()
