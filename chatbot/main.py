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
            state_clses=pizzaorder.pizza_order_state_clses,
            user_interface=ui
        )
        ui.run()
#     log.setup_root_logger('DEBUG')
#     logging.getLogger('transitions').setLevel(logging.ERROR)
#     model = pizzaorder.PizzaOrderModel(1, pizzaorder.pizza_order_state_clses)
#     model.on_get_message(u'Большую')
#     model.on_get_message(u'Картой')
#     model.on_get_message(u'хз')
#     model.on_get_message(u'да')
    

if __name__ == '__main__':
    main()
