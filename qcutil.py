#!/usr/bin/env python
"""
qcmac is meant for a MAC OS QC of a data delivery with shasum 512 checksums.
This uses pexpect to spawn a child process of the shasum app., which should be in the user's PATH.
The shasum app. CLI invokation options are: 'shasum -a 512 -c checksum_summary_file.sha512'.
"""
# more detailed discussion/decription of this module is appended to its docstring
# at the bottome of this file ...

from __future__ import print_function

import datetime, getpass, hashlib, inspect, json, os
import pexpect, psutil, re, scandir, string, sys, timeit
if(sys.version_info.major < 3):
  import six # allows python3 syntax in python2

_sha512file = []
_log = None
_verbose = False
_usr = getpass.getuser()

def qclog(qctmp = '/var/tmp/' + _usr + '/QC'):
  """
  Open unique logfile for this QC.
  """
  global _log, _usr
  logdir = qctmp + '/log'
  now = datetime.datetime.now().strftime("%Y.%j.%H.%M.%S")
  logfile = logdir + '/' + _usr + 'QClog.' + now
  try:
    # os.mknod(logfile)
    if(not os.path.exists(logdir)): os.makedirs(logdir)
    _log = open(logfile, 'a')
    print('opened logfile: ', logfile, ' ... proceeding with QC ....')
  except:
    print('failed to open logfile: ', logfile, ' ... abort ....')
    sys.exit()

  return _log
#end qclog

def writelog(info):
  """
  Write one or more info-objects to stdout and to log-file
  """
  global _log
  if( not _log ): _log = qclog()

  if( isinstance(info, dict) ):
    print(info) ; json.dump(info, _log, sort_keys=True, indent=2)
    return

  if( isinstance(info, basestring) ):
    print(info) ; print(info, file=_log)
    return

  # if not a dict or sring, try an iterator
  try:
    it = iter(info)
    while( True ):
      val = it.next()
      print(repr(val)) ; print(repr(val), file=_log)
  except:
    return

  # assume its some sorta simple scalar, but play it safe with repr
  print(repr(info)) ; print(repr(info), file=_log)
  return
#end writelog

def yesno(text=''):
  """
  Prompt user for yes/no response, with the default response (user just hits enter) in no.
  """
  resp = getpass.getpass('qcUCB> '+text+' [y/n]: ')
  if( resp != 'y' ):
    resp = 'n'
    writelog('Ok, seems you replied with no ...')
  return resp
#end yesno

def workspace():
  """
  Check current working directory is USB volume and mounted as NTFS.
  """
  cwd = os.getcwd()
  print('Current working directoy is:', cwd)
  resp = yesno('Is this the root of the USB volume?')
  if( resp == 'n' ):
    writelog('Please cd or pushd to the root of the USB volume and restart this script ...')
#   return cwd # test here regardless ...
    sys.exit()
  #endif

  parts = psutil.disk_partitions()
  for p in parts:
    if( p.mountpoint == cwd ):
      if( p.fstype == 'ntfs' ):
        writelog('Ok found NTFS partition, proceeding with QC of: '+cwd)
        return cwd
      #endif
    #endif
  #endfor
  writelog('Oops, this is not a USB volume with NTFS? '+cwd)
  resp = yesno('Proceed with QC on this non NTFS volme?')
  if( resp == 'n' ):
    writelog('Ok abort QC ...')
    sys.exit()
  else:
    writelog('Ok proceeding with QC ...')

  return cwd
#end workspace

def dir_content(dir, items, zero_items):
  """
  Find all files in all sub-dirs and set list of full paths.
  Also check for zero content files and note those in their own list
  """
  global _sha512file # list of '*.sha512'
  for item in scandir.scandir(dir): files found
    if(item.is_dir()): dir_content(item.path, items, zero_items)
    if(not item.is_file()): continue
    items.append(item.path)
    if(item.path.endswith('.sha512')): _sha512file.append(item.path)
    try:
      sz = os.path.getsize(item.path)
      if(sz <= 0): zero_items.append(item.path)
    except:
      writelog('Oops, unable to access file (cannot determine its size)? '+item.path)
      sys.exit()
    #endtry
  #endfor

  #writelog('Total number of files found: '+repr(len(items)))
  return _sha512file
#end dir_content

__doc__ += """
This scripts relies on the user responing to prompts with yes/no (y/n).
Note the assumption of a sha512 filename convention -- '*.sha512'.
If more than 1 such file is found, the user should be prompted for instructions.
If no such file is found, a more elaborate version of this script called ddsha.py
can be used to perform the initial shasum and create the summary file.

Although this is called qcmac because it's meant to be used on a MAC OS system,
it should work on Linux too.
"""
