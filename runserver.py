#!/usr/bin/env python
# -*- coding: utf-8 -*-

import bottle
from bottle import route, request

from config import *
from weixinclient import *

@route('/')
def index():
  if len(request.query) == 4:
    weixin = WeiXin.on_connect(
      token = WEIXINTOKEN,
      timestamp = request.query.timestamp,
      nonce = request.query.nonce,
      signature = request.query.signature,
      echostr = request.query.echostr)
    if weixin.validate():
      return request.query.echostr

  return 'WX'

# Run Server
if __name__ == '__main__':
  bottle.run(host = 'localhost', port = 7777, reloader = True, debug = True)

app = bottle.default_app()
