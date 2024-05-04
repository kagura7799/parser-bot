import telebot
import requests
from config import token
class HelloWorldBot:
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.register_handlers()
        self.URL = None

    def register_handlers(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message, "Здравствуйте. Отправьте мне ссылку на целевой сайт.")

        @self.bot.message_handler(func=lambda message: message.text and not message.text.startswith('/'))
        def save_url(message):
            url = message.text

            if self.check_url(url):
                self.URL = url
                self.bot.reply_to(message, "Ваша ссылка принята.")
                print(f"LOG: Сайт {self.URL} существует.")
            else:
                self.bot.reply_to(message, "Ссылка указана некорректно, или не является рабочей.")
    def check_url(self, url) -> bool:
        try:
            response = requests.get(url)
            return response.status_code == 200
        except Exception as e:
            print(f"Ошибка при проверке ссылки: {e}")
            return False
    def start_polling(self):
        print('Bot started')
        self.bot.polling()

if __name__ == "__main__":
    bot = HelloWorldBot(token)
    bot.start_polling()
