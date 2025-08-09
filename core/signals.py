import threading
from asyncio import run
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings
from .models import Order, Review
from .mistral import is_bad_review
from .telegram_bot import send_telegram_message

TELEGRAM_BOT_API_KEY = settings.TELEGRAM_BOT_API_KEY
TELEGRAM_USER_ID = settings.TELEGRAM_USER_ID


# ======== Общая функция отправки в Telegram =========
def send_telegram_async(message: str):
    """Отправка в Telegram в отдельном потоке, чтобы не блокировать сайт."""
    def _send():
        try:
            run(send_telegram_message(
                TELEGRAM_BOT_API_KEY,
                TELEGRAM_USER_ID,
                message
            ))
        except Exception as e:
            print(f"[Telegram ERROR] {e}")

    threading.Thread(target=_send).start()


# ======== Отзывы =========
@receiver(post_save, sender=Review)
def check_review_text(sender, instance, created, **kwargs):
    """
    При создании отзыва проверяем текст.
    Если нет негативных слов — публикуем и отправляем в Telegram.
    """
    if not created:
        return

    if not is_bad_review(instance.text):
        instance.is_published = True
        instance.save(update_fields=["is_published"])

        message = f"""
🎉*Новый отзыв от клиента!*🎉

👤*Имя:* {instance.client_name}
💬*Текст:* {instance.text}
⭐*Оценка:* {instance.rating}

🔗*Ссылка на отзыв:* http://127.0.0.1:8000/admin/core/review/{instance.id}/change/

#отзыв
=================
"""
        send_telegram_async(message)

    else:
        instance.is_published = False
        instance.save(update_fields=["is_published"])
        print(f"Отзыв {instance.client_name} не опубликован из-за негативных слов.")


# ======== Заказы =========
@receiver(m2m_changed, sender=Order.products.through)
def send_telegram_notification(sender, instance, action, **kwargs):
    """
    При добавлении товаров в заказ — отправляем уведомление в Telegram.
    """
    if action == 'post_add' and kwargs.get('pk_set'):
        products = [product.name for product in instance.products.all()]

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
        send_telegram_async(message)
