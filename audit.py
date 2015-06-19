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
        btn1 = wx.Button(self, label = "View Colleague List", size=(420, 60))
        btn1.Bind(wx.EVT_BUTTON, self.view_colleague)
        btn2 = wx.Button(self, label='Create New Audit', size=(420, 60))
        btn2.Bind(wx.EVT_BUTTON, self.create_audit)
        btn3 = wx.Button(self, label="Add New Colleague", size=(420, 60))
        btn3.Bind(wx.EVT_BUTTON, self.create_engineer)
        btn4 = wx.Button(self, label="View Previous Audit", size=(420, 60))
        btn4.Bind(wx.EVT_BUTTON, self.view_audit)
        btn5 = wx.Button(self, label="Close", size=(420, 60))
        btn5.Bind(wx.EVT_BUTTON, self.close_app)

        main_sizer.AddStretchSpacer()
        main_sizer.Add(btn1, 0, wx.CENTER)
        main_sizer.Add(btn2, 0, wx.CENTER)
        main_sizer.Add(btn3, 0, wx.CENTER)
        main_sizer.Add(btn4, 0, wx.CENTER)
        main_sizer.Add(btn5, 0, wx.CENTER)
        main_sizer.AddStretchSpacer()
        self.SetSizer(main_sizer)

        # This opens the Create New Audit frame.
    def create_audit(self, event):
        frame = self.GetParent() #This assigns parent frame to frame.
        frame.Close() #This then closes frame removing the main menu.
        frame = FrontAudit()

        # To be completed
    def create_engineer(self, event):
        frame = self.GetParent() #This assigns parent frame to frame.
        frame.Close() #This then closes frame removing the main menu.
        frame = FrontAddEngineer()

    # To be completed
    def view_audit(self, event):
        option = 3
        print "View Audit"
        exit()

    def view_colleague(self, event):
        frame = self.GetParent() #This assigns parent frame to frame.
        frame.Close() #This then closes frame removing the main menu.
        frame = ViewColleagues()

    # To be completed
    def close_app(self, event):
        frame = self.GetParent() #This assigns parent frame to frame.
        frame.Destroy() #This then closes frame removing the main menu and terminates app.
        exit('Good Bye')

class ViewColleaguesPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        con = sqlite3.connect("hs_audit.sqlite")
        cur = con.execute('SELECT max(rowid) FROM T1')
        max_row_id = cur.fetchone()[0]
        main_sizer = wx.GridSizer(1, 3, 200, 200)
        main_sizer.Add(wx.StaticText(self, label = "Name"),20, wx.ALIGN_TOP | wx.ALIGN_CENTER)
        main_sizer.Add(wx.StaticText(self, label = "eMail"),20, wx.ALIGN_TOP | wx.ALIGN_CENTER)
        main_sizer.Add(wx.StaticText(self, label = "Role"), 20, wx.ALIGN_TOP | wx.ALIGN_CENTER)
        #main_sizer = wx.FlexGridSizer(max_row_id, 3, 5, 5)#
        self.SetSizer(main_sizer)
        self.Show()




#This creates the panel for the Create New Audit Menu
class CreateAudit(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.lblname = wx.StaticText(self, label = "Site Name :", pos=(20,60))
        self.site_name = wx.TextCtrl(self, pos=(170, 60), size=(170,-1))
        self.lblname = wx.StaticText(self, label = "Job Number (4 digits only)", pos=(20,120))
        self.job_number = wx.TextCtrl(self, pos=(170, 120), size=(170,-1))
        con = sqlite3.connect("hs_audit.sqlite")
        con.row_factory = lambda cursor, row: row[0]
        myList = con.execute('SELECT engineer FROM T1').fetchall()
        con.close()
        self.lblname = wx.StaticText(self, label="Select Engineer :", pos=(20,180))
        self.engineer_name = wx.ComboBox(self, pos=(170, 180), size=(170,-1), choices = myList)
        self.save_button = wx.Button(self, label="Save", pos=(150, 400))
        self.save_button.Bind(wx.EVT_BUTTON, self.save_audit_details)
        self.Show()

    def save_audit_details(self, event):
        audit_jobnumber = self.job_number.GetValue()
        audit_site = self.site_name.GetValue()
        audit_engineer = self.engineer_name.GetValue()
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
        print "The engineer is %s" % (audit_engineer)
        con = sqlite3.connect("hs_audit.sqlite")
        con.execute('INSERT INTO T2 VALUES (?,?,?,?,?,?)',
                    (audit_id, audit_engineer, audit_date, audit_site, audit_jobnumber, audit_ver))
        con.commit()
        con.close()
        frame = self.GetParent() #This assigns parent frame to frame.
        frame.Close() #This then closes frame removing the main menu.
        exit()

class CreateEngineerPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        role_list = ["Electrician", "Trainee", "Fitter", "Labourer", "Sub Contractor"]
        self.text = wx.StaticText(self, label = "Employees Name :", pos=(20,60))
        self.engineer_name = wx.TextCtrl(self, pos=(170, 60), size=(170,-1))
        self.text = wx.StaticText(self, label = "e-Mail Address :", pos=(20,120))
        self.engineer_email = wx.TextCtrl(self, pos=(170, 120), size=(170,-1))
        self.text = wx.StaticText(self, label = "Role :", pos=(20,180))
        self.engineer_role = wx.ComboBox(self, pos=(170, 180), size=(170,-1), choices = role_list)
        self.save_button = wx.Button(self, label="Save", pos=(150, 400))
        self.save_button.Bind(wx.EVT_BUTTON, self.save_engineer_details)
        self.Show()

    def save_engineer_details(self, event):

        new_engineer = self.engineer_name.GetValue()
        new_email = self.engineer_email.GetValue()
        new_role = self.engineer_role.GetValue()
        con = sqlite3.connect("hs_audit.sqlite")
        con.execute('INSERT INTO T1 VALUES (?,?,?)',
                    (new_engineer, new_email,new_role))
        con.commit()
        con.close()
        frame = FrontFrame()






#This creates the frame for the Main Menu
class FrontFrame(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title='H&S Audit App', size = (500, 350))
        panel = FrontPanel(self)
        con = sqlite3.connect("hs_audit.sqlite")
        con.row_factory = lambda cursor, row: row[0]
        myList = con.execute('SELECT engineer FROM T1').fetchall()
        con.close()
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

class FrontAddEngineer(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title='Create New Employee', size = (400, 500))
        panel = CreateEngineerPanel(self)

        self.Centre()
        self.Show()

class ViewColleagues(wx.Frame):
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="View Collegues.", size = (1000, 1000))
        panel = ViewColleaguesPanel(self)
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