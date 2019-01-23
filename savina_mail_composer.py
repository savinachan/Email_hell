#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys, os
import re
import datetime
import base64

CRLF = "\r\n"

def add_pattern(content):
   return "=?utf-8?B?" + base64.b64encode(content.encode('utf-8')).decode('utf-8') + "?="

class text_message:
   def __init__(self):
      self.headers = {}
      self.body = ""
   '''
   def is_chinese(self, uchar):
      if uchar >= u'\u4e00' and uchar <= u'\u9fff':
         return True
      else:
         return False
   '''
   def _parse_value(self, _name, _value):

      _key = _name.capitalize()
      print(_key,_value)
      if _key == "Date":
         try:
            _value = datetime.datetime.fromtimestamp(int(_value)).strftime('%a, %d %b %Y %H:%M:%S') + CRLF
            return (_key, _value)
         except ValueError:
            print("[Error] field body of Date with invalid syntax. (%s) should be an integer. Compose mail fail." % _value[:-1])
            return (None, None)
      elif _key == "To" or _key == "From" or _key == "Cc":
         _tar = _value.split()
         
         if '@' not in _tar[-1]:
            print("[Warning] field body of %s with invalid syntax. (%s) should contain \"@\"." % (_key, _tar[-1]))

         if len(_tar) > 1:
            display_name = "\"%s\"" % (' '.join(_tar[:-1]))
            result = re.match(r'(.*[\u4e00-\u9fff]+)', display_name)
            if result:
               display_name = add_pattern(display_name)
                  
            _value = display_name + " <" + _tar[-1] + ">" + CRLF		
         else:
            _value = "<" + _tar[-1] + ">" + CRLF	
      elif _key == "Subject":
         result = re.match(r'(.*[\u4e00-\u9fff]+)', _value)
         if result:
            _value = add_pattern(_value) + CRLF
         
      else:
         return (None, None)

      '''
      ch_flag = 0
      _tar = ""
      for chr in _value:
         if self.is_chinese(chr) and ch_flag == 0:
            ch_flag = 1
            _tar += "=?utf-8?B?" + base64.b64encode(chr.encode('utf-8')).decode('utf-8')
         elif not self.is_chinese(chr) and ch_flag == 1:
            ch_flag = 0
            _tar += "?=" + chr
         elif self.is_chinese(chr):
            _tar += base64.b64encode(chr.encode('utf-8')).decode('utf-8')
         else:
             _tar += chr
      _value = _tar
      '''
      return (_key, _value)

   def add_header(self, _name, _value):
      if _name is not None and _value is not None:
         _key, _value = self._parse_value(_name, _value)

      if _key == None:
         return

      if _key not in self.headers:
         self.headers[_key] = _value
      elif _key in self.headers:
         self.headers[_key] = self.headers[_key][:-1]+", "+_value

   def verifiy_field(self):
      if "From" not in self.headers:
         print ('[ERROR] Please specify sender. Compose mail fail.')
         return False
      if "To" not in self.headers:
         print ('[ERROR] Please specify receiver. Compose mail fail.')
         return False
      if "Date" not in self.headers:
         print ('[ERROR] Please specify date. Compose mail fail.')
         return False
		
      return True

if __name__ == '__main__':
   if len(sys.argv) < 3:
      print("Usage: python3 %s <input file> <output file>" % sys.argv[0])
      exit(0)

   lines = list()
   delimited = 0
   if os.path.exists(sys.argv[1]):
      try:
         input_file = open(sys.argv[1], "r")
         lines = input_file.readlines()
         input_file.close()
      except Exception:
         exit(0)
   else:
      print("[Error] %s file not exist. Compose mail fail." % sys.argv[1])
      exit(0)

   if len(lines) > 0:
      msg = text_message()
      for line in lines:
         if ':' in line and delimited == 0:
            msg.add_header(line[:line.find(":")], line[line.find(":")+1:])
         elif delimited == 1:
            msg.body += line
         elif line == "\r\n" or line == "\n" or line == "\r":
            delimited = 1

      if msg.verifiy_field():
         output_file = open(sys.argv[2], "w")
         for k,v in msg.headers.items():
            output_file.write(k+": "+v)
         if len(msg.body) > 0:				
            output_file.write(CRLF + msg.body)
         output_file.close()
         print ('Compose Mail Success.')
   else:
      print("[Error] Input file is empty.")
'''
      for k, v in msg.headers.items():
         print(k+"."+v)
      print(msg.body)
'''
