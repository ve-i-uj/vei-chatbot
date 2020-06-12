# -*- coding: utf-8 -*-
"""Юнит тесты для модуля chatbot\pizzaorder\model.py"""

import unittest

from chatbot import common
from chatbot import pizzaorder
from chatbot.pizzaorder import state
from chatbot.pizzaorder import model


class TestUI(object, common.IUserInterface):
    """Интерфейс взаимодействия с пользователем через командную строку."""

    def __init__(self):
        self._model = None
        # смотреть какие сообщения "отправлены" и сколько их
        self.msges = []

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, value):
        self._model = value

    def send_message(self, msg): 
        self.msges.append(msg)


# цель скорее не сам тест, а чтобы ловить в дебагере на брэйкпоинтах
class DialogTestCase(unittest.TestCase):
    """Тест всего диалога."""
    
    def setUp(self):
        unittest.TestCase.setUp(self)
        self._test_ui = TestUI()
        self._model = pizzaorder.PizzaOrderModel(
            uid=1,
            state_clses=pizzaorder.pizza_order_state_clses,
            user_interface=self._test_ui
        )

    # TODO: (burov_alexey@mail.ru 12 июн. 2020 г. 08:48:27) 
    # Нужно разбить на маленькие тесты.
    def test_ok(self):
        """Проверка, когда вводятся только корректные данные."""
        # после инициализации должно быть преветсвенное сообщение и выбор размера пиццы
        self.assertEqual(
            len(self._test_ui.msges), 2,
            u'После инициализации должно быть преветсвенное сообщение и выбор размера пиццы'
        )
        # это сообщения от состояний
        self.assertEqual(self._test_ui.msges[0],
                         state.GreetingState.build_init_message(None))
        self.assertEqual(self._test_ui.msges[1], 
                         state.PizzaSizeState.build_init_message(None))
        # сейчас состояние получения размера
        self.assertEqual(self._model.machine.get_state(self._model.state).state,
                         state.PizzaSizeState.state)

        # чистим сообщения
        self._test_ui.msges[:] = []
        # Ответ пользоватеся
        self._test_ui.model.on_get_message(u'Большую')
        # теперь нужное состояние (оно переключилось)
        self.assertEqual(self._model.machine.get_state(self._model.state).state,
                         state.PaymentMethodState.state)
        # отправлено только одно сообщение ...
        self.assertEqual(len(self._test_ui.msges), 1)
        # ... и это сообщение, которое ожидается
        self.assertEqual(self._test_ui.msges[0],
                         state.PaymentMethodState.build_init_message(None))

        # чистим сообщения
        self._test_ui.msges[:] = []
    
        self._test_ui.model.on_get_message(u'Картой')
        # теперь нужное состояние (оно переключилось)
        self.assertEqual(self._model.machine.get_state(self._model.state).state,
                         state.ConfirmState.state)
        # отправлено только одно сообщение ...
        self.assertEqual(len(self._test_ui.msges), 1)
        # ... и это сообщение, которое ожидается
        po = model.PizzaOrder(1, u'Большую', u'Картой')
        self.assertEqual(self._test_ui.msges[0],
                         state.ConfirmState.build_init_message(po))

        # чистим сообщения
        self._test_ui.msges[:] = []
    
        self._test_ui.model.on_get_message(u'Да')
        # теперь нужное состояние (оно переключилось)
        self.assertEqual(self._model.machine.get_state(self._model.state).state,
                         state.GratitudeState.state)
        # отправлено только одно сообщение ...
        self.assertEqual(len(self._test_ui.msges), 1)
        # ... и это сообщение, которое ожидается
        self.assertEqual(self._test_ui.msges[0],
                         state.GratitudeState.build_init_message(None))


class InvalidInputTestCase(object):
    """Родительский класс для тестов с неправильным вводом данных"""
    
    # нужно задать в наследнике
    _tested_state = None
        
    def setUp(self):
        unittest.TestCase.setUp(self)
        self._test_ui = TestUI()
        self._model = pizzaorder.PizzaOrderModel(
            uid=1,
            state_clses=pizzaorder.pizza_order_state_clses,
            user_interface=self._test_ui
        )
        state_name = self._tested_state.state.name
        should_be_state = self._model.machine.get_state(state_name)
        self._model.machine.set_state(should_be_state)
        # чистим сообщения
        self._test_ui.msges[:] = []

    def test_invalid_input(self):
        """Проверка, когда вводится неправильные данные.
        
        Должна в ответ водиться посказка, а состояние должно оставаться
        прежним.
        """
        # сейчас состояние получения размера
        self.assertEqual(self._model.machine.get_state(self._model.state).state,
                         self._tested_state.state)

        self._test_ui.model.on_get_message(u'--- Неизвестный ввод ---')
        # остались в том же состоянии
        self.assertEqual(self._model.machine.get_state(self._model.state).state,
                         self._tested_state.state)
        # отправлено только одно сообщение ...
        self.assertEqual(len(self._test_ui.msges), 1)
        # ... и это сообщение, которое ожидается (подсказка)
        self.assertEqual(self._test_ui.msges[0],
                         self._tested_state._hint)


class InvalidPizzaSizeTestCase(InvalidInputTestCase, unittest.TestCase):
    """Тест когда не правильно указан размер пиццы."""

    _tested_state = state.PizzaSizeState
        
        
class InvalidPaymentMethodTestCase(InvalidInputTestCase, unittest.TestCase):
    """Тест когда не правильно указан способ оплаты."""

    _tested_state = state.PaymentMethodState
        
        
class InvalidConfirmTestCase(InvalidInputTestCase, unittest.TestCase):
    """Тест когда не правильно задано подтверждение."""

    _tested_state = state.ConfirmState
        
        

if __name__ == '__main__':
    unittest.main()
