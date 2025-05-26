# CorrectNames.py ----------------------------------------------------------
# Read directory of PDF files, and remove illegal chars from names
#  
# 
# 
#
#---------------------------------------------------------------------------

import ftplib, os
from string import maketrans

def FilterRemoteDirectory(host, username, password):
  "Check all filenames in remote scan directory, rename badly formatted names."
  f=ftplib.FTP(host, username, password)
  f.cwd('scans')
  dirlist = f.nlst('.')
  filelist = []
  #Get list of filenames, filter out all but .pdf files
  for name in dirlist:
    if '.pdf' in name:
      filelist.append(name.replace('.pdf',''))
  badnamelist = []
  table = maketrans('','')
  for name in filelist:
    nametrans = name.translate(table,'"\'&*~!@#$%^&*()+`{}[];:<>,/?.')
    if name!=nametrans:
      badnamelist.append([name, nametrans])
  print 'Server: %i incorrectly formatted names'%len(badnamelist)
  # Rename poorly formatted files
  for names in badnamelist:
    print 'Renaming '+names[0]+'.pdf',names[1]+'.pdf'
    f.rename(names[0]+'.pdf',names[1]+'.pdf')

def FilterLocalDirectory():
  "Check all filenames in local scan directory, rename badly formatted names."
  os.chdir('scans')
  dirlist = os.listdir('.')
  filelist = []
  #Get list of filenames, filter out all but .pdf files
  for name in dirlist:
    if '.pdf' in name:
      filelist.append(name.replace('.pdf',''))
  badnamelist = []
  table = maketrans('','')
  for name in filelist:
    nametrans = name.translate(table,'"\'&*~!@#$%^&*()+`{}[];:<>,/?.')
    if name!=nametrans:
      badnamelist.append([name, nametrans])
  print 'Local: %i incorrectly formatted names'%len(badnamelist)
  # Rename poorly formatted files
  for names in badnamelist:
    print 'Renaming '+names[0]+'.pdf',names[1]+'.pdf'
    os.rename(names[0]+'.pdf',names[1]+'.pdf')

  
def main():
  """Correct all of the filenames in the scan subdirectory to remove illegal chars"""
  #Username and Password for Michael's FTP account
  host = "ftp.spencersmithlab.org"
  username = "mgiltz@spencersmithlab.org"
  password = "wsh1awnnyer"
  FilterLocalDirectory()
  FilterRemoteDirectory(host, username, password)
  #Filter remote web directory
  #FilterRemoteDirectory(host, username, password)

  
if __name__ == '__main__': main()

