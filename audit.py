__author__ = 'Paul Finch'

import wx

import wx

########################################################################
class FrontPanel(wx.Panel):
	""""""

	#----------------------------------------------------------------------
	def __init__(self, parent):
		"""Constructor"""
		wx.Panel.__init__(self, parent)
		main_sizer = wx.BoxSizer(wx.VERTICAL)
		btn1 = wx.Button(self, id=-1, label='Create New Audit', size=(420, 60))
		btn2 = wx.Button(self, label="Add New Colleague", size=(420, 60))
		btn3 = wx.Button(self, label="View Previous Audit", size=(420, 60))
		btn4 = wx.Button(self, label="Close", size=(420, 60))
		main_sizer.AddStretchSpacer()
		main_sizer.Add(btn1, 0, wx.CENTER)
		main_sizer.Add(btn2, 0, wx.CENTER)
		main_sizer.Add(btn3, 0, wx.CENTER)
		main_sizer.Add(btn4, 0, wx.CENTER)
		main_sizer.AddStretchSpacer()

		self.SetSizer(main_sizer)


########################################################################
class FrontFrame(wx.Frame):
	""""""

	#----------------------------------------------------------------------
	def __init__(self):
		"""Constructor"""
		wx.Frame.__init__(self, None, title='H&S Audit App', size = (500, 350))
		panel = FrontPanel(self)

		self.Show()

if __name__ == '__main__':
	app = wx.App(False)
	frame = FrontFrame()
	app.MainLoop()