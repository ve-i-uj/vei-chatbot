# -*- coding: utf-8 -*-
"""Модель FSM для работы с заказом пиццы."""

import logging

import attr
import transitions

from chatbot import common
from chatbot.pizzaorder import state
from chatbot.pizzaorder.state import StateEnum

logger = logging.getLogger(__name__)


pizza_order_transitions = [
    # у этих состояний переход линейный, поэтому триггер одни и тот же
    ['proceed', StateEnum.GREETING, StateEnum.WAITING_FOR_PIZZA_SIZE],
    ['proceed', StateEnum.WAITING_FOR_PIZZA_SIZE, StateEnum.WAITING_FOR_PAYMENT_METHOD],
    ['proceed', StateEnum.WAITING_FOR_PAYMENT_METHOD, StateEnum.WAITING_FOR_CONFIRM],
    # а здесь начинает ветвиться
    #     подтвердил заказ
    ['confirm', StateEnum.WAITING_FOR_CONFIRM, StateEnum.GRATITUDE],
    ['wait_new_order', StateEnum.GRATITUDE, StateEnum.WAITING_FOR_NEW_ORDER],
    ['new_order', StateEnum.WAITING_FOR_NEW_ORDER, StateEnum.GREETING],
    #     отменил заказ
    ['cancel', StateEnum.WAITING_FOR_CONFIRM, StateEnum.CANCEL_ORDER],
    ['update', StateEnum.CANCEL_ORDER, StateEnum.WAITING_FOR_PIZZA_SIZE],
]


@attr.s
class PizzaOrder(object):
    """Данные заказа."""
    uid = attr.ib(type=int, default=None)
    size = attr.ib(type=unicode, default=None)
    payment_method = attr.ib(type=unicode, default=None)
    confirmed = attr.ib(type=bool, default=False)


class PizzaOrderModel(common.IMessageHandler):
    """Модель FSM для работы с заказом пиццы."""

    def __init__(self, uid, user_interface):
        self._pizza_order = PizzaOrder(uid=uid)
        # экземпляр IUserInterface
        self._user_interface = user_interface
        self._user_interface.model = self

        # нужно добавить колбэк состоянию при инициализации,
        # поэтому заменяется имя состояния на экземпляр

        def on_enter_cb():
            """Отправка сообщения при входе в состояние"""
            state_inst = self.machine.get_state(self.state)
            msg = state_inst.build_init_message(self._pizza_order)
            self.send_message(msg)

        # сперва находим все имена состояний, которые используются с триггерами
        state_names = set()
        for _, src_state, dst_state in pizza_order_transitions:
            state_names.add(src_state)
            state_names.add(dst_state)
        # теперь под каждое имя создаём экземпляр состояния
        state_inst_by_name = {}
        for state_name in state_names:
            state_cls = state.pizza_order_state_clses[state_name]
            state_inst_by_name[state_name] = state_cls(name=state_name,
                                                       on_enter=on_enter_cb)

        new_transitions = []
        for trigger_name, src_state, dst_state in pizza_order_transitions:
            src_state_inst = state_inst_by_name[src_state]
            dst_state_inst = state_inst_by_name[dst_state]
            new_transitions.append([trigger_name, src_state_inst, dst_state_inst])

        self.machine = transitions.Machine(
            model=self,
            states=list(state_inst_by_name.values()),
            initial=state.StateEnum.GREETING,
            transitions=new_transitions,
            ignore_invalid_triggers=True
        )
        
        self.init()

    def init(self):
        # дернем руками приветсвенное сообщение начального состояния
        state_inst = self.machine.get_state(self.state)
        msg = state_inst.build_init_message(self._pizza_order)
        self.send_message(msg)
        # И переходим в следующее состояние
        self.proceed()

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
            self.proceed()
        elif state_inst.state == state.StateEnum.WAITING_FOR_PAYMENT_METHOD:
            self._pizza_order.payment_method = msg
            self.proceed()
        elif state_inst.state == state.StateEnum.WAITING_FOR_CONFIRM:
            # на то, что это да / нет уже была проверка в validate
            if msg.strip().lower() == u'да':
                self._pizza_order.confirmed = True
                self.confirm()
                self.wait_new_order()
            elif msg.strip().lower() == u'нет':
                self.cancel()
                self.update()
        elif state_inst.state == state.StateEnum.GRATITUDE:
            self.wait_new_order()
        elif state_inst.state == state.StateEnum.WAITING_FOR_NEW_ORDER:
            self.new_order()
            self.proceed()
            

        # (burov_alexey@mail.ru 11 июн. 2020 г. 20:12:14) 
        # Перекидываем куда-нибудь данные заказа и сохраняем историю 
        # в БД, если нужно, например, отслеживать состояние (готова / едет) и т.д. 
        

    def send_message(self, msg):
        """Отправить сообщение."""
        logger.debug(u'msg = %s', msg)
        if not msg.strip():
            # TODO: (burov_alexey@mail.ru 12 июн. 2020 г. 11:18:30) 
            # Когда диалог, но ничего не отправляет. Нужен отдельный интерфейс,
            # и специальная логика. Пока так.
            return
        self._user_interface.send_message(msg)
