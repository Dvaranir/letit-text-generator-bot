import os
import telebot

from dotenv import load_dotenv
from .TextGeneratorController import TextGeneratorController


class Controller:

    def __init__(self):
        load_dotenv()
        token = os.getenv("BOT_TOKEN")

        self.bot = telebot.TeleBot(token)
        self.types = telebot.types
        self.text_generator_controller = TextGeneratorController(self)

        self.callbacks_handler()

        self.start_bot()

    def start_bot(self):
        self.start()
        self.bot.infinity_polling()
        # while True:
        #     try:
        #         self.bot.polling(none_stop=True)
        #
        #     except Exception as e:
        #         logger.error(e)  # или просто print(e) если у вас логгера нет,
        #         # или import traceback; traceback.print_exc() для печати полной инфы
        #         time.sleep(15)

    def start(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            self.show_buttons(message.chat.id)

    def show_buttons(self, chat_id):
        button_generate_text = self.types.InlineKeyboardButton('Generate Text', callback_data='generate_text')

        keyboard = self.types.InlineKeyboardMarkup()

        keyboard.add(button_generate_text)

        controls_message = "Functions:"

        self.bot.send_message(chat_id, text=controls_message, reply_markup=keyboard)

    def callbacks_handler(self):
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            if call.data == "generate_text":
                self.text_generator_controller.get_text_input(call)
