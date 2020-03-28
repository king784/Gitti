import wx
import os.path
from os import path
from subprocess import *
import threading 
import time

class Window(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        self.path = ""
        file1 = open(os.path.dirname(os.path.abspath(__file__)) + "\LastPath.txt","r")
        self.path = file1.readline()
        file1.close() 
        self.commitMsg = ""
        self.panel = wx.Panel(self)
        self.tc = wx.TextCtrl(self.panel, value=self.path)
        self.InitUI()
        self.SetSize((400, 200))
        self.SetTitle('Gitti')
        self.Center()

    def InitUI(self):        
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        fileItem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit Application')
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)
        
        self.Bind(wx.EVT_MENU, self.OnQuit, fileItem)

        font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        font.SetPointSize(12)

        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        vbox.AddStretchSpacer()
        st1 = wx.StaticText(self.panel, label='Path to project folder: ')
        st1.SetFont(font)
        hbox1.Add(st1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=8)
        hbox2.Add(self.tc, flag=wx.EXPAND|wx.LEFT|wx.RIGHT, border=8 ,proportion=1)
        btn1 = wx.Button(self.panel, wx.ID_OPEN)
        self.Bind(wx.EVT_BUTTON, self.SelectFolder, id=btn1.GetId())
        btn2 = wx.Button(self.panel, wx.ID_OK, "Commit")
        self.Bind(wx.EVT_BUTTON, self.ShowMessage, id=btn2.GetId())
        hbox3.Add(btn1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=8)
        hbox3.Add(btn2, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP|wx.BOTTOM, border=8)
        vbox.Add(hbox1)
        vbox.Add(hbox2)
        vbox.Add(hbox3)
        vbox.AddStretchSpacer()
        vbox.SetItemMinSize(hbox2, 400, 20)
        

        self.SetSizer(vbox)
        

    def OnQuit(self, e):
        self.Close()

    def ShowToast(self):
        textDialog = wx.Dialog(None, wx.ID_DEFAULT, "Success")
        textDialog.ShowModal()

    def Commit(self):
        self.path = self.path.replace('\r', '').replace('\n', '')
        self.commitMsg = self.commitMsg.replace('\r', '').replace('\n', '')
        p = Popen([os.path.dirname(os.path.abspath(__file__)) + '\Automerge.bat', self.path, self.commitMsg], cwd=self.path, shell= True, stdout=PIPE, stderr=PIPE)
        output, errors = p.communicate()
        p.wait() # wait for process to terminate
        print(output)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnQuit, self.timer)
        self.timer.Start(2000)
        self.ShowToast()

    def ShowError(self, errorMsg):
        wx.MessageBox(errorMsg, 'ERROR',
            wx.OK | wx.ICON_ERROR)

    def SelectFolder(self, e):
        dirDialog = wx.DirDialog (None, "Choose directory", "",
                    wx.DD_DEFAULT_STYLE | wx.DD_DIR_MUST_EXIST)
        if dirDialog.ShowModal() == wx.ID_OK:
            if not path.exists(dirDialog.GetPath() + '\.git'):
                self.ShowError("Not a git directory!!")
            
            self.path = dirDialog.GetPath()
            print(self.path)
            self.tc.Clear()
            self.tc.SetValue(dirDialog.GetPath())
            file1 = open(os.path.dirname(os.path.abspath(__file__)) + "\LastPath.txt","w")
            file1.write(self.path)
            file1.close() 

        dirDialog.Destroy()
        self.panel.Layout()

    def ShowMessage(self, e):
        textDialog = wx.TextEntryDialog(None, "Enter commit message", "Commit Message")
        if textDialog.ShowModal() == wx.ID_OK:
            self.commitMsg = textDialog.GetValue()
            self.Commit()


def main():
    app = wx.App()
    frame = Window(None)
    frame.Show()
    app.MainLoop()

if __name__ == '__main__':
    main()
