import os
import time
import copy
import yaml
import json
import logging
import argparse

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *


from utils import check_input_valid
from utils import is_input_command
from utils import input_context_msg, input_question_msg, input_answer_msg, input_reset_msg
from utils import input_template as input_
from utils import question_limit

## extra files
from update_DB_information import *
from utils_py.execute_flow import *


# setup logger
logging.basicConfig(
    level="INFO",  # INFO, DEBUG
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# check env variables
logger.debug("Check environment variables")
for env_k, env_v in os.environ.items():
    logger.debug(f'{env_k}: {env_v}')


# parse args
parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--model', help='Select model', default='bert', required=False, choices=['bert', 'bidaf'])
parser.add_argument('--example', help='Use example to test model', action='store_true')
args, unknown = parser.parse_known_args()

# setup app
app = Flask(__name__)
TSP_LineBot = TSP()
read_db()

'''
# load example
if args.example:
    with open('line-bot/example.json', 'r') as f:
        example_input = json.load(f)
        logger.debug(f'Loaded example: {example_input}')
'''

# load config
config_path = 'config.yml'
try:
    with open(config_path, 'r') as yml_f:
        config = yaml.load(yml_f, Loader=yaml.BaseLoader)
    
    print(config)
    
    # Channel Access Token
    line_bot_api = LineBotApi(config['Linebot']['access_token'])

    # Channel Secret
    handler = WebhookHandler(config['Linebot']['secret'])
    
except:
    print('web hook gone')
    logger.exception(f'Please check if {config_path} exists')


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    body_dict = json.loads(body)
    print(body_dict)
    # handle webhook body
    try:
        if "latitude" in body_dict["events"][0]["message"].keys():
            TSP_LineBot.location["latitude"] = body_dict["events"][0]["message"]["latitude"]
            TSP_LineBot.location["longitude"] = body_dict["events"][0]["message"]["longitude"]
            TSP_LineBot.location["title"] = body_dict["events"][0]["message"]["title"]

        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    def reply(text):
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=text))
    
    message = TextSendMessage(text=event.message.text)
    
    if isfloat(message.text):
        TSP_LineBot.radius = float(message.text)
        reply(f'你選擇的搜尋距離是 {TSP_LineBot.radius} km')

    if message.text == 'find restaurant':
        url, tsp_result = TSP_LineBot.execute_all()
        path = f'你選擇的搜尋距離是 {TSP_LineBot.radius}km \n 一共有{len(tsp_result)}家\n'
        for i in range(len(tsp_result)):
            path += f'{i+1} : {tsp_result[i][0]}\n'
        
        path += f'\n來看看路徑吧 :\n {url}'

        reply(path)





if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
