import imgkit
import os

html = './views/test.html'

current_directory = os.getcwd()
path_to_currencies_view = current_directory + "/views"

with open(html, 'r') as html_file:
    html = html_file.read()

html = html.replace('!!PATH_TO_VIEWS!!', path_to_currencies_view)

image_path = 'test_chart.png'

options = {
    'format': 'png',
    'encoding': "UTF-8",
    'enable-local-file-access': None,
    'quality': '100',
    "transparent": ""
}

imgkit.from_string(html, image_path, options)

# print(type(['str']) is list)
