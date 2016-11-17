#!/usr/bin/env python
"""
ncz.py should behave something like nc -z IP port ... with the option to scan
the entire range of port numbers from 0 to 65536.
"""

from __future__ import print_function
import os, string, sys
if sys.version_info.major < 3: import six # allows python3 syntax in python2
import socket, errno, os, time, select

def connect(ip='10.101.11.129', port=22, cntsec=2):
  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  # sock.setblocking(0)
  sock.settimeout(.100)
  try:
    sock.connect((ip, port))
  except socket.error, exc:
    # print('exception socket.error: ',repr(exc))
    return None
  return sock
#end connect

def findListeners(ip='10.101.11.129', list=[]):
  port = 22 ; max = 65536
  while(port <= max):
    sock = connect(ip, port)
    if( sock != None ):
      print('\nFound listener: ', ip, port)
      sock.close()
      list.append(port)
    else:
      # print('No listener: ', ip, port)
      sys.stdout.write('.'+str(port)) ; sys.stdout.flush()
    #endif
    port += 1
  #endwhile
  return len(list)
#end findListeners

if __name__ == '__main__':
  ip = '10.101.11.129'
  # ip = '10.101.8.94'
  if len(sys.argv) > 1: ip = sys.argv[1]
  list = []
  cnt = findListeners(ip, list)
