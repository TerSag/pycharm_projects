from abc import ABC, abstractmethod


# Створюємо інтерфейс Notifier за допомогою абстрактного класу
class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):
        pass


# Реалізуємо клас для Email
class EmailNotifier(Notifier):
    def send(self, message: str):
        # Власна логіка для імейлу
        print(f"[Email] Відправка листа на пошту: {message}")


# Реалізуємо клас для SMS
class SMSNotifier(Notifier):
    def send(self, message: str):
        # Власна логіка для смс
        print(f"[SMS] Надсилання смс на телефон: {message}")


# Реалізуємо клас для Telegram
class TelegramNotifier(Notifier):
    def send(self, message: str):
        # Власна логіка для телеграму
        print(f"[Telegram] Відправка повідомлення в чат: {message}")


# Створюємо менеджер сповіщень
class NotificationManager:
    def __init__(self, notifier: Notifier):
        # Менеджер приймає об'єкт, що реалізує інтерфейс Notifier
        self.notifier = notifier

    def set_notifier(self, notifier: Notifier):
        # Метод, щоб можна було змінювати спосіб сповіщення на льоту
        self.notifier = notifier

    def notify(self, message: str):
        # Викликаємо метод send(), не прив'язуючись до конкретного класу
        self.notifier.send(message)


# --- Демонстрація роботи (тестування) ---
if __name__ == "__main__":
    # Створюємо об'єкти різних типів сповіщень
    email_client = EmailNotifier()
    sms_client = SMSNotifier()
    telegram_client = TelegramNotifier()

    print("--- Запуск системи сповіщень ---")

    # 1. Передаємо в менеджер EmailNotifier
    manager = NotificationManager(email_client)
    manager.notify("Ваш акаунт у системі каршерінгу успішно активовано.")

    # 2. Змінюємо тип сповіщення на SMS (використовуємо той самий менеджер)
    manager.set_notifier(sms_client)
    manager.notify("Списання коштів за поїздку пройшло успішно.")

    # 3. Змінюємо на Telegram
    manager.set_notifier(telegram_client)
    manager.notify("Користувач Nathan щойно завершив оренду автомобіля.")