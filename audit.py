__author__ = 'Paul Finch'

#This piece of code sets up a frame to display the simple front menu
import wx
import sqlite3

#This is the front main menu panel
class FrontPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        btn1 = wx.Button(self, label='Create New Audit', size=(420, 60))
        btn1.Bind(wx.EVT_BUTTON, self.create_audit)
        btn2 = wx.Button(self, label="Add New Colleague", size=(420, 60))
        btn2.Bind(wx.EVT_BUTTON, self.create_engineer)
        btn3 = wx.Button(self, label="View Previous Audit", size=(420, 60))
        btn3.Bind(wx.EVT_BUTTON, self.view_audit)
        btn4 = wx.Button(self, label="Close", size=(420, 60))
        btn4.Bind(wx.EVT_BUTTON, self.close_app)
        main_sizer.AddStretchSpacer()
        main_sizer.Add(btn1, 0, wx.CENTER)
        main_sizer.Add(btn2, 0, wx.CENTER)
        main_sizer.Add(btn3, 0, wx.CENTER)
        main_sizer.Add(btn4, 0, wx.CENTER)
        main_sizer.AddStretchSpacer()
        self.SetSizer(main_sizer)

        # This opens the Create New Audit frame.
    def create_audit(self, event):
        print 'create audit'
        self.Close(True)
        frame = FrontAudit()
        app.MainLoop()

        # To be completed
    def create_engineer(self, event):
        option = 2
        print "Create engineer"
        exit()

    # To be completed
    def view_audit(self, event):
        option = 3
        print "View Audit"
        exit()

    # To be completed
    def close_app(self, event):
        option = 4
        exit('Good Bye')


#This creates the panel for the Create New Audit Menu
class CreateAudit(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.lblname = wx.StaticText(self, label="Site Name :", pos=(20,60))
        self.sitename = wx.TextCtrl(self, value="Enter site name here.", pos=(150, 60), size=(140,-1))
        self.lblname = wx.StaticText(self, label="4 Digit Job Number", pos=(20,120))
        self.jobnumber = wx.TextCtrl(self, pos=(150, 120), size=(140,-1))

        con = sqlite3.connect("hs_audit.sqlite")
        cur = con.cursor()
        con.row_factory = lambda cursor, row: row[0]
        ids = con.execute('SELECT engineer FROM T1').fetchall()
        myList = ids
        self.lblname = wx.StaticText(self, label="Select Engineer :", pos=(20,180))
        self.engineername = wx.ComboBox(self, pos=(150, 180), size=(140,-1)).SetItems(myList)

        self.button =wx.Button(self, label="Save", pos=(150, 400))
        self.Show()

#This creates the frame for the Main Menu
class FrontFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title='H&S Audit App', size = (500, 350))
        panel = FrontPanel(self)

        self.Centre()
        self.Show()

#This creates the frame for the Create New Audit Menu.
class FrontAudit(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title='Create New Audit', size = (400, 500))
        panel = CreateAudit(self)

        self.Centre()
        self.Show()

"""
This section will manage all the questions via the sqlite3 database

class Questions(object):

    def read_questions(self):
        pass


class VanAudit(Questions):

    def read_questions(self):
        pass


class RamsAudit(Questions):

    def read_questions(self):
        pass


class PpeAudit(Questions):

    def read_questions(self):
        pass


class ToolAudit(Questions):

    def read_questions(self):
        pass


class HvAudit(Questions):

    def read_questions(self):
        pass
"""
#This kicks everything off.
if __name__ == '__main__':
    app = wx.App(False)
    frame = FrontFrame()
    app.MainLoop()