# -*- coding: utf-8 -*-
from flask import Flask, request
import hashlib
import time
import json
# import requests
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.debug = True
# BASE_URL = 'http://112.124.43.232/v1/wechat-pomodoro'
# ACCESS_TOKEN = '61e13e47ed0b1b6f6a0ebe598d5ddba0c386a0d856487ec84e973d06b1848220'
# HEADERS = {'Authorization': 'Bearer ' + ACCESS_TOKEN,
#            'Content-Type': 'application/json'}
WECHAT_TOKEN = 'asdfuiop'


@app.route('/')
def hello():
    # ds = {'id': 'abc', 'type': 'string'}
    # res = request_get("%s/datastreams/%s/datapoints" % (BASE_URL, ds['id']))
    # return res.read()
    return "Hello, world! - Wechat Pomodoro"


@app.route('/wechat', methods=['GET'])
def wechat_verify():
    echostr = request.args.get('echostr')
    if verification(request):
        return echostr
    return 'access verification fail'


@app.route('/wechat', methods=['POST'])
def wechat_msg():
    if verification(request):
        msg = parse_msg(request.data)
        if is_text_msg(msg) or is_image_msg(msg):
            return process_text(msg)
        if is_subscribe_event_msg(msg):
            return response_text_msg(msg, 'welcome')
    return 'message processing fail'


def verification(request):
    params = request.args
    signature = params.get('signature')
    timestamp = params.get('timestamp')
    nonce = params.get('nonce')

    token = WECHAT_TOKEN
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()

    if hashstr == signature:
        return True
    return False


def parse_msg(msg):
    root = ET.fromstring(msg)
    parsed_msg = {}
    for child in root:
        parsed_msg[child.tag] = child.text
    return parsed_msg


def is_text_msg(msg):
    return msg['MsgType'] == 'text'


def is_image_msg(msg):
    return msg['MsgType'] == 'image'


def is_subscribe_event_msg(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'


TEXT_MSG = u"""
<xml>
<ToUserName><![CDATA[%s]]></ToUserName>
<FromUserName><![CDATA[%s]]></FromUserName>
<CreateTime>%s</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[%s]]></Content>
<FuncFlag>0</FuncFlag>
</xml>
"""


def response_text_msg(msg, content):
    return TEXT_MSG % (msg['FromUserName'], msg['ToUserName'],
                       str(int(time.time())), content)


def process_text(msg):
    # ds = {'id': 'n'}
    # dp = {'v': 1}
    # requests.post("%s/datastreams/%s/datapoints" % (BASE_URL, ds['id']),
    #               data=json.dumps(dp),
    #               headers=HEADERS)
    return response_text_msg(msg, json.dumps(msg))

if __name__ == "__main__":
    app.run()
