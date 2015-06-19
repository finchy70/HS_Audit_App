__author__ = 'Paul Finch'

#This piece of code sets up a frame to display the simple front menu
import wx
import sqlite3
import datetime as dt

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
        frame = self.GetParent() #This assigns parent frame to frame.
        frame.Close() #This then closes frame removing the main menu.
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
        frame = self.GetParent() #This assigns parent frame to frame.
        frame.Destroy() #This then closes frame removing the main menu and terminates app.
        exit('Good Bye')


#This creates the panel for the Create New Audit Menu
class CreateAudit(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.engineer = ""
        self.lblname = wx.StaticText(self, label = "Site Name :", pos=(20,60))
        self.site_name = wx.TextCtrl(self, pos=(170, 60), size=(170,-1))
        self.lblname = wx.StaticText(self, label = "Job Number (4 digits only)", pos=(20,120))
        self.job_number = wx.TextCtrl(self, pos=(170, 120), size=(170,-1))
        con = sqlite3.connect("hs_audit.sqlite")
        con.row_factory = lambda cursor, row: row[0]
        myList = con.execute('SELECT engineer FROM T1').fetchall()
        con.close()
        self.lblname = wx.StaticText(self, label="Select Engineer :", pos=(20,180))
        self.engineer_name = wx.ComboBox(self, pos=(170, 180), size=(170,-1)).SetItems(myList)
        self.save_button = wx.Button(self, label="Save", pos=(150, 400))
        self.save_button.Bind(wx.EVT_BUTTON, self.save_audit_details)
        self.Show()

    def save_audit_details(self, event):
        audit_jobnumber = self.job_number.GetValue()
        audit_site = self.site_name
        #audit_engineer = self.engineer_name.GetCurrentString()
        con = sqlite3.connect("hs_audit.sqlite")
        cur = con.execute('SELECT max(audit_id) FROM T2')
        max_audit_id = cur.fetchone()[0]
        cur = con.execute('SELECT max(audit_ver) FROM T3')
        max_audit_ver = cur.fetchone()[0]
        con.close()
        audit_ver = max_audit_ver
        audit_id = max_audit_id + 1
        audit_date = dt.datetime.today().strftime("%d/%m/%Y")
        print "The Audit ID is %r and the date is %s." % (audit_id, audit_date)
        print "The job number is EPS-%s-15 and the site is %s." % (audit_jobnumber, audit_site)
        print "The version of the audit is version %r." %(audit_ver)
        #print "The engineer is %s" % (audit_engineer)




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

def onClose(self, event):
   frame = self.GetParent()
   frame.Close()

#This kicks everything off by calling frame and starting the apps loop.
if __name__ == '__main__':
    app = wx.App(False)
    frame = FrontFrame()
    app.MainLoop()