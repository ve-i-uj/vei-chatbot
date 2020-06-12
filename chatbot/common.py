# -*- coding: utf-8 -*-
"""Общие классы."""


class IMsgState:
    """Интерфейс состояния, которое начинается с сообщения."""
    
    @classmethod
    def build_init_message(cls, *args, **kws):
        """Начальное сообщение."""
        pass


class ValidateException(Exception):
    """Ошибка валидации."""


class IDialogState(IMsgState):
    """Интерфейс единицы диалога (вопрос / ответ / подсказка)."""
    
    @classmethod
    def validate(cls, answer):
        """Проверить, что сообщение будет понято.
        
        Если проверка не пройдена, возбуждает исключение ValidateException,
        если пройдена, то возвращает None (ничего не делает).
        """
        pass
    
    @classmethod
    def build_init_message(cls, *args, **kws):
        """Начальное сообщение."""
        pass


class IUserInterface:
    """Интерфейс взаимодействия с пользователем (ввод / вывод данных).
    
    Класс принимает собщение и вызывает колбэк модели.
    """
    
    @property
    def model(self):
        """Получить модель (наследник IMessageHandler)"""
        pass

    @model.setter
    def model(self, value):
        """Сеттер"""
        pass

    def send_message(self, msg):
        """Отправить сообщение в UI."""
        pass


class IMessageHandler:
    """Интерфейс для класса работающего с сообщениями (получить, отправить)."""

    def on_get_message(self, msg):
        """Метод срабатывает, когда получено сообщение."""
        pass
    
    def send_message(self, msg):
        """Отправить сообщение."""
        pass
