import sys
from uploader import upload
import Tkinter as tk

#Example format: editor.py user_joe p4ssw0rd sftp.mysite.com , Port is assumed to be 22
username = sys.argv[1]
password = sys.argv[2]
host = sys.argv[3]

class Application(object):
    def __init__(self, master):
        self.FRAME = tk.Frame()
        self.FRAME.pack()
        self.createWidgets()
    
    htmlDocument = "Empty"
    documentTitle = "Empty"
    
    def createWidgets(self):
        
        self.QUIT = tk.Button(self.FRAME)
        self.QUIT["text"] = "Quit"
        self.QUIT["fg"] = "red"
        self.QUIT["command"] = self.QUIT.quit
        self.QUIT.pack({"side": "left"})
        
        self.PUBLISH = tk.Button(self.FRAME)
        self.PUBLISH["text"] = "Publish"
        self.PUBLISH["command"] = lambda: upload(username, password, host, self.documentTitle, self.TEXT, tk.END)
        self.PUBLISH.pack({"side": "left"})
        
        self.TEXT = tk.Text(self.FRAME)
        self.TEXT.pack()
        
        self.SETTITLE = tk.Button(self.FRAME)
        self.SETTITLE["text"] = "Set Title"
        self.SETTITLE["command"] = lambda: self.setTitle()
        self.SETTITLE.pack({"side": "left"})
               
    def setTitle(self):
        class Prompt(Application):
            def __init__(self, master):
                self.promptFrame = tk.Toplevel()
                self.createWidg()
                
            def createWidg(self):
                self.titleEntry = tk.Entry(self.promptFrame)
                self.titleEntry.focus_set()
                self.titleEntry.pack()
                
                self.titleSend = tk.Button(self.promptFrame)
                self.titleSend["text"] = "Set"
                self.titleSend["command"] = lambda: self.getEntry()
                self.titleSend.pack()
                
                self.titleBack = tk.Button(self.promptFrame)
                self.titleBack["text"] = "Back"
                self.titleBack["command"] = self.promptFrame.destroy
                self.titleBack.pack()
            
            def getEntry(self):
                if self.titleEntry.get() == '' or self.titleEntry.get() == 'Title can not be empty!':
                    self.titleEntry.delete(0, tk.END)
                    self.titleEntry.insert(0, "Title can not be empty!")
                else:
                    Application.documentTitle = self.titleEntry.get()
                    self.promptFrame.destroy()
        
        prom = Prompt(self)
        
root = tk.Tk()
app = Application(root)
root.mainloop()        
