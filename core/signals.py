# Опишем сигнал, который будет слушать создание записи в модель Review 
# и проверять есть ли в поле text слова "плохо" или "ужасно" - если нет, то меняем is_published на True
from .models import Order, Review
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from .mistral import is_bad_review
from .telegram_bot import send_telegram_message
from asyncio import run
from telegram.error import BadRequest
from asgiref.sync import async_to_sync
# Из настроек импортирум токен и id чата 
from django.conf import settings

TELEGRAM_BOT_API_KEY = settings.TELEGRAM_BOT_API_KEY
TELEGRAM_USER_ID = settings.TELEGRAM_USER_ID


@receiver(post_save, sender=Review)
def check_review_text(sender, instance, created, **kwargs):
    """ 
    Проверяет текст отзыва на наличие слов 'плохо' или 'ужасно'. 
    Если таких слов нет, то устанавливаем is_published = True
    """
    if created:
        if not is_bad_review(instance.text):
            instance.is_published = True
            instance.save()
            # Отправка в телеграм
            message = f"""
🎉*Новый отзыв от клиента!*🎉

👤*Имя:* {instance.client_name}
💬*Текст:* {instance.text}
⭐*Оценка:* {instance.rating}

🔗*Ссылка на отзыв:* http://127.0.0.1:8000/admin/core/review/{instance.id}/change/

#отзыв
=================
"""
            run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))

        else:
            instance.is_published = False
            instance.save()
            # Вывод  в терминал
            print(f"Отзыв {instance.client_name} не опубликован из-за негативных слов.")


@receiver(m2m_changed, sender=Order.products.through)
def send_telegram_notification(sender, instance, action, **kwargs):
    """
    Обработка сигнала m2m_changed для модели Order.
    Он обрабатывает добавление каждой услуги в запись на консультацию.
    """
    if action == 'post_add' and kwargs.get('pk_set'):
        # Получаем список услуг
        products = [product.name for product in instance.products.all()]

        # Формируем сообщение

        message = f"""🥛 *НОВАЯ ЗАПИСЬ НА УСЛУГУ!* 🥛

👤*Имя:* {instance.client_name}
📞*Телефон:* `{instance.phone or 'Не указан'}`
💬*Комментарий:* _{instance.comment or 'Не указан'}_
📦*Продукты:* {', '.join(products) or 'Не указаны'}
🗓️ *Дата создания:* {instance.date_created.strftime('%d.%m.%Y %H:%M') if instance.date_created else 'Не указана'}
📅*Желаемый день:* {instance.delivery_day or 'Не указан'}

🔗*Ссылка на запись:* http://127.0.0.1:8000/admin/core/order/{instance.id}/change/
        
#новыйзаказ
====================
""" 
        run(send_telegram_message(TELEGRAM_BOT_API_KEY, TELEGRAM_USER_ID, message))