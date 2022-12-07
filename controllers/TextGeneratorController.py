import os
import imgkit
import random
import zipfile

from uuid import uuid4


class TextGeneratorController:

    def __init__(self, controller):
        self.controller = controller
        self.bot = controller.bot

        self.stroke_active = {}

        self.english_alphabet = "abcdefghijklmnopqrstuvwxyz"
        self.russian_alphabet = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        self.numbers = "1234567890 "
        self.symbols = "\"',{}[]?!"
        self.symbol_letters = {
            "a": [["4", " "], ["@", " "], ["/-\\", " "], ["/\\", " "]],
            "b": [["8", " "], ["/3", " "]],
            "c": [["¢", " "], ["©", " "], ["(", " "]],
            "d": [["[)", " "], ["|}", " "], ["|)", " "]],
            "e": [["€", " "], ["3", "flip-horizontal"]],
            "f": [["₤", " "]],
            "g": [["6", " "], ["9", " "]],
            "h": [["|-|", " "], ["/-/", " "], ["#", " "], ["|~|", " "], ["]-[", " "], [")-(", " "]],
            "i": [["1", " "], ["!", " "]],
            "j": [[",_|", " "], ["]", " "]],
            "k": [["|{ ", " "], ["[{", " "], ["|<", " "]],
            "l": [["1", " "], ["|_", " "], ["7", "flip-full"]],
            "m": [["|\\/|", " "], ["/\\/\\", " "], ["/V\\", " "]],
            "n": [["|\\|", " "], ["/\\/", " "], ["И", " "]],
            "o": [["0", " "], ["[]", " "], ["()", " "], ["Ø", " "]],
            "p": [["|*", " "]],
            "q": [["(,)", " "]],
            "r": [["®", " "], ["Я", " "]],
            "s": [["$", " "], ["5", " "], ["2", " "]],
            "t": [["7", " "], ["₸", " "]],
            # "u": "",
            "v": [["\\/", " "]],
            "w": [["Ш", " "], ["\\/\\/", " "], ["vv", " "]],
            "x": [["}{", " "], ["×", " "]],
            "y": [["¥", " "]],
            "z": [["2", " "]],
            "а": [["@", " "], ["4", " "], ["/-\\", " "]],
            "б": [["6", " "]],
            "в": [["8", " "]],
            "г": [["r", " "]],
            "д": [["|)", " "]],
            "е": [["€", " "], ["3", "flip-horizontal"]],
            # "ё": "",
            "ж": [["}|{", " "], ["]|[", " "]],
            "з": [["3", " "]],
            "и": [["|/|", " "], ["|Л", " "]],
            # "й": "",
            "к": [["|{ ", " "], ["]", " "], ["|<", " "]],
            "л": [["/\\", " "], ["j|", " "]],
            "м": [["|\\/|", " "], ["/\\/\\", " "], ["/V\\", " "]],
            "н": [["|-|", " "], ["/-/", " "], ["#", " "], ["|~|", " "], ["]-[", " "], [")-(", " "]],
            "о": [["0", " "], ["[]", " "], ["()", " "], ["Ø", " "]],
            "п": [["||", " "]],
            "р": [["₽", " "]],
            "с": [["¢", " "], ["©", " "], ["(", " "]],
            "т": [["7", " "], ["₸", " "]],
            "у": [["¥", " "], ["'/", " "]],
            "ф": [["0|0", " "], ["qp", " "]],
            "х": [["}{", " "], ["×", " "]],
            "ц": [["I_I, ", " "]],
            "ч": [["4", " "], ["'-|", " "]],
            "ш": [["LLI", " "]],
            "щ": [["LLL", " "]],
            "ъ": [["'b", " "]],
            "ы": [["bI", " "]],
            "ь": [["b", " "]],
            "э": [["'€", " "]],
            "ю": [["|-o", " "]],
            "я": [["9I", " "], ["'R", " "]],
            "1": [["!", " "], ["I", " "], ["‘I", " "], ["|", " "]],
            "2": [["z", " "]],
            # "3": "",
            # "4": "",
            "5": [["S", " "]],
            # "6": "",
            "7": [["Z", " "]],
            "8": [["B", " "]],
            # "9": "",
            "0": [["0", " "], ["[]", " "], ["()", " "], ["Ø", " "]],
        }

        self.allowed_symbols = f'{self.english_alphabet}\n{self.russian_alphabet}\n{self.numbers}\n{self.symbols}'

    @staticmethod
    def load_templates():
        html_template = {}
        with open("./views/head.html", 'r') as head:
            html_template['head'] = head.read()

        with open("./views/element.html", 'r') as element:
            html_template['element'] = element.read()

        with open("./views/footer.html", 'r') as footer:
            html_template['footer'] = footer.read()

        return html_template

    def get_text_input(self, call, send_times=1):
        message = call.message
        bot_reply = 'Type some words:\n'
        next_message = self.bot.send_message(message.chat.id, bot_reply)
        self.bot.register_next_step_handler(next_message, self.handle_text_input, bot_reply, send_times)

    def handle_text_input(self, message, bot_reply, send_times=1):
        users_input = message.text.lower()
        self.group_log_message(message)

        for letter in users_input:
            if letter not in self.allowed_symbols:

                bot_reply = f'Symbol {letter} is not allowed.\n\n' \
                            f'You can only use:\n' \
                            f'{self.allowed_symbols}\n\n' \
                            f'{bot_reply}'

                next_message = self.bot.send_message(message.chat.id, bot_reply)
                self.bot.register_next_step_handler(next_message, self.handle_text_input, bot_reply, send_times)

                return

        while True:
            if send_times <= 0:
                break
            self.send_image(message, users_input)
            send_times -= 1

        self.controller.show_buttons(message.chat.id)

    @staticmethod
    def choose_class(number):
        if number == 0:
            return "first"
        elif number == 1:
            return "second"
        elif number == 2:
            return "third"
        else:
            return "forth"

    @staticmethod
    def choose_font_style(number):
        if number == 0:
            return " "
        elif number == 1:
            return "bold"
        else:
            return "italic"

    def generate_classes(self, have_symbol):
        classes = {}

        if have_symbol:
            random_font = random.randint(0, 2)
        else:
            random_font = random.randint(0, 1)

        if random_font == 0:
            random_font_style = random.randint(0, 1)
        else:
            random_font_style = random.randint(0, 2)

        random_color = random.randint(0, 3)

        classes['font'] = self.choose_class(random_font) + "-font"
        classes['color'] = self.choose_class(random_color) + "-color"
        classes['font-style'] = self.choose_font_style(random_font_style)

        return classes

    def fill_template(self, classes, letter, template, chat_id):
        filled_template = template
        all_classes = ""
        if classes['font'] == 'third-font':
            symbol = self.symbol_letters[letter]

            if type(symbol) is list:
                random_symbol = symbol[random.randint(0, len(symbol) - 1)]
                random_symbol_class = random_symbol[1]
                all_classes += f"{random_symbol_class} "
                symbol = random_symbol[0]

            replacing_symbol = symbol.upper()
            classes = self.generate_classes(have_symbol=False)
        else:
            replacing_symbol = letter

        filled_template = filled_template.replace("!!LETTER!!", replacing_symbol.upper())
        stroke = ""
        try:
            if self.stroke_active[chat_id]:
                stroke = "stroke"
        except Exception as exception:
            print(f"fill_template\n{Exception}")



        all_classes += f"{classes['font']} {classes['color']} {classes['font-style']} {stroke}"

        filled_template = filled_template.replace('!!CLASSES!!', all_classes)

        return filled_template

    def build_html(self, text, chat_id):
        user_input = text
        html_template = self.load_templates()

        current_directory = os.getcwd()
        path_to_currencies_view = current_directory + "/views"

        html = html_template['head']\
            .replace('!!PATH_TO_VIEWS!!', path_to_currencies_view)

        for letter in user_input:
            if letter == " ":
                html += "<span>&nbsp;</span><br>"
                continue

            if letter in list(self.symbol_letters.keys()):
                classes = self.generate_classes(have_symbol=True)
            else:
                classes = self.generate_classes(have_symbol=False)

            filled_template = self.fill_template(classes, letter, html_template['element'], chat_id)

            html += filled_template

        html += html_template['footer']

        return html

    def create_image(self, text, chat_id):
        html = self.build_html(text, chat_id)

        image_id = str(uuid4())[:13]
        image_name = f"letit-text-{image_id}"
        directory_path = "./files/"

        image_object = {
            "path": f'{directory_path}{image_name}',
            "extension": ".png"
        }

        options = {
            'format': 'png',
            'encoding': "UTF-8",
            'enable-local-file-access': None,
            'quality': '80',
            "transparent": ""
        }

        imgkit.from_string(html, f"{image_object['path']}{image_object['extension']}", options)

        return image_object

    def zip_compress_the_file(self, image_object):
        zip_path = f'{image_object["path"]}.zip'
        image_path = f'{image_object["path"]}{image_object["extension"]}'

        compression = zipfile.ZIP_DEFLATED
        with zipfile.ZipFile(zip_path, 'w', compression=compression, compresslevel=9) as zip_file:
            zip_file.write(image_path, os.path.basename(image_path))
        os.remove(image_path)

        return zip_path

    def send_image(self, message, text):
        image_object = self.create_image(text, message.chat.id)
        # zip_path = self.zip_compress_the_file(image_object)
        file_path = image_object['path'] + image_object['extension']
        with open(file_path, "rb") as file:
            self.bot.send_document(message.chat.id, document=file, timeout=240)

    def toggle_stroke(self, id):
        try:
            self.stroke_active[id] = not self.stroke_active[id]
            print(self.stroke_active[id])
        except Exception as exception:
            self.stroke_active[id] = False
            print(f"toggle_stroke\n{exception}")

    def group_log_message(self, message):
        try:
            user = message.from_user
            log_message = f'ID: {user.id}\n' \
                          f'First Name: {user.first_name}\n' \
                          f'Last Name: {user.last_name}\n' \
                          f'Nickname: {user.username}\n' \
                          f'Message: {message.text}'

            self.bot.send_message(os.getenv('LOGS_GROUP_ID'), log_message)
        except Exception as exception:
            print(exception)
