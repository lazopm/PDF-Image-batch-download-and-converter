import cookielib 
import urllib2 
import mechanize 
import csv
import os
from wand.image import Image

LOGIN_URL="http://example.com"
FILES_URL="http://example.com/img/"
#Csv list of file names
FILE_LIST="filename.csv"

#Output format
OUTPUT_FORMAT="jpeg"
OUTPUT_EXTENSION=".jpg"

#Login details (leave as none if not needed)
LOGIN=None
PASSWORD=None
#This are the field names, if they are not named you have
#to change the code below to select them using numbers like for the form
LOGIN_FIELD=None
PASSWORD_FIELD=None
#Login form number, usually 0 if it's the only/first of the page
FORM=0

# Make Browser 
br = mechanize.Browser() 

# Enable cookies
cookiejar = cookielib.LWPCookieJar() 
br.set_cookiejar( cookiejar ) 

# Browser options 
br.set_handle_equiv( True )
br.set_handle_redirect( True ) 
br.set_handle_referer( True ) 
br.set_handle_robots( False ) 
br.set_handle_refresh( mechanize._http.HTTPRefreshProcessor(), max_time = 1 ) 
br.addheaders = [ ( 'User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1' ) ] 

#Authenticate if credentials are set
if(LOGIN!=None and PASSWORD!=None):
    br.open( LOGIN_URL ) 
    br.select_form(nr=FORM)
    br[ LOGIN_FIELD ] = LOGIN
    br[ PASSWORD_FIELD ] = PASSWORD
    br.submit() 

with open(FILE_LIST, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
    for row in reader:
        #Check if the file was already downloaded in case the script closed prematurely
        t = os.path.isfile('pdf/'+row[0]+'.pdf')
        if t == False:
            try:
                #Try to download the file
                br.retrieve(FILES_URL+row[0]+'.pdf','pdf/'+row[0]+'.pdf')
                #Convert to desired image format
                with Image(filename='pdf/'+row[0]+'.pdf') as img:
                    img.format = OUTPUT_FORMAT
                    img.save(filename= OUTPUT_FORMAT+'/'+row[0]+OUTPUT_EXTENSION)
                print(row[0]+' OK!')
            except:
                pass
        
