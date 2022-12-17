import os
import sys

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import send_text_message, send_button_message, send_image_message


load_dotenv()

machine = TocMachine(
    states = [
        'scarlet_violet',
        'pokemon_go',
        'battle',
        'type',
        'moves',
        'weakness',
        'greeting',
        'pkm_input',
        'good_at',
        'fast_moves',
        'main_moves',
        'user',
        'fsm_graph',
    ],
    transitions = [
        {'trigger': 'advance', 'source': 'user', 'dest': 'pkm_input', 'conditions': 'is_going_to_pkm_input'}, 
        {'trigger': 'advance', 'source': 'pkm_input', 'dest': 'greeting', 'conditions': 'is_going_to_greeting'},        
        {'trigger': 'advance', 'source': 'greeting', 'dest': 'pokemon_go', 'conditions': 'is_going_to_pokemon_go'},
        {'trigger': 'advance', 'source': 'greeting', 'dest': 'scarlet_violet', 'conditions': 'is_going_to_scarlet_violet'},
        {'trigger': 'advance', 'source': 'scarlet_violet', 'dest': 'battle', 'conditions': 'is_going_to_battle'},
        {'trigger': 'advance', 'source': 'scarlet_violet', 'dest': 'type', 'conditions': 'is_going_to_type'},
        {'trigger': 'advance', 'source': 'scarlet_violet', 'dest': 'weakness', 'conditions': 'is_going_to_weakness'},
        {'trigger': 'advance', 'source': 'scarlet_violet', 'dest': 'good_at', 'conditions': 'is_going_to_good_at'},
        {'trigger': 'advance', 'source': 'moves', 'dest': 'fast_moves', 'conditions': 'is_going_to_fast_moves'},
        {'trigger': 'advance', 'source': 'moves', 'dest': 'main_moves', 'conditions': 'is_going_to_main_moves'},
        {'trigger': 'advance', 'source': 'pokemon_go', 'dest': 'type', 'conditions': 'is_going_to_type'},
        {'trigger': 'advance', 'source': 'pokemon_go', 'dest': 'weakness', 'conditions': 'is_going_to_weakness'},
        {'trigger': 'advance', 'source': 'pokemon_go', 'dest': 'moves', 'conditions': 'is_going_to_moves'},
        {'trigger': 'advance', 'source': 'pokemon_go', 'dest': 'good_at', 'conditions': 'is_going_to_good_at'},
        {'trigger': 'advance', 'source': 'pkm_input', 'dest': 'fsm_graph', 'conditions': 'is_going_to_fsm_graph'},
        {
            'trigger': 'go_back', 
            'source': [
                'scarlet_violet',
                'pokemon_go',
                'battle',
                'type',
                'moves',
                'weakness',
                'greeting',
                'pkm_input',
                'good_at',
                'fast_moves',
                'main_moves',
                'fsm_graph'
            ],
            'dest': 'user'
        },
    ],
    initial = 'user',
    auto_transitions= False,
    show_conditions= True,
)

app = Flask(__name__, static_url_path='')


channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)

mode = 0

@app.route('/callback', methods=['POST'])
def webhook_handler():
    global mode
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f'Request body: {body}')

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f'\nFSM STATE: {machine.state}')
        print(f'REQUEST BODY: \n{body}')

        
        response = machine.advance(event)


        if response == False:
            if event.message.text.lower() == 'restart':
                machine.go_back()
            elif machine.state == 'pkm_input':
                send_text_message(event.reply_token,"輸入想查詢的 寶可夢 名稱")
            elif machine.state == 'greeting':
                send_text_message(event.reply_token,"輸入遊戲版本")
            elif machine.state == 'pokemon_go' or machine.state == 'scarlet_violet' or machine.state == 'moves':
                send_text_message(event.reply_token,"輸入要查詢的功能")
            elif machine.state == 'battle' or machine.state == 'type' or machine.state == 'weakness' or machine.state == 'good_at' or machine.state == 'fast_moves' or machine.state == 'main_moves':
                machine.go_back()

                

    print(f'\nFSM STATE: {machine.state}')
    return 'OK'


@app.route('/show-fsm', methods=['POST'])
def show_fsm():
    machine.get_graph().draw('fsm.png', prog='dot', format='png')
    return send_file('fsm.png', mimetype='image/png')


if __name__ == '__main__':
    port = os.environ.get('PORT', 8000)
    app.run(host='0.0.0.0', port=port, debug=True)
