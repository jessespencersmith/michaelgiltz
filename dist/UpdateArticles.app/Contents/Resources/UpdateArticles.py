# MakeLinks.py ----------------------------------------------------------
# Read directory of PDF files, and create a text file of web links 
# appropriate for Michael's web page. Cut and paste into the correct 
# web page.
# Should always be run in web directory, with scans an immediate subfolder.
#
#---------------------------------------------------------------------------

import os, os.path, glob, time, ftplib

def NameFormatCheck(namelist):
  """Filenames naming convention: publication-Title_of_Article-Month-Day-Year.pdf
  Check names for proper formatting (order, number, dates, return list of good and bad names"""
  
  def good_date(year, month, day):
    tup1 = (year, month, day, 0,0,0,0,0,0)
    try:
      date = time.mktime (tup1)
      tup2 = time.localtime (date)
      if tup1[:2] != tup2[:2]:
        return False
      else:
        return True
    except OverflowError:
      return False

  goodnames = []
  badnames = []
  for filename in namelist:
    #Remove extension
    rawinfo = filename.rstrip(".pdf")
    #Check all data
    try: 
      pub, title, month, day, year = rawinfo.split("-")
      if good_date(int(year), int(month), int(day)):
        #Good date
        goodnames.append(filename)
      else:
        #Bad date
        #print "Bad date (illegal date): "+filename
        #print
        badnames.append(filename)
    except ValueError:
      #print "Bad format: "+filename
      #print "Format: Publication-Title_of_Article-Month-Day-Year.pdf"
      #print
      badnames.append(filename)
  return((goodnames, badnames))

def FilterRemoteDirectory(host, username, password):
  "Check all filenames in remote scan directory, remove badly formatted names."
  #Read all the file names. Assumes it is being run in the parent directory of the files.
  # Log in to server
  f=ftplib.FTP(host, username, password)
  dirlist = f.nlst('scans')
  filelist = []
  #Get list of filenames, filter out all but .pdf files
  for name in dirlist:
    if '.pdf' in name:
      filelist.append(name)
  (goodnamelist, badnamelist) = NameFormatCheck(filelist)
  print 'Server: %i incorrectly formatted names'%len(badnamelist)
  # Move badnamelist files to BadFormatPDFs
  for name in badnamelist:
    print 'Moving '+name
    f.rename('scans/'+name,'BadFormatPDFs/'+name)
    
def FilterLocalDirectory():
  "Check all filenames in scan directory, remove badly formatted names."
  #Read all the file names. Assumes it is being run in the parent directory of the files.
  os.chdir("scans")
  filelist = glob.glob("*.pdf")
  os.chdir("..")
  (goodnamelist, badnamelist) = NameFormatCheck(filelist)
  print 'Local: %i incorrectly formatted names'%len(badnamelist)
  # Move badnamelist files to BadFormatPDFs
  for name in badnamelist:
    if os.access(os.path.join('BadFormatPDFs',name),os.X_OK):
      print 'Already in BadFormatPDFs directory, deleting '+name
      os.remove(os.path.join('scans',name))
    else:
      print 'Moving '+name
      os.rename(os.path.join('scans',name),os.path.join('BadFormatPDFs', name))
      
def MakeArticleDict():
  """Read all files in current directory, turn into lists of links for inclusion on pages
     Filenames naming convention: publication-Title_of_Article-Month-Day-Year.pdf"""
  #Read all the file names. Assumes it is being run in the posarent directory of the files.
  os.chdir("scans")
  filelist = glob.glob("*.pdf")
  os.chdir("..")
  pubdatetitlelist = []
  for name in filelist:
      #Put keys in front
      name = name.replace('.pdf','')
      try: 
        pub, title, month, day, year = name.split("-")
        info = pub, year, "%02i"%int(month), "%02i"%int(day), month, day, title
        pubdatetitlelist.append("-".join(info))
      except ValueError:
        print "ERROR! Bad format, not caught by NameFormatCheck: "+name
  
  #Sort all filenames by publication
  pubdatetitlelist.sort()
  
  #Create dictionary to hold all article links
  articles = {}
  prev = "" 
  for rawinfo in pubdatetitlelist:
    # Format for link text
    try: 
      pub, year, keymonth, keyday, month, day, title = rawinfo.split("-")
    except:
      print "Bad string in goodlist!!!"+rawinfo
      print
      print

    if pub!=prev:
      prev = pub
      articles[pub] = []
    displayname = title.replace("_"," ")
    # Add string to pub list
    articlelink ='<a href="scans/%(pub)s-%(title)s-%(month)s-%(day)s-%(year)s.pdf">%(displayname)s, %(month)s-%(day)s-%(year)s</a><br>' % {'pub':pub, 'title':title, 'month':month, 'day':day, 'year':year, 'displayname':displayname}
    articles[pub].append(articlelink)
  return(articles)  

  
