# -*- coding: utf-8 -*-
"""Состояния FSM для закача пиццы."""

import enum

import transitions

from chatbot.common import ValidateException, IDialogState, IMsgState

class StateEnum(enum.Enum):
    ERROR = 0
    GREETING = 1
    WAITING_FOR_PIZZA_SIZE = 2
    WAITING_FOR_PAYMENT_METHOD = 3
    WAITING_FOR_CONFIRM = 4
    GRATITUDE = 5
    CANCEL_ORDER = 6
    WAITING_FOR_NEW_ORDER = 7

ANY_MESSAGE = object()


class GreetingState(IMsgState, transitions.State):
    """Состояние приветствия (инициализационное)."""
    state = StateEnum.GREETING
    
    @classmethod
    def build_init_message(cls, pizza_order):
        return u'Здравсвуйте, я бот и я буду принимать ваш заказ.'


class _PizzaOrderState(IDialogState, transitions.State):
    """Родительский класс для диалогов, связанных с заказом пиццы."""
    state = StateEnum.ERROR
    
    _valid_msg = None
    _hint = u'Place a hint here.'

    @classmethod
    def build_init_message(cls, pizza_order):
        return u''

    def validate(self, answer):
        if answer.lower() not in self._valid_msg:
            raise ValidateException(self._hint)


class PizzaSizeState(_PizzaOrderState):
    """Состояние ожидания размера пиццы."""
    state = StateEnum.WAITING_FOR_PIZZA_SIZE
    
    _valid_msg = (u'большую', u'маленькую')
    _hint = (u'Не понимаю ваш ответ. Введите, пожалуйста, "%s" или "%s" '
             u'(без кавычек)') % _valid_msg

    @classmethod
    def build_init_message(cls, pizza_order):
        return (u'Какую вы хотите пиццу? %s или %s?'
                ) % tuple(w.capitalize() for w in cls._valid_msg)


class PaymentMethodState(_PizzaOrderState):
    """Состояние ожидания способа оплаты."""
    state = StateEnum.WAITING_FOR_PAYMENT_METHOD

    _cash_payment = (u'нал', u'наличка', u'налик', u'наличный', u'наличкой', u'кэш')
    _card_payment = (u'картой', u'безнал', u'безналом', u'карта', u'безналичный')
    _valid_msg = set(_cash_payment + _card_payment)
    _hint = (u'Не понимаю ваш ответ. Введите, пожалуйста, "%s" или "%s" '
             u'(без кавычек)') % (u'Картой', u'Наличкой')
    
    @classmethod
    def build_init_message(cls, pizza_order):
        return u'Как вы будете платить?'


class ConfirmState(_PizzaOrderState):
    """Состояние ожидания размера пиццы."""
    state = StateEnum.WAITING_FOR_CONFIRM

    _valid_msg = (u'да', u'нет')
    _hint = (u'Не понимаю ваш ответ. Введите, пожалуйста, "%s" или "%s" '
             u'(без кавычек)') % tuple(w.capitalize() for w in _valid_msg)

    @classmethod
    def build_init_message(self, pizza_order):
        return (u'Вы хотите {size} пиццу, оплата - {payment_method}?'
                ).format(size=pizza_order.size,
                         payment_method=pizza_order.payment_method)


class GratitudeState(IMsgState, transitions.State):
    """Прощальное сообщение."""
    state = StateEnum.GRATITUDE
    
    @classmethod
    def build_init_message(cls, pizza_order):
        return u'Спасибо за заказ.'


class CancelOrderState(IMsgState, transitions.State):
    """Отмена заказа."""
    state = StateEnum.CANCEL_ORDER
    
    @classmethod
    def build_init_message(cls, pizza_order):
        return u'Введите данные заказа ещё раз'


# TODO: (burov_alexey@mail.ru 12 июн. 2020 г. 11:21:30) 
# По быстрому сделал, как диалог, но так что-то просто ждущее любого ввода
class WaitingForNewOrderState(IDialogState, transitions.State):
    """Ожидание нового заказа."""
    state = StateEnum.WAITING_FOR_NEW_ORDER
    
    @classmethod
    def build_init_message(cls, pizza_order):
        return u''

    def validate(self, answer):
        # Любой ввод
        return True


pizza_order_state_clses = {
    GreetingState.state: GreetingState,
    PizzaSizeState.state: PizzaSizeState,
    PaymentMethodState.state: PaymentMethodState,
    ConfirmState.state: ConfirmState,
    GratitudeState.state: GratitudeState,
    CancelOrderState.state: CancelOrderState,
    WaitingForNewOrderState.state: WaitingForNewOrderState
}
