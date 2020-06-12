# -*- coding: utf-8 -*-
"""Пользовательский интерфейс через телеграм."""

from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

from chatbot import common

TOKEN = '1211214680:AAHGNFx7RvU-uS5AYFc8cLLG-TUUoVNnLUQ'


class TelegramUI(common.IUserInterface):
    """Интерфейс взаимодействия с пользователем через командную строку."""

    def __init__(self, model_cls):
        self._model_cls = model_cls

        self._updater = Updater(token=TOKEN, use_context=True)
        self._dispatcher = self._updater.dispatcher

        start_handler = CommandHandler('start', self._start)
        self._dispatcher.add_handler(start_handler)

        echo_handler = MessageHandler(Filters.text & (~Filters.command), self._msg_handler)
        self._dispatcher.add_handler(echo_handler)

        self._users = {}
        # TODO: (burov_alexey@mail.ru 12 июн. 2020 г. 13:03:15)
        # Нужно думать, как пробрасывать этот context и что это в обще такое.
        # Пока так.
        self._contexts = {}

    def run(self):
        """Запускает loop чтения / записи из командной строки."""

        self._updater.start_polling()

    def send_message(self, uid, msg):
        context = self._contexts[uid]
        context.bot.send_message(chat_id=uid, text=msg)

    def _start(self, update, context):
        chat_id = update.effective_chat.id
        model = self._model_cls(chat_id, model_cls=self)
        self._users[chat_id] = model
        self._contexts[chat_id] = context
        # Приветствие и т.п.
        model.init()

    def _msg_handler(self, update, context):
        chat_id = update.effective_chat.id
        self._contexts[chat_id] = context

        model = self._users[chat_id]
        # TODO: (burov_alexey@mail.ru 12 июн. 2020 г. 13:08:20)
        # А оно в чём тут приходит? В юникоде?
        model.on_get_message(update.message.text)
