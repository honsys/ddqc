#!/usr/bin/env python

from __future__ import print_function

import datetime, getpass, hashlib, inspect, json, os
import pexpect, psutil, re, scandir, ssl, string, sys
if(sys.version_info.major < 3):
  import six # allows python3 syntax in python2

# in the event we need to perform ssl transactions without published certificates:
ssl._create_default_https_context = ssl._create_unverified_context

_sha512file = []
_log = None
_verbose = False
_usr = getpass.getuser()

def qclog(qctmp = '/var/tmp/' + _usr + '/QC'):
  """
  open unique logfile for this QC.
  """
  global _log, _usr
  logdir = qctmp + '/log'
  now = datetime.datetime.now().strftime("%Y.%j.%H.%M.%S")
  logfile = logdir + '/' + _usr + 'QClog.' + now
  try:
    # os.mknod(logfile)
    if(not os.path.exists(logdir)): os.makedirs(logdir)
    _log = open(logfile, 'a')
  except:
    print('failed to open logfile: ', logfile, ' ... abort ....')
    sys.exit()

  return _log
#end qclog

def writelog(info):
  """
  write one or more info-objects to stdout and to log-file
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
  prompt user for yes/no response, with the default response (user just hits enter) in no.
  """
  resp = getpass.getpass('qcUCB> '+text+' [y/n]: ')
  if( resp != 'y' ):
    resp = 'n'
    writelog('Ok, seems you replied with no ...')
  return resp
#end yesno

def workspace():
  """
  check current working directory is USB volume and mounted as NTFS.
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
  find all files in all sub-dirs and set list of full paths.
  also check for zero content files and note those in their own list
  """
  global _sha512file
  for item in scandir.scandir(dir):
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
  return len(_sha512file)
#end dir_content

def shasum512(filename):
  """
  read file into buffer and eval sha512
  log result in the same format as shasum -a 512 to be double-checked via shasum -c
  note sym-links may point to non-existant filesystem item
  """
  global _verbose
  if(_verbose): print(filename)

  filesha = { filename : None }
  try:
    f = open(filename, 'rb') ; s = hashlib.sha512()
    # for really large files may need multiple read-n-update
    buff = f.read() ; s.update(buff) ; shasum = s.hexdigest()
    filesha = { filename : shasum }
    if(_verbose): print(shasum + '  ' + flename)
  except OSError as err:
    print("OS error: {0}".format(err))
  except:
    if(_verbose): print("non OS error:", sys.exc_info()[0]) ; pass
  #endtry
  return filesha
#end shasum512

def shasum512list(filelist, logfilename=None, verbose=False):
  """
  evaluate and log sha512 checksums of a list of files, populate and return
  a list of non-None { filename : shasum } hash-dicts.
  """
  global _verbose
  shasums = {}
  for filename in filelist:
    filesha = shasum512(filename) # return a single key-val dict
    if(_verbose): print('shasum512list> ', filesha)
    if(filesha[filename]): shasums.update(filesha)
  #endfor
  return shasums
#end shasum512list

def main(verbose=True):
  global _verbose
  _verbose = verbose
  redmine = 'https://redmine.biotech.ufl.edu/projects/day-to-day/wiki/How_to_Perform_Data_Delivery_QC'
  writelog('Feel free to review this ICBR Redmine Wiki page, which describes how to reset the USB PIN and perform the QC: ')
  writelog(redmine)
  writelog('This script attempts to step through the QC with a bit of user interaction ...')
  cwd = workspace()
  items = [] ; zero_items = []
  sha512file_cnt = dir_content(cwd, items, zero_items)
  cnt0 = len(zero_items)
  if(cnt0 > 0 ):
    for f0 in zero_items: writelog('zero content file: '+f0)
    resp = yesno('Found some '+repr(cnt0)+' zero content files ... should shasum check proceed?')
    if(resp == 'n'):
      writelog('Abort QC due to presence of 0 content file count: '+repr(cnt0))
      sys.exit()
    else:
      writelog('Continuing QC despite 0 content file count: '+repr(cnt0))
  #if cnt0
  resp = yesno('Found sha512 list file(s): ' + repr(sha512file_cnt) + ' ... ' + repr(_sha512file) + ' ... proceed?')
  if(resp == 'n'):
    writelog('Abort QC due to incorrect sha512 list file: '+repr(sha512file))
    sys.exit()
  #endif
  shas = shasum512list(items)
  writelog(shas)

if __name__ == "__main__":
  main()
