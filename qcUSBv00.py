#!/usr/bin/env python

from __future__ import print_function

import datetime, getpass, json, os, pexpect, psutil, re, ssl, string, sys
if(sys.version_info.major < 3):
  import six # allows python3 syntax in python2

# in the event we need to perform ssl transactions without published certificates:
ssl._create_default_https_context = ssl._create_unverified_context
_log = None

def qclog():
  usr = getpass.getuser()
  qcdir = '/var/tmp/' + usr + '/QC'
  logdir = qcdir + '/log'
  now = datetime.datetime.now().strftime("%Y.%j.%H.%M.%S")
  logfile = logdir + '/' + usr + 'QClog.' + now
  log = None
  try:
    # os.mknod(logfile)
    if(not os.path.exists(logdir)): os.makedirs(logdir)
    log = open(logfile, 'a')
  except:
    print('failed to open logfile: ', logfile, ' ... abort ....')
    sys.exit()

  return log
#end qclog

def writelog(items):
  global _log
  if( not _log ): _log = qclog()
  json.dump(items, _log)
#  for i in items: _log.write(i+'\n')
  print(items)

def yesno(text=''):
  resp = getpass.getpass('qcUCB> '+text+' [y/n]: ')
  if( resp != 'y' ):
    resp = 'n'
    writelog('Ok, seems you replied with no ...')
  return resp
#end yesno

def workspace():
  cwd = os.getcwd()
  print('Current working directoy is:', cwd)
  resp = yesno('Is this the root of the USB volume?')
  if( resp == 'n' ):
    writelog(['Please cd or pushd to the root of the USB volume and restart this script ...'])
    sys.exit()
  #endif

  cwdpart = None
  parts = psutil.disk_partitions()
  for p in parts:
    if( p.mountpoint == cwd ):
      if( p.fstype == 'ntfs' ):
        writelog('Ok found NTFS partition, proceeding with QC of: '+cwd)
        return cwd

  writelog('Oops, this is note a USB volume with NTFS? '+cwd)
  return None
#end workspace

def dir_content(dir):
  items = [os.path.join(dir, f) for f in os.listdir(dir)]
  for i in items:
    print(i)
#end lsdir
  return items

if __name__ == "__main__":
  cwd = workspace()
  items = dir_content(cwd)
  writelog(items)
