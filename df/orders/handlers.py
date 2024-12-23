# orders/handlers.py

import logging
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, Filters
from .models import Order
from .utils import send_status_update

logger = logging.getLogger(__name__)

def start(update: Update, context):
    logger.info(f"Received /start from {update.message.from_user.id}")
    update.message.reply_text('Привет! Я бот для доставки цветов. Как я могу помочь?')

def help_command(update: Update, context):
    logger.info(f"Received /help from {update.message.from_user.id}")
    update.message.reply_text('Доступные команды:\n/start\n/help\n/order\n/analytics')

def order_command(update: Update, context):
    logger.info(f"Received /order from {update.message.from_user.id}")
    update.message.reply_text('Пожалуйста, отправьте информацию о вашем заказе в формате: название букета, адрес доставки.')

def handle_message(update: Update, context):
    text = update.message.text
    logger.info(f"Received message from {update.message.from_user.id}: {text}")
    try:
        bouquet, address = text.split(',', 1)
        order = Order.objects.create(
            user=update.message.from_user.id,
            bouquet=bouquet.strip(),
            address=address.strip(),
            status='pending'
        )
        logger.info(f"Created Order #{order.id} for user {update.message.from_user.id}")
        update.message.reply_text(f'Ваш заказ #{order.id} принят! Мы уведомим вас о статусе.')
    except ValueError:
        logger.warning(f"Invalid order format from {update.message.from_user.id}: {text}")
        update.message.reply_text('Пожалуйста, отправьте информацию в формате: название букета, адрес доставки.')

def analytics_command(update: Update, context):
    logger.info(f"Received /analytics from {update.message.from_user.id}")
    from django.db.models import Count

    total_orders = Order.objects.count()
    pending = Order.objects.filter(status='pending').count()
    confirmed = Order.objects.filter(status='confirmed').count()
    shipped = Order.objects.filter(status='shipped').count()
    delivered = Order.objects.filter(status='delivered').count()
    cancelled = Order.objects.filter(status='cancelled').count()

    message = (
        f"📊 **Статистика заказов**\n\n"
        f"Всего заказов: {total_orders}\n"
        f"В ожидании: {pending}\n"
        f"Подтверждено: {confirmed}\n"
        f"Отправлено: {shipped}\n"
        f"Доставлено: {delivered}\n"
        f"Отменено: {cancelled}"
    )

    update.message.reply_text(message, parse_mode='Markdown')

def setup_dispatcher(dispatcher):
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("order", order_command))
    dispatcher.add_handler(CommandHandler("analytics", analytics_command))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
