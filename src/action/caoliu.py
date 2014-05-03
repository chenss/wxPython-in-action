"""
Created on 2014-5-1

@author: chen
"""

import os
import re
import time
import urllib2
import shutil
import wx
from bs4 import BeautifulSoup

class Frame(wx.Frame):

    def __init__(self):
        wx.Frame.__init__(self, None, -1, "CaoLiu Spider", size=(500, 300))
        self.panel = wx.Panel(self, -1)
        self.button = wx.Button(self.panel, -1, "Download", pos=(350, 10))
        self.Bind(wx.EVT_BUTTON, self.BookSpider, self.button)
        wx.StaticText(self.panel, -1, "URL:", pos=(10, 20))
        self.posCtrl = wx.TextCtrl(self.panel, -1, "", pos=(40, 10), size=(300,-1))
        wx.StaticText(self.panel, -1, "", pos=(10, 50), size=(500,200))

    def BookSpider(self, event):
        i = 1
        url = self.posCtrl.GetValue()
        name = ""
        TEMP_DIR = os.getcwd() + "/.temp/"
        HOME = os.path.expanduser("~")
        
        if not os.path.exists(TEMP_DIR):
            os.mkdir(TEMP_DIR)
        else:
            for f in os.listdir(TEMP_DIR):
                print f
                os.remove(TEMP_DIR + f)
           
        temp_file = TEMP_DIR + str(time.time())    
        fo = open(temp_file, "a")
    
        while True:
            url2 = url + str(i)
            page = urllib2.urlopen(url2)
            content = page.read()
    
            soup = BeautifulSoup(content, from_encoding="gbk")
    
            if len(soup.h4.text) > 0:   
                    name = soup.h4.text + ".txt"
        
            text = soup.find_all(class_="tpc_content")
            text = str(text).replace("<br/><br/>", "\n\n").replace("<br/>", "")
            #text = str(text).replace("<br/>", "\n\n")
            text = re.sub("<.+>", "", text) 
    
            if len(text) < 100:
                    break
      
            fo.write(text)
            i = i + 1
            print url2
        
        fo.close()

        shutil.move(temp_file, HOME + "/" + name)
        print "done"

class App(wx.App):
    
    def __init__(self, redirect=True, filename=None):
        wx.App.__init__(self, redirect, filename)
    
    def OnInit(self):
        self.frame = Frame()
        self.frame.Show()
        self.SetTopWindow(self.frame)
        return True

def main():
    app = App(redirect=False)
    app.MainLoop()

if __name__ == "__main__":
    main()