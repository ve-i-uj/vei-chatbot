# -*- coding: utf-8 -*-
"""Интерфес взаимодействия с ботом через командную строку.

Для отладочных действий.
"""

import logging
import queue
import sys
import threading

from chatbot import common

logger = logging.getLogger(__name__)

TIMEOUT = 0.5


class TimeoutExpired(Exception):
    """Ожидание по таймауту истекло."""


class _ReadingInputThread(threading.Thread):
    """Класс читающий ввод данных с CL."""
     
    def __init__(self, queue):
        super(_ReadingInputThread, self).__init__()
        self._queue = queue
        self.stop = False
 
    def run(self):        
        while True:
            # нужно периодическое прерывание ожидания ввода иначе
            # тред будет не остановить
            try:
                msg = raw_input()
            except EOFError:
                # Эта ошибка возникает при остановке главного треда
                return
            msg = unicode(msg, sys.stdout.encoding)
            self._queue.put_nowait(msg)


class CLI(object, common.IUserInterface):
    """Интерфейс взаимодействия с пользователем через командную строку."""

    def __init__(self, model_cls):
        object.__init__(self)
        self._model_cls = model_cls
        self._model = model_cls(0, self)
        self._input_msg_queue = queue.Queue()
        self._reading_thread = _ReadingInputThread(self._input_msg_queue)

    def run(self):
        """Запускает loop чтения / записи из командной строки."""
        assert self._model is not None, u'A FSM model should be set at first'
        # начальное сообщение модели
        self._model.init()

        self._reading_thread.start()
        
        while True:
            try:
                msg = self._input_msg_queue.get()
                self._model.on_get_message(msg)
            except StopIteration:
                # останавливаем тред чтения
                self._reading_thread.stop = True
                self.send_message(0, u'Пока :-)')
            except Exception as err:
                logger.error(err)

    def send_message(self, uid, msg):
        sys.stdout.write(msg)
        sys.stdout.write('\n')
        sys.stdout.flush()
