# FTPtest.py ----------------------------------------------------------
# Read directory of PDF files, and remove illegal chars from names
#---------------------------------------------------------------------------

import ftplib, os
from string import maketrans

def FilterRemoteDirectory(host, username, password):
  "Check all filenames in remote scan directory, rename badly formatted names."
  f=ftplib.FTP(host, username, password)
  f.cwd('scans')
  dirlist = f.nlst('.')
  print 'Directory has %i entries'%len(dirlist)


  
def main():
  """Correct all of the filenames in the scan subdirectory to remove illegal chars"""
  #Username and Password for Michael's FTP account
  host = "ftp.spencersmithlab.org"
  username = "mgiltz@spencersmithlab.org"
  password = "wsh1awnnyer"
  #FilterLocalDirectory()
  FilterRemoteDirectory(host, username, password)
  #Filter remote web directory
  #FilterRemoteDirectory(host, username, password)

  
if __name__ == '__main__': main()

