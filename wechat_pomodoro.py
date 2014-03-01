from flask import Flask, request
import hashlib

app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    return "Hello, world! - Flask"

@app.route('/weixin', methods=['GET'])
def weixin_verify():
    signature = request.args.get('signature')
    timestamp = request.args.get('timestamp')
    nonce = request.args.get('nonce')
    echostr = request.args.get('echostr')

    token = 'asdfuiop'
    tmplist = [token, timestamp, nonce]
    tmplist.sort()
    tmpstr = ''.join(tmplist)
    hashstr = hashlib.sha1(tmpstr).hexdigest()

    if hashstr == signature:
        return echostr
    return 'access verification fail'
