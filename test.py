__author__ = 'Paul'
class FrontMenuFrame(wx.Frame):
	def __init__(self, parent=None):  # Pass frame height, width, name, and panel.
		#wx.Frame.__init__(self, None, title="EPS - Health and Safety Audit.", size=(500, 300))
		super(FrontMenuFrame, self).__init__(parent, title="EPS - Health and Safety Audit.", size=(500, 300))
		self.SetBackgroundColour("default")
		self.InitUI()
		self.Centre()
		self.Show()

	def InitUI(self):
		panel = wx.Panel(self, 0)
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
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = SetUpFrame(400, 500, "Create New Audit", CreateAuditPanel)

	def manage_colleagues(self, event):
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = SetUpFrame(500, 300, "Manage Current Colleagues", ManageColleaguePanel)

	def view_audit(self, event):
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = SetUpFrame(500, 700, "View Previous Audit - Select Colleague", PreviousAuditPanel)

	def close_app(self, event):
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()
		exit('Good Bye')