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

    def get_stroke_btn_text(self, chat_id):
        try:
            if self.text_generator_controller.stroke_active[chat_id]:
                return "Disable stroke"
            else:
                return "Enable stroke"
        except Exception as exception:
            self.text_generator_controller.toggle_stroke(chat_id)
            print(f"show_buttons\n{exception}")
            return "Enable stroke"

    def show_buttons(self, chat_id):
        button_generate_text = self.types.InlineKeyboardButton('Generate Text x1', callback_data='generate_text')
        button_generate_text_5 = self.types.InlineKeyboardButton('Generate Text x5', callback_data='generate_text_5')
        button_generate_text_10 = self.types.InlineKeyboardButton('Generate Text x10', callback_data='generate_text_10')

        stroke_button_text = self.get_stroke_btn_text(chat_id)
        button_toggle_stroke = self.types.InlineKeyboardButton(stroke_button_text, callback_data='toggle_stroke')

        keyboard = self.types.InlineKeyboardMarkup()

        keyboard.add(button_generate_text)
        keyboard.add(button_generate_text_5)
        keyboard.add(button_generate_text_10)
        keyboard.add(button_toggle_stroke)

        controls_message = "Functions:"

        self.bot.send_message(chat_id, text=controls_message, reply_markup=keyboard)

    def callbacks_handler(self):
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_query(call):
            if call.data == "generate_text":
                self.text_generator_controller.get_text_input(call)
            elif call.data == "generate_text_5":
                self.text_generator_controller.get_text_input(call, send_times=5)
            elif call.data == "generate_text_10":
                self.text_generator_controller.get_text_input(call, send_times=10)
            elif call.data == "toggle_stroke":
                chat_id = call.message.chat.id
                self.text_generator_controller.toggle_stroke(chat_id)
                self.show_buttons(chat_id)
