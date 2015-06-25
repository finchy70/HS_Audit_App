# -*- coding: utf_8 -*

__author__ = 'Paul Finch'



import wx
import sqlite3
import datetime as dt
from itertools import chain


def get_columns(state):
    global my_list_col
    global my_list_id
    my_list_col = ""
    my_list_id = ""
    con = sqlite3.connect("hs_audit.sqlite")
    con.text_factory = str
    cur = con.cursor()
    cur.execute("SELECT rowid FROM T1 WHERE active =?", (state))
    my_list_id = [lists[0] for lists in cur.fetchall()]
    con.close()
    con = sqlite3.connect("hs_audit.sqlite")
    con.text_factory = str
    cur = con.cursor()
    cur.execute("SELECT engineer FROM T1 WHERE active =?", (state))
    my_list_col = [lists[0] for lists in cur.fetchall()]
    con.close()



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
        frame = SetUpFrame(500, 300, "Manage Current Colleagues", ManageColleaguePanel)

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
        btn3 = wx.Button(self, label="View Leavers", size=(420, 60))
        btn3.Bind(wx.EVT_BUTTON, self.leaver_colleague)
        btn4 = wx.Button(self, label="Back To Main Menu", size=(420, 60))
        btn4.Bind(wx.EVT_BUTTON, self.main_menu)
        main_sizer.AddStretchSpacer()
        main_sizer.Add(btn1, 0, wx.CENTER)
        main_sizer.Add(btn2, 0, wx.CENTER)
        main_sizer.Add(btn3, 0, wx.CENTER)
        main_sizer.Add(btn4, 0, wx.CENTER)
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
        frame = SetUpFrame(600, 600, "Manage Existing Colleague", ManageExistingColleaguePanel)

    def leaver_colleague(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(600, 600, "View Leavers", LeaverColleaguePanel)

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
        cur = con.execute('SELECT max(rowid) FROM T2')
        global audit_id
        max_audit_id = cur.fetchone()[0]
        if max_audit_id == "NoneType":
            max_audit_id = 1

        cur = con.execute('SELECT max(audit_ver) FROM T3')
        global max_audit_ver
        max_audit_ver = cur.fetchone()[0]
        con.close()
        audit_ver = max_audit_ver
        audit_id = max_audit_id
        audit_date = dt.datetime.today().strftime("%d/%m/%Y")
        ####Database####
        con = sqlite3.connect("hs_audit.sqlite")
        con.execute('INSERT INTO T2 VALUES (?,?,?,?,?)',
                    (audit_engineer, audit_date, audit_site, audit_job_number, audit_ver))
        con.commit()
        con.close()
        ####Kill Frame####
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(600, 500, "Van Audit", VanAuditAnswersPanel)

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
        frame = SetUpFrame(480, 450, "Manage Colleagues", ManageColleaguePanel)

    def save_engineer_details(self, event):
        new_engineer = self.engineer_name.GetValue()
        new_email = self.engineer_email.GetValue()
        new_role = self.engineer_role.GetValue()
        con = sqlite3.connect("hs_audit.sqlite")
        con.execute('INSERT INTO T1 VALUES (?,?,?,?)', (new_engineer, new_email, new_role, 1))
        con.commit()
        con.close()
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(500, 300, "H&S Audit App", FrontMenuPanel)


class ManageExistingColleaguePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer1 = wx.BoxSizer(wx.VERTICAL)
        main_sizer2 = wx.BoxSizer(wx.VERTICAL)
        top_sizer.AddStretchSpacer()
        top_sizer.Add(main_sizer1)
        top_sizer.Add(main_sizer2)
        top_sizer.AddStretchSpacer()
        get_columns("1")
        main_sizer1.AddStretchSpacer()
        main_sizer2.AddStretchSpacer()

        if len(my_list_id) == 1:
            main_sizer1.Add(wx.Button(self, label=str(my_list_col[0]), id=int(my_list_id[(0)]), size=(200, 40)), 2, wx.CENTER)
            self.Bind(wx.EVT_BUTTON, self.detect_on_button)

        elif len(my_list_id) % 2 == 1:
            for n in range(0, len(my_list_col)-1, 2):
                main_sizer1.Add(wx.Button(self, label=str(my_list_col[n]), id=int(my_list_id[(n)]), size=(200, 40)), 2, wx.CENTER)
                self.Bind(wx.EVT_BUTTON, self.detect_on_button)
                main_sizer2.Add(wx.Button(self, label=str(my_list_col[n+1]), id=int(my_list_id[(n+1)]), size=(200, 40)), 2, wx.CENTER)
                self.Bind(wx.EVT_BUTTON, self.detect_on_button)
            main_sizer1.Add(wx.Button(self, label=str(my_list_col[(len(my_list_id)-1)]), id=int(my_list_id[(n+2)]), size=(200, 40)), 2, wx.CENTER)
            self.Bind(wx.EVT_BUTTON, self.detect_on_button)

        else:
            for n in range(0, len(my_list_id)-1, 2):
                main_sizer1.Add(wx.Button(self, label=str(my_list_col[n]), id=int(my_list_id[(n)]), size=(200, 40)), 2, wx.CENTER)
                self.Bind(wx.EVT_BUTTON, self.detect_on_button)
                main_sizer2.Add(wx.Button(self, label=str(my_list_col[n+1]), id=int(my_list_id[(n+1)]), size=(200, 40)), 2, wx.CENTER)
                self.Bind(wx.EVT_BUTTON, self.detect_on_button)

        main_sizer1.AddStretchSpacer()
        main_sizer2.AddStretchSpacer()
        self.SetSizer(top_sizer)
        self.back_button = wx.Button(self, label="Back", id=999, pos=(400, 500))
        self.back_button.Bind(wx.EVT_BUTTON, self.detect_on_button)

    def detect_on_button(self, event):
        #event.Skip()
        global colleague_row_id
        colleague_row_id = event.GetId()
        frame = self.GetParent()  # This assigns parent frame to frame.
        if colleague_row_id == 999:
            frame = self.GetParent()  # This assigns parent frame to frame.
            frame.Close()  # This then closes frame removing the main menu.
            frame = SetUpFrame(480, 450, "Manage Colleagues", ManageColleaguePanel)

        else:
            frame = self.GetParent()  # This assigns parent frame to frame.
            frame.Close()  # This then closes frame removing the main menu.
            frame = SetUpFrame(440, 600, "Edit Colleague", EditColleaguePanel)


class EditColleaguePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        con = sqlite3.connect("hs_audit.sqlite")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT * FROM T1 WHERE rowid='%s'" % (colleague_row_id))
        myList = [[str(item) for item in results] for results in cur.fetchall()]
        con.close()
        ####The following lines extract the nested list from the list
        final_list = []
        while myList:
            final_list.extend(myList.pop(0))

        role_list = ["Management", "Electrician", "Trainee", "Fitter", "Labourer", "Sub Contractor"]
        active_list = ["1", "0"]
        self.text = wx.StaticText(self, label="Employees Name :", pos=(20, 60))
        self.engineer_name = wx.TextCtrl(self, pos=(150, 60), size=(250,-1), value = final_list[0])
        self.text = wx.StaticText(self, label="e-Mail Address :", pos=(20, 120))
        self.engineer_email = wx.TextCtrl(self, pos=(150, 120), value = final_list[1], size=(250,-1))
        self.text = wx.StaticText(self, label="Role :", pos=(20, 180))
        self.engineer_role = wx.ComboBox(self, pos=(230, 180), size=(170, -1), choices=role_list, value=final_list[2])
        self.text = wx.StaticText(self, label="Current Employee (1=Yes 2=No):", pos=(20, 240))
        self.active_eng = wx.ComboBox(self, pos=(350, 240), size=(50, -1), choices=active_list, value=final_list[3])
        self.back_button = wx.Button(self, label="Back", pos=(220, 500))
        self.back_button.Bind(wx.EVT_BUTTON, self.cancel_new_colleague)
        self.save_button = wx.Button(self, label="Save", pos=(320, 500))
        self.save_button.Bind(wx.EVT_BUTTON, self.save_engineer_details)
        self.Show()

    def cancel_new_colleague(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(600, 600, "Manage Existing Colleague", ManageExistingColleaguePanel)

    def save_engineer_details(self, event):
        new_engineer = self.engineer_name.GetValue()
        new_email = self.engineer_email.GetValue()
        new_role = self.engineer_role.GetValue()
        new_active = self.active_eng.GetValue()
        con = sqlite3.connect("hs_audit.sqlite")
        con.execute("UPDATE T1 SET engineer='%s', email='%s', role='%s', active='%s' WHERE rowid='%s'" % (new_engineer, new_email, new_role, new_active, colleague_row_id))
        con.commit()
        con.close()
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(500, 300, "Manage Current Colleagues", ManageColleaguePanel)


class LeaverColleaguePanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        top_sizer = wx.BoxSizer(wx.HORIZONTAL)
        main_sizer1 = wx.BoxSizer(wx.VERTICAL)
        main_sizer2 = wx.BoxSizer(wx.VERTICAL)
        top_sizer.AddStretchSpacer()
        top_sizer.Add(main_sizer1)
        top_sizer.Add(main_sizer2)
        top_sizer.AddStretchSpacer()
        get_columns("0")
        main_sizer1.AddStretchSpacer()
        main_sizer2.AddStretchSpacer()

        if len(my_list_id) == 1:
            main_sizer1.Add(wx.Button(self, label=str(my_list_col[0]), id=int(my_list_id[(0)]), size=(200, 40)), 2, wx.CENTER)
            self.Bind(wx.EVT_BUTTON, self.detect_on_button)

        elif len(my_list_id) % 2 == 1:
            for n in range(0, len(my_list_col)-1, 2):
                main_sizer1.Add(wx.Button(self, label=str(my_list_col[n]), id=int(my_list_id[(n)]), size=(200, 40)), 2, wx.CENTER)
                self.Bind(wx.EVT_BUTTON, self.detect_on_button)
                main_sizer2.Add(wx.Button(self, label=str(my_list_col[n+1]), id=int(my_list_id[(n+1)]), size=(200, 40)), 2, wx.CENTER)
                self.Bind(wx.EVT_BUTTON, self.detect_on_button)
            main_sizer1.Add(wx.Button(self, label=str(my_list_col[(len(my_list_id)-1)]), id=int(my_list_id[(n+2)]), size=(200, 40)), 2, wx.CENTER)
            self.Bind(wx.EVT_BUTTON, self.detect_on_button)

        else:
            for n in range(0, len(my_list_id)-1, 2):
                main_sizer1.Add(wx.Button(self, label=str(my_list_col[n]), id=int(my_list_id[(n)]), size=(200, 40)), 2, wx.CENTER)
                self.Bind(wx.EVT_BUTTON, self.detect_on_button)
                main_sizer2.Add(wx.Button(self, label=str(my_list_col[n+1]), id=int(my_list_id[(n+1)]), size=(200, 40)), 2, wx.CENTER)
                self.Bind(wx.EVT_BUTTON, self.detect_on_button)

        main_sizer1.AddStretchSpacer()
        main_sizer2.AddStretchSpacer()
        self.SetSizer(top_sizer)
        self.back_button = wx.Button(self, label="Back", id=999, pos=(400, 500))
        self.back_button.Bind(wx.EVT_BUTTON, self.detect_on_button)

    def detect_on_button(self, event):
        #event.Skip()
        global colleague_row_id
        colleague_row_id = event.GetId()
        frame = self.GetParent()  # This assigns parent frame to frame.
        if colleague_row_id == 999:
            frame = self.GetParent()  # This assigns parent frame to frame.
            frame.Close()  # This then closes frame removing the main menu.
            frame = SetUpFrame(480, 450, "Manage Colleagues", ManageColleaguePanel)

        else:
            frame = self.GetParent()  # This assigns parent frame to frame.
            frame.Close()  # This then closes frame removing the main menu.
            frame = SetUpFrame(440, 600, "Edit Colleague", EditColleaguePanel)


class ReactivateLeaverPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        con = sqlite3.connect("hs_audit.sqlite")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT * FROM T1 WHERE rowid='%s'" % (leaver_colleague_id))
        myList = [[str(item) for item in results] for results in cur.fetchall()]
        con.close()
        final_list = []
        while myList:
            final_list.extend(myList.pop(0))

        active_list = ["1", "0"]
        self.text = wx.StaticText(self, label="Employees Name :    %s" % (final_list[0]), pos=(20, 60))
        self.text = wx.StaticText(self, label="e-Mail Address :    %s" % (final_list[1]), pos=(20, 120))
        self.text = wx.StaticText(self, label="Role :              %s" % (final_list[2]), pos=(20, 180))
        self.text = wx.StaticText(self, label="Current Employee (1=Yes 0=No):", pos=(20, 240))
        self.active_eng = wx.ComboBox(self, pos=(350, 240), size=(50, -1), choices=active_list, value=final_list[3])
        self.back_button = wx.Button(self, label="Back", pos=(220, 500))
        self.back_button.Bind(wx.EVT_BUTTON, self.cancel_new_colleague)
        self.save_button = wx.Button(self, label="Save", pos=(320, 500))
        self.save_button.Bind(wx.EVT_BUTTON, self.save_engineer_details)
        self.Show()

    def cancel_new_colleague(self, event):
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(500, 450, "Manage Colleagues", ManageColleaguePanel)

    def save_engineer_details(self, event):
        new_active = self.active_eng.GetValue()
        con = sqlite3.connect("hs_audit.sqlite")
        con.execute("UPDATE T1 SET active='%s' WHERE rowid='%s'" % (new_active, leaver_colleague_id))
        con.commit()
        con.close()
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(500, 300, "Manage Current Colleagues", ManageColleaguePanel)

#############################################################################
#                            Question Panels                                #
#############################################################################

class VanAuditAnswersPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        global question
        question = 0
        sizerControl = wx.GridBagSizer(hgap=4,vgap = 4)
        rboxPick = ["Yes", "No", "N/A", "Not answered yet"]
        con = sqlite3.connect("hs_audit.sqlite")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT vaq1, vaq2, vaq3, vaq4 FROM T3 WHERE audit_ver =1")#, (change 1 to max_audit_id))
        result = [[str(item) for item in results] for results in cur.fetchall()]
        con.close()
        global aa
        aa ={}
        global labels
        labels = []
        while result:
            labels.extend(result.pop(0))

        #Create, layout and bind the RadioBoxes
        for row, label in enumerate(labels):
            question += 1
            lbl = wx.StaticText(self)
            rbox = wx.RadioBox(self, id=question, label="Q%r - %s" % (question, label), choices=rboxPick)
            rbox.SetSelection(3)
            self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, rbox)
            sizerControl.Add(rbox, pos=(row+1, 1), span=(1,5),
                             flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=2)
        self.save_button = wx.Button(self, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.save_answers)
        sizerControl.Add(self.save_button, pos=(question+3, 5),
                         flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=2)
        #Show()
        sizerMain = wx.BoxSizer()
        sizerMain.Add(sizerControl)
        self.SetSizerAndFit(sizerMain)



    def onRadioBox(self, event):
        """Event handler for RadioBox.."""
        rbox = event.GetEventObject()
        rboxLbl = rbox.GetLabel()
        answer = rbox.GetSelection()
        question = rbox.GetId()
        print rbox
        print "rbox label = %s" % (rboxLbl)
        print "Selection = %s" % (question)
        print "Answer = %r" % (answer)
        aa[question] = answer
        print aa

    def save_answers(self, event):
        global running_question_total
        running_question_total = 0
        print running_question_total
        print question
        if len(aa) < (running_question_total + question): #Have all questions been answered
            return

        else:
            global full_audit_answers
            full_audit_answers = {}
            running_question_total += question
            for f in range ((running_question_total) - question, running_question_total):
                print "f=%s" % (f)
                full_audit_answers[f+1] = aa[f+1]
            frame = self.GetParent()  # This assigns parent frame to frame.
            frame.Close()  # This then closes frame removing the main menu.
            frame = SetUpFrame(600, 650, "Method Statement and RAMS.", RamsAuditAnswersPanel)


class RamsAuditAnswersPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        question = 0
        sizerControl = wx.GridBagSizer(hgap=4,vgap = 4)
        rboxPick = ["Yes", "No", "N/A", "Not answered yet"]
        con = sqlite3.connect("hs_audit.sqlite")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT rq1, rq2, rq3, rq4, rq5, rq6, rq7 FROM T3 WHERE audit_ver = 1")#, (change 1 to max_audit_id))
        result = [[str(item) for item in results] for results in cur.fetchall()]
        con.close()
        aa ={}
        global labels
        labels = []
        while result:
            labels.extend(result.pop(0))

        #Create, layout and bind the RadioBoxes
        for row, label in enumerate(labels):
            question += 1
            lbl = wx.StaticText(self)
            rbox = wx.RadioBox(self, id=question, label="Q%r - %s" % (question, label), choices=rboxPick)
            rbox.SetSelection(3)
            self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, rbox)
            sizerControl.Add(rbox, pos=(row+1, 1), span=(1,5),
                             flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=2)

        self.save_button = wx.Button(self, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.save_answers)
        sizerControl.Add(self.save_button, pos=(question+3, 5),
                         flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=2)
        #Show()
        sizerMain = wx.BoxSizer()
        sizerMain.Add(sizerControl)
        self.SetSizerAndFit(sizerMain)



    def onRadioBox(self, event):
        """Event handler for RadioBox.."""
        rbox = event.GetEventObject()
        rboxLbl = rbox.GetLabel()
        answer = rbox.GetSelection()
        question = rbox.GetId()
        aa[question+running_question_total] = answer
        print aa

    def save_answers(self, event):
        global running_question_total
        print "The running total = %s" % (running_question_total+question)
        print "Questions so far = %s" % (question)
        print "Range check is (%s, %s)." % ((running_question_total) - question, running_question_total)
        if len(aa) < (running_question_total + question): #Have all questions been answered
            return

        else:
            running_question_total += question
            for f in range ((running_question_total) - question, running_question_total):
                print "f=%s" % (f)
                full_audit_answers[f+1] = aa[f+1]
                print full_audit_answers
            frame = self.GetParent()  # This assigns parent frame to frame.
            frame.Close()  # This then closes frame removing the main menu.
            frame = SetUpFrame(600, 500, "PPE Audit.", PpeAuditAnswersPanel)


class PpeAuditAnswersPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        question = 0
        sizerControl = wx.GridBagSizer(hgap=4,vgap = 4)
        rboxPick = ["Yes", "No", "N/A", "Not answered yet"]
        con = sqlite3.connect("hs_audit.sqlite")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT ppeq1, ppeq2, ppeq3, ppeq4 FROM T3 WHERE audit_ver = 1")#, (change 1 to max_audit_id))
        result = [[str(item) for item in results] for results in cur.fetchall()]
        con.close()
        aa ={}
        global labels
        labels = []
        while result:
            labels.extend(result.pop(0))

        #Create, layout and bind the RadioBoxes
        question = 0
        for row, label in enumerate(labels):
            question += 1
            lbl = wx.StaticText(self)
            rbox = wx.RadioBox(self, id=question, label="Q%r - %s" % (question, label), choices=rboxPick)
            rbox.SetSelection(3)
            self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, rbox)
            sizerControl.Add(rbox, pos=(row+1, 1), span=(1,5),
                             flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=2)

        self.save_button = wx.Button(self, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.save_answers)
        sizerControl.Add(self.save_button, pos=(question+3, 5),
                         flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=2)
        #Show()
        sizerMain = wx.BoxSizer()
        sizerMain.Add(sizerControl)
        self.SetSizerAndFit(sizerMain)



    def onRadioBox(self, event):
        """Event handler for RadioBox.."""
        rbox = event.GetEventObject()
        rboxLbl = rbox.GetLabel()
        answer = rbox.GetSelection()
        question = rbox.GetId()
        print rbox
        print "rbox label = %s" % (rboxLbl)
        print "Selection = %s" % (question)
        print "Answer = %r" % (answer)
        aa[question + running_question_total] = answer
        print aa

    def save_answers(self, event):
        global running_question_total
        print running_question_total
        print "The running total = %s" % (running_question_total+question)
        print "Questions so far = %s" % (question)
        print "Range check is (%s, %s)." % ((running_question_total) - question, running_question_total)
        if len(aa) < (running_question_total + question): #Have all questions been answered
            return

        else:
            running_question_total += question
            for f in range ((running_question_total) - question, running_question_total):
                print "f=%s" % (f)
                full_audit_answers[f+1] = aa[f+1]
                print full_audit_answers
            frame = self.GetParent()  # This assigns parent frame to frame.
            frame.Close()  # This then closes frame removing the main menu.
            frame = SetUpFrame(800, 500, "Tool Audit.", ToolsAuditAnswersPanel)


class ToolsAuditAnswersPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        question = 0
        sizerControl = wx.GridBagSizer(hgap=4,vgap = 4)
        rboxPick = ["Yes", "No", "N/A", "Not answered yet"]
        con = sqlite3.connect("hs_audit.sqlite")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT tq1, tq2, tq3, tq4, tq5 FROM T3 WHERE audit_ver = 1")#, (change 1 to max_audit_id))
        result = [[str(item) for item in results] for results in cur.fetchall()]
        con.close()
        aa ={}
        global labels
        labels = []
        while result:
            labels.extend(result.pop(0))

        #Create, layout and bind the RadioBoxes
        for row, label in enumerate(labels):
            question += 1
            lbl = wx.StaticText(self)
            rbox = wx.RadioBox(self, id=question, label="Q%r - %s" % (question, label), choices=rboxPick)
            rbox.SetSelection(3)
            self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, rbox)
            sizerControl.Add(rbox, pos=(row+1, 1), span=(1,5),
                             flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=2)

        self.save_button = wx.Button(self, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.save_answers)
        sizerControl.Add(self.save_button, pos=(question+2, 5),
                         flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=2)
        #Show()
        sizerMain = wx.BoxSizer()
        sizerMain.Add(sizerControl)
        self.SetSizerAndFit(sizerMain)



    def onRadioBox(self, event):
        """Event handler for RadioBox.."""
        rbox = event.GetEventObject()
        rboxLbl = rbox.GetLabel()
        answer = rbox.GetSelection()
        question = rbox.GetId()
        print rbox
        print "rbox label = %s" % (rboxLbl)
        print "Selection = %s" % (question)
        print "Answer = %r" % (answer)
        aa[question+running_question_total] = answer
        print aa

    def save_answers(self, event):
        global running_question_total

        print "The running total = %s" % (running_question_total+question)
        print "Questions so far = %s" % (question)
        print "Range check is (%s, %s)." % ((running_question_total) - question, running_question_total)
        if len(aa) < (running_question_total + question): #Have all questions been answered
            return

        else:
            running_question_total += question
            for f in range ((running_question_total) - question, running_question_total):
                print "f=%s" % (f)
                full_audit_answers[f+1] = aa[f+1]
                print full_audit_answers
            frame = self.GetParent()  # This assigns parent frame to frame.
            frame.Close()  # This then closes frame removing the main menu.
            frame = SetUpFrame(800, 500, "HV works and Documentation.", HvAuditAnswersPanel)


class HvAuditAnswersPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        question = 0
        sizerControl = wx.GridBagSizer(hgap=4,vgap = 4)
        rboxPick = ["Yes", "No", "N/A", "Not answered yet"]
        con = sqlite3.connect("hs_audit.sqlite")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT hvq1, hvq2, hvq3, hvq4, hvq5 FROM T3 WHERE audit_ver = 1")#, (change 1 to max_audit_id))
        result = [[str(item) for item in results] for results in cur.fetchall()]
        con.close()
        aa ={}
        global labels
        labels = []
        while result:
            labels.extend(result.pop(0))

        #Create, layout and bind the RadioBoxes
        for row, label in enumerate(labels):
            question += 1
            lbl = wx.StaticText(self)
            rbox = wx.RadioBox(self, id=question, label="Q%r - %s" % (question, label), choices=rboxPick)
            rbox.SetSelection(3)
            self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, rbox)
            sizerControl.Add(rbox, pos=(row+1, 1), span=(1,5),
                             flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=2)

        self.save_button = wx.Button(self, label="Save")
        self.save_button.Bind(wx.EVT_BUTTON, self.save_answers)
        sizerControl.Add(self.save_button, pos=(question+3, 5),
                         flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=2)
        #Show()
        sizerMain = wx.BoxSizer()
        sizerMain.Add(sizerControl)
        self.SetSizerAndFit(sizerMain)



    def onRadioBox(self, event):
        """Event handler for RadioBox.."""
        rbox = event.GetEventObject()
        rboxLbl = rbox.GetLabel()
        answer = rbox.GetSelection()
        question = rbox.GetId()
        print rbox
        print "rbox label = %s" % (rboxLbl)
        print "Selection = %s" % (question)
        print "Answer = %r" % (answer)
        aa[question+running_question_total] = answer
        print aa

    def save_answers(self, event):
        global running_question_total
        print "The running total = %s" % (running_question_total+question)
        print "Questions so far = %s" % (question)
        print "Range check is (%s, %s)." % ((running_question_total) - question, running_question_total)
        if len(aa) < (running_question_total + question): #Have all questions been answered
            return

        else:
            running_question_total += question
            for f in range ((running_question_total) - question, running_question_total):
                print "f=%s" % (f)
                full_audit_answers[f+1] = aa[f+1]
                print full_audit_answers
            frame = self.GetParent()  # This assigns parent frame to frame.
            frame.Close()  # This then closes frame removing the main menu.
            frame = SetUpFrame(600, 500, "Method Statement and RAMS.", exit(0))
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

