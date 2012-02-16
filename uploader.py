import paramiko
import Tkinter as tk
from bs4 import BeautifulSoup
import re

def upload(username, password, host, title, textbox, END):

    #Get all the text in the textbox and save it to currentSaved.html with some slight decoration
    if title is not 'Empty':
        htmlDocument = '<h1>' + title + '</h1>' + textbox.get("1.0", tk.END) + '<a id="blogReturn" class="regular linkPointer">Back to Blog</a>'
    else:
        htmlDocument = textbox.get("1.0", tk.END) + '<a id="blogReturn" class="regular linkPointer">Back to Blog</a>'
    f = open('blog/currentSaved.html', 'w')
    f.write(htmlDocument)
    f.close()
    
    #SFTP setup
    transport = paramiko.Transport((host, 22))
    transport.connect(username = username, password = password)
    sftp = paramiko.SFTPClient.from_transport(transport)
    
    #Get the soon to be outdated remote index and open it in BS
    sftp.get("index.html", "blog/indexOld.html")
    soup = BeautifulSoup(open("blog/indexOld.html", 'r'))
    oldIndex = open("blog/indexOld.html").read()
    
    #Find the latest post number from the old index
    currentPostNumber = re.search("(?<=blogPost)\d+", oldIndex).group(0)
    currentPostNumber = int(currentPostNumber) + 1
    
    #Form and insert the link that will appear on the new index
    markup = '<li id="blogPost' + str(currentPostNumber) + '"><a class="linkPointer">' + title +'</a></li>'
    theList = soup.find("ul", id="postList")
    theList.insert(0, markup)
    
    #Modify the index, this is the final version
    newIndex = soup.prettify()
    index = open("blog/index.html", 'w')
    index.write(newIndex)
    index.close()
    
    #This is the remote path for the blog content
    path = "blog/blogPost" + str(currentPostNumber) + ".html"
    
    #Clear the way and upload the final versions
    sftp.remove("index.html")
    sftp.put("blog/currentSaved.html", path)
    sftp.put("blog/index.html", "index.html")

    #Close connections
    sftp.close()
    transport.close()
    print 'Upload done.'