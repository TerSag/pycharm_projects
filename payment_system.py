from abc import ABC, abstractmethod


# 1. Абстрактний базовий клас
class PaymentMethod(ABC):

    @abstractmethod
    def pay(self, amount):
        pass

    @abstractmethod
    def refund(self, amount):
        pass

    def log_transaction (self, amount):
        print(f"[LOG]: Транзакція на суму {amount} грн успішно оброблена.")


# 2. Реалізація CreditCardPayment
class CreditCardPayment(PaymentMethod):
    def __init__(self, card_number):
        self.card_number = card_number

    def pay(self, amount):
        # Замаскував номер картки для безпеки
        masked_card = f"****{self.card_number[-4:]}"
        print(f"Оплата {amount} грн з кредитної картки {masked_card}")
        self.log_transaction(amount)

    def refund(self, amount):
        print(f"Повернення {amount} грн на картку {self.card_number}")


# 3. Реалізація PayPalPayment
class PayPalPayment(PaymentMethod):
    def __init__(self, email):
        self.email = email

    def pay(self, amount):
        print(f"Оплата {amount} грн через PayPal (аккаунт: {self.email})")
        self.log_transaction(amount)

    def refund(self, amount):
        print(f"Повернення {amount} грн на PayPal ({self.email})")


# 4. Реалізація CryptoPayment
class CryptoPayment(PaymentMethod):
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address

    def pay(self, amount):
        print(f"Оплата {amount} грн у криптовалюті з гаманця {self.wallet_address}")
        self.log_transaction(amount)

    def refund(self, amount):
        print("Помилка: Повернення коштів у криптовалюті неможливе (Blockchain restriction).")


# 5. Демонстрація роботи
if __name__ == "__main__":
    payments = [
        CreditCardPayment("4441111122221234"),
        PayPalPayment("user@example.com"),
        CryptoPayment("0x71C7656EC7ab88b098defB751B7401B5f6d8976F")
    ]

    print("--- Процес оплати ---")
    for method in payments:
        method.pay(100)
        print("-" * 20)

    print("\n--- Процес повернення ---")
    for method in payments:
        method.refund(50)