def UpdatePages(articles):
  # Pages contain names(s) of links to be included <!-- list:HuffPo -->
  # Get list of all .htm files in directory
  pages = glob.glob("*.htm")
  # Clear backup directory
  for filename in os.listdir("backup"): ## USE PROPER SEPARATOR
    os.remove(os.path.join("backup",filename))
  # Move all web pages pages to backup folder
  for pagename in pages:
    os.rename(pagename,os.path.join('backup',pagename))
    htmlpage = open(os.path.join('backup', pagename)) # Open original file
    newhtmlpage = open(pagename,'w') # Open new file
    inlist = False # Doesn't start out in article section
    for htmlline in htmlpage:
      if not(inlist):      # If in article list section, don't copy out lines (replace)
        newhtmlpage.write(htmlline)
        if '<!-- list:' in htmlline:
          inlist = True
          pub = htmlline.split(':')[1].replace(' -->','').strip()
          print 'Populating links for '+pub
          newhtmlpage.write('<p>\n')
          try:
            for article in articles[pub]:
              newhtmlpage.write(article+'\n')
          except:
            print 'No articles in scan directory for '+pub+'.'
            print
          newhtmlpage.write('</p>\n')
      if '<!-- /list -->' in htmlline: #end of previouslist found.
        inlist = False
        newhtmlpage.write(htmlline)
        # Write this line
    newhtmlpage.close()
    htmlpage.close()


def SyncArticles(host, username, password):
  # Log in to server
  f=ftplib.FTP(host, username, password)
  
  #For pdfs, not concerned with timestamp, only existence
  #Get list of remote articles
  f.cwd('scans')
  dirlist = f.nlst('.')
  remotefiles = []
  #Get list of filenames, filter out all but .pdf files
  for name in dirlist:
    if '.pdf' in name:
      remotefiles.append(name)
  
  #Get list of local files
  os.chdir('scans')
  localfiles = glob.glob('*.pdf')
      
  #Bring down all articles on server not on local
  getfiles = set(remotefiles).difference(localfiles)
  for filename in getfiles:
    print "Getting %s from server."%filename
    fd = open(filename, 'wb')
    f.retrbinary('RETR '+filename, fd.write)
    fd.close()
  
  #Send up all articles on local not on server
  putfiles = set(localfiles).difference(remotefiles)
  for filename in putfiles:
    print "Putting %s to server."%filename
    fd = open(filename, 'rb')
    f.storbinary('STOR '+filename, fd)
    fd.close()
  f.quit()
  os.chdir('..') #Leave in parent directory
  

def GetHTMLfiles(host, username, password):
  def writeline(data):
    fd.write(data + "\n")
    
  # Log in to server
  f=ftplib.FTP(host, username, password)
  #Get list of remote web pages
  dirlist = f.nlst('.')
  filelist = []
  #Get list of filenames, filter out all but .pdf files
  for name in dirlist:
    if '.htm' in name:
      print 'Get ' + name
      fd = open(name, "wt")
      f.retrlines("RETR "+name, writeline)
      fd.close()
  f.quit()

def PutHTMLfiles(host, username, password):
  #Assume in parent directory
  # Log in to server
  f=ftplib.FTP(host, username, password)
  localfiles = glob.glob('*.htm')
  for name in localfiles:
    print 'Put '+name
    fd = open(name, 'r')
    f.storlines('STOR '+name, fd)
  f.close()
        
def main():
  #Username and Password for Michael's FTP account
  host = "ftp.spencersmithlab.org"
  username = "mgiltz@spencersmithlab.org"
  password = "wsh1awnnyer"

  #Filter local directory (look out for repeat names)
  FilterLocalDirectory()
  
  #Filter remote web directory
  FilterRemoteDirectory(host, username, password)

  #Call routine to sync current directory with web directory
  #Note: Must be changed if host changes, duh.
  SyncArticles(host, username, password)
  GetHTMLfiles(host, username, password)

  #Read all file names in scans directory, make dictionary of article links
  articles = MakeArticleDict()
  
  #Read current files, replace links sections
  UpdatePages(articles)

  #Call routine again to sync current directory with web directory
  PutHTMLfiles(host, username, password)
  
  raw_input('Press ENTER key to end... ')
  
if __name__ == '__main__': main()

