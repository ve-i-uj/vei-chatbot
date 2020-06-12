#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Входная точка для запуска бота."""

import argparse
import logging

from chatbot.misc import log
from chatbot import pizzaorder


def read_args():
    """Прочитать аргументы командной стоки."""
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--ui', dest='ui', type=str, choices=['cli', 'telegram'],
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
        ui = cli.CLI()
        _model = pizzaorder.PizzaOrderModel(uid=1, user_interface=ui)
        ui.run()
    elif namespace.ui == 'telegram':
        pass
        

if __name__ == '__main__':
    main()
