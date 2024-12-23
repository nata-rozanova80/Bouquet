# orders/utils.py

from django.conf import settings
from telegram import Bot
import logging

logger = logging.getLogger(__name__)

bot = Bot(token=settings.TELEGRAM_TOKEN)

def send_status_update(user_id, order_id, status):
    message = f'Ваш заказ #{order_id} обновлен. Новый статус: {status}.'
    try:
        bot.send_message(chat_id=user_id, text=message)
        logger.info(f"Sent status update to user {user_id} for order {order_id}")
    except Exception as e:
        logger.error(f'Error sending message to {user_id}: {e}')
