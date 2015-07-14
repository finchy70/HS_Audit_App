import wx

def YesNo(question, caption = 'Yes or no?'):
	dlg = wx.MessageDialog(question, caption, wx.YES_NO | wx.ICON_QUESTION)
	result = dlg.ShowModal() == wx.ID_YES
	dlg.Destroy()
	return result

YesNo("Site or Colleague Audit?", "Site or Colleague")