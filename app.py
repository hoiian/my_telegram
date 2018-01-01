import sys
import telebot
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '489589959:AAFUyzPE9CwU-1AyetlpZUfL0kgnv4OsGQo'
WEBHOOK_URL = 'https://4e9b7949.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'user',
        'state1',
        'state2',
        'state3',
        'state4'
    ],
    transitions=[
        {
            'trigger': 'advance',
            'source': [
                'user',
                'state2',
                'state4'
            ],
            'dest': 'state1',
            'conditions': 'to_a'
        },
        {
            'trigger': 'advance',
            'source': [
                'user',
                'state1',
                'state3',
                'state4'
            ],
            'dest': 'state2',
            'conditions': 'to_b'
        },
        {
            'trigger': 'go_back',
            'source': [
                'state1',
                'state2'
            ],
            'dest': 'user'
        },
        {
            'trigger':'advance',
            'source': 'state1',
            'dest': 'state3',
            'conditions': 'a_to_c'
        },
        {
            'trigger':'advance',
            'source': 'state2',
            'dest': 'state4',
            'conditions': 'b_to_d'
        }
    ],
    initial='user',
    auto_transitions=False,
    show_conditions=True,
)

def _set_webhook():
    status = bot.set_webhook(WEBHOOK_URL)
    if not status:
        print('Webhook setup failed')
        sys.exit(1)
    else:
        print('Your webhook URL has been set to "{}"'.format(WEBHOOK_URL))


@app.route('/hook', methods=['POST'])
def webhook_handler():
    # if request.method == "POST":
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    # bot.send_message(chat_id=bot.chat_id,text=":)")
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')

# @bot.message_handler(commands=['help', 'start'])
# def send_welcome(message):
#     bot.reply_to(message,
#                  ("Hi there, I am EchoBot.\n"
#                   "I am here to echo your kind words back to you."))

if __name__ == "__main__":
    _set_webhook()
    app.run()
    # bot.polling()