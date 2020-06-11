# -*- coding: utf-8 -*-
"""Модель FSM для работы с заказом пиццы."""

import logging

import attr
import transitions

from chatbot import common
from chatbot.pizzaorder import state

logger = logging.getLogger(__name__)


@attr.s
class PizzaOrder(object):
    uid = attr.ib(type=int, default=None)
    size = attr.ib(type=str, default=None)
    payment_method = attr.ib(type=str, default=None)
    confirmed = attr.ib(type=bool, default=False)


class PizzaOrderModel(common.IMessageHandler):

    def __init__(self, uid):
        self._pizza_order = PizzaOrder(uid=uid)

        def on_enter_cb():
            """Отправка сообщения при входе в состояние"""
            state_inst = self.machine.get_state(self.state)
            msg = state_inst.build_init_message(self._pizza_order)
            self.send_message(msg)

        states = []
        conditions=[]
        for state_cls in state.pizza_order_state_clses:
            inst = state_cls(name=state_cls.state,
                             on_enter=on_enter_cb)
            states.append(inst)

        self.machine = transitions.Machine(
            model=self, states=states, initial=state.StateEnum.GREETING
        )
        self.machine.add_ordered_transitions()
        
        self.init()

    def init(self):
        # дернем руками приветсвенное сообщение начального состояния
        state_inst = self.machine.get_state(self.state)
        msg = state_inst.build_init_message(self._pizza_order)
        self.send_message(msg)
        # И переходим в следующее состояние
        self.next_state()

    def on_get_message(self, msg):
        """Метод срабатывает, когда получено сообщение."""
#         logger.debug(u'msg = %s', msg)
        logger.debug(msg)
        state_inst = self.machine.get_state(self.state)
        try:
            state_inst.validate(msg)
        except common.ValidateException as err:
            hint = err.message
            self.send_message(hint)
            return
        
        if state_inst.state == state.StateEnum.WAITING_FOR_PIZZA_SIZE:
            self._pizza_order.size = msg
        elif state_inst.state == state.StateEnum.WAITING_FOR_PAYMENT_METHOD:
            self._pizza_order.payment_method = msg
        elif state_inst.state == state.StateEnum.WAITING_FOR_CONFIRM:
            if msg.strip().lower() == u'да':
                self._pizza_order.confirmed = True
            else:
                # TODO: (burov_alexey@mail.ru 11 июн. 2020 г. 13:58:47) 
                # Перекидываем его на узел изменения заказа
                return
        
        self.next_state()
                
    
    def send_message(self, msg):
        """Отправить сообщение."""
#         logger.debug(u'msg = %s', msg)
        logger.debug(msg)


# config = {
#     'states': ['greeting', 'waiting_for_pizza_size', 'error'],
#     'transitions': {
#         'trigger': 'melt',
#         'source': 'solid',
#         'dest': 'liquid',
#         'before': 'make_hissing_noises'
#     },
# }

#         # уникальный идентификатор пользователя
#         self._uid = uid
#         # стек состояния, чтобы можно было откатиться к предыдущему
#         self._state_stack = []
#         self._help = 'You can back to the previous state or cancel your order.'
#         self._error_msg = None


#     def on_enter_state(self):
#         self._state_stack.append(self.state)
# 
#     def on_exit_state(self):
#         if self._state_stack[-1] == self.state:
#             self._state_stack.pop()
#         else:
#             # TODO: (burov_alexey@mail.ru 11 июн. 2020 г. 10:08:36) 
#             # Хотя такой ситуации не должно быть
#             self._state_stack.remove(self.state)


# transitions = [
#     ['proceed', States.GREETING, States.WAITING_FOR_PIZZA_SIZE],
#     ['proceed', States.WAITING_FOR_PIZZA_SIZE, States.WAITING_FOR_PAYMENT_METHOD],
#     ['proceed', States.WAITING_FOR_PAYMENT_METHOD, States.WAITING_FOR_CONFIRM],
#     ['proceed', States.WAITING_FOR_CONFIRM, States.GRATITUDE],
#     ['privious', States.WAITING_FOR_CONFIRM, States.WAITING_FOR_PAYMENT_METHOD],
#     ['privious', States.WAITING_FOR_PAYMENT_METHOD, States.WAITING_FOR_PIZZA_SIZE],
#     ['error', '*', States.ERROR],
# ]

