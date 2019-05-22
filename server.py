#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import os
import argparse
import json
from flask import Flask, request, stream_with_context, render_template
import BDD

DEST = 'data'
application = Flask(__name__)
application.config['MAX_CONTENT_LENGTH'] = 9999999
CURRENT_PATH = os.path.dirname(os.path.realpath(__file__))

@application.route('/result', methods=['GET'])
def Score():
    return render_template('result.html', voicecount=BDD.GetVotesCount(), scores=BDD.getScores())

@application.route('/response', methods=['POST'])
def GetResponse():
    if BDD.clientExists(IP=request.remote_addr, USER_AGENT=request.headers.get('User-Agent')):
        return ''
    try:
        responselist = json.loads('[{}]'.format(str(request.stream.read(), 'UTF-8')))
        if all(int(i) < len(BDD.getQuestions()) and int(i) >= 0  for i in responselist):
            print('before')
            userid = BDD.createUser(IP=request.remote_addr, USER_AGENT=request.headers.get('User-Agent'))
            BDD.insertResponse(userid, responselist)
            print('done')
    finally:
        print('exception')
        return ''

@application.route('/', methods=['GET'])
def showSondage():
    return render_template('index.html', title='Enquête Slow Transfert', choicelist=BDD.getQuestions())


def parse_command_line():
    parser = argparse.ArgumentParser(description='Launch phishing server (Flask)')
    parser.add_argument('--host', help='Host Adress to listen to', default="0.0.0.0")
    parser.add_argument('--port', help='Port Adress to listen to', type=int, default=8000)
    parser.add_argument('--nossl', help="Service doesn't use SSL", action="store_true", default=True)
    parser.add_argument('--cert', help='Specific certificate to use for SSL')
    parser.add_argument('--key', help='Specific key to use for SSL')
    return parser.parse_args()

if __name__ == '__main__':
    args = parse_command_line()
    if args.nossl:
        application.run(threaded=True, host=args.host, port=args.port, debug=False)
    else:
        ssl_context=(args.cert, args.key)
        application.run(threaded=True, host=args.host, port=args.port, debug=False, ssl_context=ssl_context)
