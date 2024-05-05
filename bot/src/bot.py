import telebot
import requests
from telebot import types
from config import token


class Bot:
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
                self.choice_data(message)

                print(f"LOG: Сайт {self.URL} существует.")
            else:
                self.bot.reply_to(message, "Ссылка указана некорректно, или не является рабочей. \nПримечание: ссылка должна начинаться с https://")

    def check_url(self, url: str) -> bool:
        try:
            response = requests.get(url)
            return response.status_code == 200
        except Exception as e:
            print(f"Ошибка при проверке ссылки: {e}")
            return False

    def choice_data(self, message):
        markup = types.ReplyKeyboardMarkup(row_width=2)
        btn1 = types.KeyboardButton('Заголовки')
        btn2 = types.KeyboardButton('Ссылки')
        btn3 = types.KeyboardButton('Фото и видео')
        btn4 = types.KeyboardButton('Информацию о продуктах и ценах')
        btn5 = types.KeyboardButton('Социальные медиа данные, такие как количество лайков, комментариев, подписчиков')

        markup.add(btn1, btn2, btn3, btn4, btn5)
        self.bot.send_message(message.chat.id, "Что парсим?", reply_markup=markup)

    def start_polling(self):
        print('Bot started')
        self.bot.polling()

if __name__ == "__main__":
    bot = Bot(token)
    bot.start_polling()
