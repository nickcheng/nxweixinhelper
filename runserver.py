#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from bottle import route, request
import csv, time

from config import *
from weixinclient import *

def ll(i):
  f = open('xxx.txt', 'a')
  f.write(i)
  f.write('\r\n')

@route('/', ['GET', 'POST'])
def index():
  if request.query.signature and request.query.timestamp and request.query.nonce:
    weixin = WeiXin.on_connect(
      token = WEIXINTOKEN,
      timestamp = request.query.timestamp,
      nonce = request.query.nonce,
      signature = request.query.signature,
      echostr = request.query.echostr)
    if weixin.validate():
      if request.query.echostr:
        return request.query.echostr
      elif request.method == 'POST':
        ll(request.body.readlines()[0])
        weixin = WeiXin.on_message(request.body.readlines()[0])
        j = weixin.to_json()
        ll('Converted to json')

        f = open('log.txt', 'a')
        wr = csv.writer(f)
        statusList = [j['ToUserName'], j['FromUserName'], j['CreateTime'], j['MsgType'], j['Content'], j['MsgId']]
        wr.writerow([(isinstance(v,unicode) and v.encode('utf8') or v) for v in statusList])
        f.close()

        weixinReply = WeiXin()
        result = weixinReply.to_xml(
          to_user_name = j['FromUserName'],
          from_user_name = j['ToUserName'],
          create_time = int(time.time()),
          msg_type = 'text',
          content = u'真的谢谢你哟!',
          func_flag = 0)

        return result

  # Last line
  return 'Here'

# Run Server
if __name__ == '__main__':
  bottle.run(host = 'localhost', port = 7777, reloader = True, debug = True)

app = bottle.default_app()
