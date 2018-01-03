import sys
from io import BytesIO

import telegram
from flask import Flask, request, send_file

from fsm import TocMachine


API_TOKEN = '480513885:AAEwQboNf9fJUuE13pBQLl4URAj5F3QCT00'
WEBHOOK_URL = 'https://21684a07.ngrok.io/hook'

app = Flask(__name__)
bot = telegram.Bot(token=API_TOKEN)
machine = TocMachine(
    states=[
        'initial',
        'name',
        'check',        
        'normal',
        
        'hungry',
        'hungry_option1',
        'hungry_option2',        

        'sick',
        'sick_option1',
        'sick_option2',        

        'boring',
        'boring_option1',
        'boring_option2',
        'boring_option3',        

        'angry',
        'angry_option1',
        'angry_option2',
        'angry_option3',
        
        'dead'
    ],
    transitions=[         
        {
            'trigger': 'advance',
            'source': 'initial',
            'dest': 'name',
            'conditions': 'is_going_to_name'
        }, 

        {
            'trigger': 'advance',
            'source': 'dead',
            'dest': 'initial',
            'conditions': 'is_going_to_initial'
        },        

        {
            'trigger': 'advance',
            'source': 'boring',
            'dest': 'boring_option1',
            'conditions': 'is_going_to_boring_option1'
        },
        {
            'trigger': 'advance',
            'source': 'boring',
            'dest': 'boring_option2',
            'conditions': 'is_going_to_boring_option2'
        },
        {
            'trigger': 'advance',
            'source': 'boring',
            'dest': 'boring_option3',
            'conditions': 'is_going_to_boring_option3'
        },

        {
            'trigger': 'advance',
            'source': 'angry',
            'dest': 'angry_option1',
            'conditions': 'is_going_to_angry_option1'
        },
        {
            'trigger': 'advance',
            'source': 'angry',
            'dest': 'angry_option2',
            'conditions': 'is_going_to_angry_option2'
        },
        {
            'trigger': 'advance',
            'source': 'angry',
            'dest': 'angry_option3',
            'conditions': 'is_going_to_angry_option3'
        },

        {
            'trigger': 'advance',
            'source': 'hungry',
            'dest': 'hungry_option1',
            'conditions': 'is_going_to_hungry_option1'
        },
        {
            'trigger': 'advance',
            'source': 'hungry',
            'dest': 'hungry_option2',
            'conditions': 'is_going_to_hungry_option2'
        },

        {
            'trigger': 'advance',
            'source': 'sick',
            'dest': 'sick_option1',
            'conditions': 'is_going_to_sick_option1'
        },
        {
            'trigger': 'advance',
            'source': 'sick',
            'dest': 'sick_option2',
            'conditions': 'is_going_to_sick_option2'
        },
        {
            'trigger': 'advance',
            'source' : ['hungry',
                        'angry',
                        'sick',
                        'boring'],
            'dest': 'normal',
            'conditions': 'do_nothing'
        },
        {
            'trigger': 'advance',
            'source' : ['hungry',
                        'hungry_option1',
                        'hungry_option2',        

                        'sick',
                        'sick_option1',
                        'sick_option2',        

                        'boring',
                        'boring_option1',
                        'boring_option2',
                        'boring_option3',        

                        'angry',
                        'angry_option1',
                        'angry_option2',
                        'angry_option3',],
            'dest': 'dead',
            'conditions': 'kill_this'
        },

        {
            'trigger': 'is_going_to_check',
            'source': 'normal',
            'dest': 'check',            
        },

        {
            'trigger': 'is_going_to_normal',
            'source' : ['name',
                        'check',
                        'boring_option1',
                        'boring_option2',
                        'boring_option3',
                        'angry_option1',
                        'angry_option2',
                        'angry_option3',
                        'hungry_option1',
                        'hungry_option2',
                        'sick_option1',
                        'sick_option2'],
            'dest': 'normal',             
        },
        {
            'trigger': 'is_going_to_hungry',
            'source': 'normal',
            'dest': 'hungry',             
        },
        {
            'trigger': 'is_going_to_sick',
            'source' : ['normal',
                        'angry'],
            'dest': 'sick',             
        },
        {
            'trigger': 'is_going_to_angry',
            'source' : ['normal',
                        'boring'],
            'dest': 'angry',             
        },
        {
            'trigger': 'is_going_to_boring',
            'source': 'normal',
            'dest': 'boring',             
        },
        {
            'trigger': 'is_going_to_dead',
            'source' : ['hungry',
                        'sick'],
            'dest': 'dead',             
        }
    ],
    initial='initial',
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
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    machine.advance(update)
    return 'ok'


@app.route('/show-fsm', methods=['GET'])
def show_fsm():
    byte_io = BytesIO()
    machine.graph.draw(byte_io, prog='dot', format='png')
    byte_io.seek(0)
    return send_file(byte_io, attachment_filename='fsm.png', mimetype='image/png')


if __name__ == "__main__":
    _set_webhook()
    app.run()
