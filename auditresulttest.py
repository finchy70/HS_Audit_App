import wx
import sqlite3

audit_id = 2




class AuditResultPanel(wx.Panel):
	def __init__(self, parent, audit_id):
		wx.Panel.__init__(self, parent)
		con = sqlite3.connect("hs_audit.sqlite")
		con.text_factory = str
		cur = con.cursor()
		cur.execute("SELECT * FROM T2 WHERE audit_id =?", str(audit_id))
		result = cur.fetchall()
		con.close()
		print "Result is %s" % (result)
		variables_list = []
		while result:
			variables_list.extend(result.pop(0))
		print variables_list
		del variables_list[-1]
		print variables_list
		the_list = ['enigineer_id', 'audit_date', 'audit_site', 'job_number', 'audit_ver']
		audit_engineer = variables_list[0]
		audit_date = variables_list[1]
		audit_site = variables_list[2]
		job_number = variables_list[3]
		audit_ver = variables_list[4]
		print audit_engineer
		self.sizerControl = wx.GridBagSizer(hgap=0, vgap=1)
		font1 = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
		font2 = wx.Font(12, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
		self.text = wx.StaticText(self, label="Employee :- ", style=wx.TEXT_ALIGNMENT_RIGHT)
		self.text.SetFont(font1)
		self.sizerControl.Add(self.text, pos=(1, 2))
		self.text = wx.StaticText(self, label=audit_engineer, style=wx.ALIGN_RIGHT)
		self.text.SetFont(font1)
		self.sizerControl.Add(self.text, pos=(1, 3))
		self.text = wx.StaticText(self, label="Site :- ", style=wx.ALIGN_RIGHT)
		self.text.SetFont(font1)
		self.sizerControl.Add(self.text, pos=(2, 2))
		self.text = wx.StaticText(self, label=audit_site, style=wx.ALIGN_RIGHT)
		self.text.SetFont(font1)
		self.sizerControl.Add(self.text, pos=(2, 3))
		self.text = wx.StaticText(self, label="Audit Date:- ", style=wx.ALIGN_RIGHT)
		self.text.SetFont(font1)
		self.sizerControl.Add(self.text, pos=(3, 2))
		self.text = wx.StaticText(self, label=audit_date, style=wx.ALIGN_RIGHT)
		self.text.SetFont(font1)
		self.sizerControl.Add(self.text, pos=(3, 3))
		con = sqlite3.connect("hs_audit.sqlite")
		con.text_factory = str
		cur = con.cursor()
		cur.execute("SELECT * FROM T3 WHERE audit_ver = '%s'" % (audit_ver))
		questions_result = [[str(item) for item in results] for results in cur.fetchall()]
		con.close()
		final_questions = []
		while questions_result:
			final_questions.extend(questions_result.pop(0))
		con = sqlite3.connect("hs_audit.sqlite")
		cur = con.cursor()
		cur.execute("SELECT * FROM T4 WHERE audit_id = '%s'" % (audit_id))
		answer_result = cur.fetchall()
		con.close()
		final_answers = []
		while answer_result:
			final_answers.extend(answer_result.pop(0))
		del final_questions[-1]
		del final_answers[-1]
		correct = 0
		wrong = 0
		not_app = 0
		for q in range(1 , len(final_questions)):
			self.text = wx.StaticText(self, label=final_questions[q], style=wx.TEXT_ALIGNMENT_RIGHT)
			self.sizerControl.Add(self.text, pos=(q+3, 2), span=(1,6), flag=wx.EXPAND)
			if final_answers[q] == 0:
				self.text = wx.StaticText(self, label="Yes", style=wx.TEXT_ALIGNMENT_RIGHT)
				self.sizerControl.Add(self.text, pos=(q+3, 8), flag=wx.EXPAND)
				correct += 1

			elif final_answers[q] == 1:
				self.text = wx.StaticText(self, label="No", style=wx.TEXT_ALIGNMENT_RIGHT)
				self.sizerControl.Add(self.text, pos=(q+3, 8), flag=wx.EXPAND)
				wrong += 1

			else:
				self.text = wx.StaticText(self, label="N/A", style=wx.TEXT_ALIGNMENT_RIGHT)
				self.sizerControl.Add(self.text, pos=(q+3, 8), flag=wx.EXPAND)
				not_app += 1

		applic = wrong + correct
		percent_correct = 100 * (float(correct) / float(applic))
		self.text = wx.StaticText(self, label="Applicable Questions = ", style=wx.TEXT_ALIGNMENT_RIGHT)
		self.text.SetFont(font2)
		self.sizerControl.Add(self.text, pos=(30, 2))
		self.text = wx.StaticText(self, label=str(applic), style=wx.ALIGN_RIGHT)
		self.text.SetFont(font2)
		self.sizerControl.Add(self.text, pos=(30, 3))
		self.text = wx.StaticText(self, label="Audit Percentage        = ", style=wx.TEXT_ALIGNMENT_RIGHT)
		self.text.SetFont(font2)
		self.sizerControl.Add(self.text, pos=(31, 2))
		self.text = wx.StaticText(self, label=str(percent_correct), style=wx.ALIGN_RIGHT)
		self.text.SetFont(font2)
		self.sizerControl.Add(self.text, pos=(31, 3))
		self.SetSizer(self.sizerControl)
		self.Show()


###################################
#####       Frame Setup       #####
###################################

# This creates the frame for the all menus.
class SetUpFrame(wx.Frame):
	def __init__(self, fwide, fhigh, ftitle, Panel):  # Pass frame height, width, name, and panel.
		wx.Frame.__init__(self, None, title=ftitle, size=(fwide, fhigh))
		panel = Panel(self, audit_id)
		self.Centre()
		self.Show()

# This kicks everything off by calling frame and starting the app loop.
if __name__ == '__main__':
	app = wx.App(False)
	frame = SetUpFrame(700, 700, "Audit Result", AuditResultPanel)
	app.MainLoop()
