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
    """Данные заказа."""
    uid = attr.ib(type=int, default=None)
    size = attr.ib(type=str, default=None)
    payment_method = attr.ib(type=str, default=None)
    confirmed = attr.ib(type=bool, default=False)


class PizzaOrderModel(common.IMessageHandler):
    """Модель FSM для работы с заказом пиццы."""

    def __init__(self, uid, state_clses, user_interface):
        self._pizza_order = PizzaOrder(uid=uid)
        # экземпляр IUserInterface
        self._user_interface = user_interface
        self._user_interface.model = self

        def on_enter_cb():
            """Отправка сообщения при входе в состояние"""
            state_inst = self.machine.get_state(self.state)
            msg = state_inst.build_init_message(self._pizza_order)
            self.send_message(msg)

        states = []
        for state_cls in state_clses:
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
        logger.debug(u'msg = %s', msg)
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

                # (burov_alexey@mail.ru 11 июн. 2020 г. 20:12:14) 
                # Перекидываем куда-нибудь данные заказа и сохраняем историю 
                # в БД, если нужно, например, отслеживать состояние (готова / едет) и т.д. 
                return
        
        self.next_state()

    def send_message(self, msg):
        """Отправить сообщение."""
        logger.debug(u'msg = %s', msg)
        self._user_interface.send_message(msg)
