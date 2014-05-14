#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import xml.etree.ElementTree as ET

class WeiXin(object):
  def __init__(self, token=None, timestamp=None, nonce=None, signature=None, echostr=None, xml_body=None):
    self.token = token
    self.timestamp = timestamp
    self.nonce = nonce
    self.signature = signature
    self.echostr = echostr

    self.xml_body = xml_body

  @classmethod
  def test(self):
	  return 'class'

  @classmethod
  def on_connect(self, token=None, timestamp=None, nonce=None, signature=None, echostr=None):
    obj = WeiXin(token=token,
      timestamp=timestamp,
      nonce=nonce,
      signature=signature,
      echostr=echostr)
    return obj

  @classmethod
  def on_message(self, xml_body):
    obj = WeiXin(xml_body=xml_body)
    return obj

  def to_json(self):
    '''http://docs.python.org/2/library/xml.etree.elementtree.html#xml.etree.ElementTree.XML
    '''
    j = {}
    root = ET.fromstring(self.xml_body)
    for child in root:
      if child.tag == 'CreateTime':
        value = long(child.text)
      else:
        value = child.text
      j[child.tag] = value
    return j

  def _to_tag(self, k):
    return ''.join([w.capitalize() for w in k.split('_')])

  def _cdata(self, data):
    '''http://stackoverflow.com/questions/174890/how-to-output-cdata-using-elementtree
    '''
    if type(data) is str:
      return '<![CDATA[%s]]>' % data.replace(']]>', ']]]]><![CDATA[>')
    return data

  def to_xml(self, **kwargs):
    xml = '<xml>'
    def cmp(x, y):
      ''' WeiXin need ordered elements?
      '''
      orderd = ['to_user_name', 'from_user_name', 'create_time', 'msg_type', 'content', 'func_flag']
      try:
        ix = orderd.index(x)
      except ValueError:
        return 1
      try:
        iy = orderd.index(y)
      except ValueError:
        return -1
      return ix - iy
    for k in sorted(kwargs.iterkeys(), cmp):
      v = kwargs[k]
      tag = self._to_tag(k)
      xml += '<%s>%s</%s>' % (tag, self._cdata(v), tag)
    xml += '</xml>'
    return xml

  def validate(self):
    params = {}
    params['token'] = self.token
    params['timestamp'] = self.timestamp
    params['nonce'] = self.nonce

    signature = self.signature

    if self.is_not_none(params):
      gen_signature = self.gen_signature(params)
      if gen_signature == signature:
        return True
    return False

  def is_not_none(self, params):
    for k, v in params.items():
      if v is None:
        return False
    return True

  @classmethod
  def gen_signature(self, params):
    '''http://docs.python.org/2/library/hashlib.html
    '''
    a = sorted([v for k, v in params.items()])
    s = ''.join(a)
    return hashlib.sha1(s).hexdigest()