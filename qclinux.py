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

def shasum_check(file, ok_checks, notok_checks):
  """
  Invokes MACOS CLI: shasum -a 512 -c filename
  The text file should contain a list of shasum results and filenames
  TBD: check if Linux provides the same CLI ...
  """
  checkcmd = 'shasum -a 512 -c ' + file
  start_time = timeit.default_timer()
  try:
    child = pexpect.spawn(checkcmd)
#    child.setlog(_log)
    child.maxsize = 1  #Turns off buffering
    child.timeout = 45 # default is 30, insufficient for me. Crashes were due to this param.
    for line in child:
      writelog(line)
      if( line.rindex(': OK') > 0 ):
        ok_checks.append(line)
      else:
        notok_checks.append(line)
    #endfor
  except pexpect.TIMEOUT:
    writelog('pexpect timeout on: ' + checkcmd)
  except pexpect.EOF:
    writelog('pexpect EOF from: ' + checkdmc)
  #endtry
  elapsed = timeit.default_timer() - start_time
  okcnt = len(ok_checks) ; notcnt = len(notok_checks)
  writelog('Shasum check Ok cnt: ' + repr(okcnt) + ' ... Not Ok cnt: ' + repr(notcnt))
  return elapsed
#end shasum_check

def main(verbose=True):
  """
  Main entry func. for 'qcmac'
  """
  global _verbose
  _verbose = verbose
  redmine = 'https://redmine.biotech.ufl.edu/projects/day-to-day/wiki/How_to_Perform_Data_Delivery_QC'
  writelog('Feel free to review this ICBR Redmine Wiki page, which describes how to reset the USB PIN and perform the QC: ')
  writelog(redmine)
  writelog('This script attempts to step through the QC with a bit of user interaction ...')
  cwd = workspace()
  items = [] ; zero_items = []
  sha512file_list = dir_content(cwd, items, zero_items)
  sha512file_cnt = len(sha512file_list)
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
    writelog('Abort QC due to incorrect sha512 list file: '+repr(_sha512file))
    sys.exit()
  #endif
  # shas = shasum512list(items) ; writelog(shas)
  elapsed = 0 ; okcnt = 0 ; ok_checks = [] ; notok_checks = []
  if(sha512file_cnt > 0 ):
    writelog('Ok proceeding with check cmd shasum -c using: ' + _sha512file[0])
    elapsed = shasum_check(_sha512file[0], ok_checks, notok_checks)
  #endif
  writelog('Elapsed time: ' + repr(elapsed))

if __name__ == "__main__":
  main(*sys.argv[1:])

__doc__ += """
This scripts relies on the user responing to prompts with yes/no (y/n).
Note the assumption of a sha512 filename convention -- '*.sha512'.
If more than 1 such file is found, the user should be prompted for instructions.
If no such file is found, a more elaborate version of this script called ddsha.py
can be used to perform the initial shasum and create the summary file.

Although this is called qcmac because it's meant to be used on a MAC OS system,
it should work on Linux too.
"""
