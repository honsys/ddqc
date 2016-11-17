#!/usr/bin/env python

from __future__ import print_function
import os, string, sys
if sys.version_info.major < 3: import six # allows python3 syntax in python2
import socket, errno, os, time, select

def connect(ip='10.101.11.129', port=22, cntsec=2):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  sock.setblocking(0)
  err = sock.connect_ex((ip, port)) ; print(err)
  errcode = errno.errorcode[err] ; print(errcode)
  while(cntsec > 0):
    time.sleep(.500) # sleep 999 millisec
    try:
      err = sock.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
      print(err) ; errcode = errno.errorcode[err] ; print(errcode)
    except: pass
    cntsec = cntsec - 1
  #end while
  if( errcode != 0 ): sock = None
  return sock
#end connect

def findListeners(ip='10.101.11.129', list=[]):
  port = 22 ; max = 65536
  while(port <= max):
    sock = connect(ip, port)
    if( sock != None ):
      print('something is listing at ', ip, port)
      sock.close()
      list.append(port)
    else:
      print('nothing is listing at ', ip, port)
    #endif
    port += 1
  #endwhile
  return len(list)
#end findListeners

if __name__ == '__main__':
  ip = '10.101.11.129'
  list = []
  cnt = findListeners(ip, list)
