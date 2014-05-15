# -*- coding: utf-8 -*-
from flask import Flask, request
import hashlib
import time
import json
import urllib2
import xml.etree.ElementTree as ET

app = Flask(__name__)
app.debug = True
BASE_URL = 'http://112.124.43.232/v1/wechat-pomodoro'
ACCESS_TOKEN = '61e13e47ed0b1b6f6a0ebe598d5ddba0c386a0d856487ec84e973d06b1848220'


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
        if is_text_msg(msg):
            return process_text(msg)
        if is_subscribe_event_msg(msg):
            return response_text_msg(msg, 'welcome')
    return 'message processing fail'


def verification(request):
    params = request.args
    signature = params.get('signature')
    timestamp = params.get('timestamp')
    nonce = params.get('nonce')

    token = 'asdfuiop'
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()

    if hashstr == signature:
        return True
    return False


def parse_msg(msg):
    root = ET.fromstring(msg)
    msg = {}
    for child in root:
        msg[child.tag] = child.text
    return msg


def is_text_msg(msg):
    return msg['MsgType'] == 'text'


def is_subscribe_event_msg(msg):
    return msg['MsgType'] == 'event' and msg['Event'] == 'subscribe'

TEXT_MSG = \
u"""
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
    s = TEXT_MSG % (msg['FromUserName'], msg['ToUserName'],
                    str(int(time.time())), content)
    return s


def request_get(url, headers={}):
    headers['Authorization'] = "Bearer %s" % ACCESS_TOKEN
    req = urllib2.Request(url, headers=headers)
    return urllib2.urlopen(req)


def request_post(url, data, headers={}):
    headers['Authorization'] = "Bearer %s" % ACCESS_TOKEN
    headers['Content-Type'] = 'application/json'
    req = urllib2.Request(url, data, headers)
    return urllib2.urlopen(req)


def request_put(url, data, headers={}):
    headers['Authorization'] = "Bearer %s" % ACCESS_TOKEN
    headers['Content-Type'] = 'application/json'
    req = urllib2.Request(url, data, headers)
    req.get_method = lambda: 'PUT'
    return urllib2.urlopen(req)


def process_text(msg):
    ds = {'id': 'n'}
    dp = {'v': 1}
    request_post("%s/datastreams/%s/datapoints" %
                 (BASE_URL, ds['id']), json.dumps(dp))
    return response_text_msg(msg, 'start')

if __name__ == "__main__":
    app.run()
