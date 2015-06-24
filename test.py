class ReactivateLeaverPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        colleague_row = int(colleague_row_id)
        con = sqlite3.connect("hs_audit.sqlite")
        con.text_factory = str
        cur = con.cursor()
        print colleague_row
        cur.execute("SELECT * FROM T1 WHERE rowid='%s'" % (colleague_row_id))
        myList = [[str(item) for item in results] for results in cur.fetchall()]
        con.close()
        final_list = []
        while myList:
            final_list.extend(myList.pop(0))


        active_list = ["1", "0"]
        self.text = wx.StaticText(self, label="Employees Name :    $s" % (final_list(0)), pos=(20, 60))
        self.text = wx.StaticText(self, label="e-Mail Address :    %s" % (final_list(1)), pos=(20, 120))
        self.text = wx.StaticText(self, label="Role :              %s" % (final_list(2)), pos=(20, 180))
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
        frame = SetUpFrame(500, 450, "Manage Colleagues", ManageColleaguePanel)

    def save_engineer_details(self, event):
        new_engineer = self.engineer_name.GetValue()
        new_email = self.engineer_email.GetValue()
        new_role = self.engineer_role.GetValue()
        new_active = self.active_eng.GetValue()
        con = sqlite3.connect("hs_audit.sqlite")
        con.execute("UPDATE T1 SET active='%s' WHERE rowid='%s'" % (new_active, colleague_row_id))
        con.commit()
        con.close()
        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(500, 300, "Manage Current Colleagues", ManageColleaguePanel)



