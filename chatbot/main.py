#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Входная точка для запуска бота."""

import logging

from chatbot.misc import log
from chatbot import pizzaorder

def main():
    # TODO: (burov_alexey@mail.ru 11 июн. 2020 г. 19:59:30) 
    # нужно логер выставлять в ERROR при cli, чтобы не фонил

#     log.setup_root_logger('ERROR')
    if True:
        from chatbot.ui import cli
        ui = cli.CLI()
        model = pizzaorder.PizzaOrderModel(
            uid=1,
            user_interface=ui
        )
        ui.run()
    

if __name__ == '__main__':
    main()
