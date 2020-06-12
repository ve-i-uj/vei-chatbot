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


# # цель скорее не сам тест, а чтобы ловить в дебагере на брэйкпоинтах
class DialogTestCase(unittest.TestCase):
    """Тест всего диалога."""
     
    def setUp(self):
        unittest.TestCase.setUp(self)
        self._test_ui = TestUI()
        self._model = pizzaorder.PizzaOrderModel(
            uid=1,
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
                         state.StateEnum.WAITING_FOR_NEW_ORDER)
        # отправлено только одно сообщение ...
        self.assertEqual(len(self._test_ui.msges), 1)
        # ... и это сообщение, которое ожидается
        self.assertEqual(self._test_ui.msges[0],
                         state.GratitudeState.build_init_message(None))


class MsgStateTestCase:
    """Родительский класс для выставления конкретного состояния."""
    
    # нужно задать в наследнике
    # Состояние, с которого перейдём на тестируемое, чтобы была начальное собщение
    _init_state = None
 
    def setUp(self):
        self._test_ui = TestUI()
        self._model = pizzaorder.PizzaOrderModel(
            uid=1,
            user_interface=self._test_ui
        )
        state_name = self._init_state.state.name
        should_be_previous_state = self._model.machine.get_state(state_name)
        self._model.machine.set_state(should_be_previous_state)
        # чистим сообщения
        self._test_ui.msges[:] = []


class DialogStateTestCase(MsgStateTestCase):
    """Родительский класс для диалогов тестов конкретного состояния."""
#     """Родительский класс для диалогов тестов с неправильным вводом данных"""
     
    # нужно задать в наследнике
    _init_state = None

    def setUp(self):
        MsgStateTestCase.setUp(self)
 
    def test_invalid_input(self):
        """Проверка, когда вводится неправильные данные.
         
        Должна в ответ водиться посказка, а состояние должно оставаться
        прежним.
        """
        # сейчас состояние получения размера
        self.assertEqual(self._model.machine.get_state(self._model.state).state,
                         self._init_state.state)
 
        self._test_ui.model.on_get_message(u'--- Неизвестный ввод ---')
        # остались в том же состоянии
        self.assertEqual(self._model.machine.get_state(self._model.state).state,
                         self._init_state.state)
        # отправлено только одно сообщение ...
        self.assertEqual(len(self._test_ui.msges), 1)
        # ... и это сообщение, которое ожидается (подсказка)
        self.assertEqual(self._test_ui.msges[0],
                         self._init_state._hint)

  
class InvalidPizzaSizeTestCase(DialogStateTestCase, unittest.TestCase):
    """Тест когда не правильно указан размер пиццы."""
 
    _init_state = state.PizzaSizeState

    def setUp(self):
        unittest.TestCase.setUp(self)
        DialogStateTestCase.setUp(self)

         
class InvalidPaymentMethodTestCase(DialogStateTestCase, unittest.TestCase):
    """Тест когда не правильно указан способ оплаты."""
 
    _init_state = state.PaymentMethodState
         
    def setUp(self):
        unittest.TestCase.setUp(self)
        DialogStateTestCase.setUp(self)


class InvalidConfirmTestCase(DialogStateTestCase, unittest.TestCase):
    """Тест когда не правильно задано подтверждение."""
 
    _init_state = state.ConfirmState

    def setUp(self):
        unittest.TestCase.setUp(self)
        DialogStateTestCase.setUp(self)
 

class CancelStateTestCase(MsgStateTestCase, unittest.TestCase):
    """Тест отмены."""
    _init_state = state.ConfirmState

    def setUp(self):
        unittest.TestCase.setUp(self)
        MsgStateTestCase.setUp(self)

    def test_next_state_no(self):
        """Нужно проверить, что после отмены перешли на заполнение по новой."""
        # Переходим в нужно состояние, отправив "нет"
        self._test_ui.model.on_get_message(u'Нет')
        # И после перехода мы на WAITING_FOR_PIZZA_SIZE
        self.assertEqual(self._model.machine.get_state(self._model.state).state,
                         state.StateEnum.WAITING_FOR_PIZZA_SIZE)

    def test_next_state_yes(self):
        """Нужно проверить, что после отмены перешли на заполнение по новой."""
        # Переходим в нужно состояние, отправив "да"
        self._test_ui.model.on_get_message(u'Да')
        # И после перехода мы на благодарим за заказ и ждём любого вводе, чтобы
        # сделать новый заказ, т.е. на GREETING
        
        # отправлено только одно сообщение ...
        self.assertEqual(len(self._test_ui.msges), 1)
        # ... и это сообщение, которое ожидается (подсказка)
        self.assertEqual(self._test_ui.msges[0],
                         state.GratitudeState.build_init_message(None))    

        self._test_ui.model.on_get_message(u'Что угодно')

        self.assertEqual(self._model.machine.get_state(self._model.state).state,
                         state.StateEnum.GREETING)

        
if __name__ == '__main__':
    unittest.main()
