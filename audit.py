# -*- coding: utf_8 -*

__author__ = 'Paul Finch'

import wx
import sqlite3
import datetime as dt




##########Panel Set Ups###########
# This is the front main menu panel
class FrontMenuPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        btn1 = wx.Button(self, label='Create New Audit', size=(420, 60))
        btn1.Bind(wx.EVT_BUTTON, self.create_audit)
        btn2 = wx.Button(self, label="Manage Colleagues", size=(420, 60))
        btn2.Bind(wx.EVT_BUTTON, self.manage_colleagues)
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

    def create_audit(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(400, 500, "Create New Audit", CreateAuditPanel)

    def manage_colleagues(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(500, 300, "Manage Colleagues", ManageColleaguePanel)

    def view_audit(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(1000, 1000, "View Previous Audit", PreviousAuditPanel)

    def close_app(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Destroy()  # This then closes frame removing the main menu and terminates app.
        exit('Good Bye')


class ManageColleaguePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        btn1 = wx.Button(self, label="Add New Colleague", size=(420, 60))
        btn1.Bind(wx.EVT_BUTTON, self.add_new_colleague)
        btn2 = wx.Button(self, label="Edit Existing Colleagues", size=(420, 60))
        btn2.Bind(wx.EVT_BUTTON, self.existing_colleague)
        btn3 = wx.Button(self, label="Back To Main Menu", size=(420, 60))
        btn3.Bind(wx.EVT_BUTTON, self.main_menu)

        main_sizer.AddStretchSpacer()
        main_sizer.Add(btn1, 0, wx.CENTER)
        main_sizer.Add(btn2, 0, wx.CENTER)
        main_sizer.Add(btn3, 0, wx.CENTER)
        main_sizer.AddStretchSpacer()
        self.SetSizer(main_sizer)

    def add_new_colleague(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(400, 500, "Add New Colleague", AddNewColleaguePanel)

        # To be completed

    def existing_colleague(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(300, 700, "Manage Existing Colleague", ManageExistingColleaguePanel)

    # To be completed
    def main_menu(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(500, 300, "H&S Audit App", FrontMenuPanel)


# This creates the panel for the Create New Audit Menu
class CreateAuditPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        self.lblname = wx.StaticText(self, label="Site Name :", pos=(20, 60))
        self.site_name = wx.TextCtrl(self, pos=(170, 60), size=(170, -1))
        self.lblname = wx.StaticText(self, label="Job Number (4 digits only)", pos=(20, 120))
        self.job_number = wx.TextCtrl(self, pos=(170, 120), size=(170, -1))
        con = sqlite3.connect("hs_audit.sqlite")
        con.row_factory = lambda cursor, row: row[0]
        myList = con.execute("SELECT engineer FROM T1 WHERE active = 1").fetchall()
        con.close()
        self.lblname = wx.StaticText(self, label="Select Engineer :", pos=(20, 180))
        self.engineer_name = wx.ComboBox(self, pos=(170, 180), size=(170, -1), choices=myList)
        self.save_button = wx.Button(self, label="Save", pos=(250, 400))
        self.save_button.Bind(wx.EVT_BUTTON, self.save_audit_details)
        self.cancel_button = wx.Button(self, label="Cancel", pos=(150, 400))
        self.cancel_button.Bind(wx.EVT_BUTTON, self.cancel_audit_details)

    def save_audit_details(self, event):
        audit_job_number = self.job_number.GetValue()
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
        ####Database####
        con = sqlite3.connect("hs_audit.sqlite")
        con.execute('INSERT INTO T2 VALUES (?,?,?,?,?,?)',
                    (audit_id, audit_engineer, audit_date, audit_site, audit_job_number, audit_ver))
        con.commit()
        con.close()
        ####Kill Frame####
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        exit()

    def cancel_audit_details(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(500, 300, "H&S Audit App", FrontMenuPanel)


class PreviousAuditPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        exit(0)


# Creates Panel for adding a new colleague.
class AddNewColleaguePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        role_list = ["Management", "Electrician", "Trainee", "Fitter", "Labourer", "Sub Contractor"]
        self.text = wx.StaticText(self, label="Employees Name :", pos=(20, 60))
        self.engineer_name = wx.TextCtrl(self, pos=(170, 60), size=(170, -1))
        self.text = wx.StaticText(self, label="e-Mail Address :", pos=(20, 120))
        self.engineer_email = wx.TextCtrl(self, pos=(170, 120), size=(170, -1))
        self.text = wx.StaticText(self, label="Role :", pos=(20, 180))
        self.engineer_role = wx.ComboBox(self, pos=(170, 180), size=(170, -1), choices=role_list)
        self.back_button = wx.Button(self, label="Back", pos=(150, 400))
        self.back_button.Bind(wx.EVT_BUTTON, self.cancel_new_colleague)
        self.save_button = wx.Button(self, label="Save", pos=(250, 400))
        self.save_button.Bind(wx.EVT_BUTTON, self.save_engineer_details)
        # self.Show()

    def cancel_new_colleague(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(500, 350, "Manage Colleagues", ManageColleaguePanel)

    def save_engineer_details(self, event):
        new_engineer = self.engineer_name.GetValue()
        new_email = self.engineer_email.GetValue()
        new_role = self.engineer_role.GetValue()
        con = sqlite3.connect("hs_audit.sqlite")
        con.execute('INSERT INTO T1 VALUES (?,?,?,?)', (new_engineer, new_email, new_role, 1))
        con.commit()
        con.close()
        frame = SetUpFrame(500, 300, "H&S Audit App", FrontMenuPanel)


class ManageExistingColleaguePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        con = sqlite3.connect("hs_audit.sqlite")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT engineer FROM T1")
        myList = [r[0] for r in cur.fetchall()]
        con.close()
        main_sizer.AddStretchSpacer()
        for n in range(0, len(myList)):
            main_sizer.Add(wx.Button(self, label=str(myList[(n)]), id=n, size=(200, 25)), 0, wx.CENTER)
            self.Bind(wx.EVT_BUTTON, self.detect_on_button)
            main_sizer.AddStretchSpacer()
        self.SetSizer(main_sizer)

    def detect_on_button(self, event):
        #event.Skip()
        colleague_id = event.GetId()
        colleague_row_id = colleague_id + 1
        print colleague_row_id


# topSizer.Add(wx.StaticLine(self.panel), 0, wx.ALL|wx.EXPAND, 5)

###########Frame Setups############

# This creates the frame for the all menus.
class SetUpFrame(wx.Frame):
    def __init__(self, fwide, fhigh, ftitle, Panel):  # Pass frame height, width, name, and panel.
        wx.Frame.__init__(self, None, title=ftitle, size=(fwide, fhigh))
        panel = Panel(self)
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


# This kicks everything off by calling frame and starting the app loop.
if __name__ == '__main__':
    app = wx.App(False)
    frame = SetUpFrame(500, 300, "H&S Audit App", FrontMenuPanel)
    app.MainLoop()
