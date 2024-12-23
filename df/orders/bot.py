# orders/bot.py

import logging
from telegram import Bot
from telegram.ext import Dispatcher
from django.conf import settings
from .handlers import setup_dispatcher

# Настройка логирования
logger = logging.getLogger(__name__)

# Инициализация бота
bot = Bot(token=settings.TELEGRAM_TOKEN)

# Инициализация диспетчера
dispatcher = Dispatcher(bot, None, workers=0)

# Настройка обработчиков
setup_dispatcher(dispatcher)
