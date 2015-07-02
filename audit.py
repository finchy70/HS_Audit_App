# -*- coding: utf-8 -*-
__author__ = 'Paul Finch'

import wx
import sqlite3
import datetime as dt
from sqlalchemy.sql import select
from sqlalchemy import create_engine

global aa
global labels
global running_total
global full_audit_answers


# This function gets a list of current or ex employees from db. State 2=all, 1=cur, and 0=leavers.
def get_all_questions():
	con = sqlite3.connect("hs_audit.sqlite")
	con.text_factory = str
	cur = con.cursor()
	cur.execute("SELECT max(audit_ver) FROM T3")
	temp_id = cur.fetchall()
	max_audit_version = temp_id[0]
	con.close()
	con = sqlite3.connect("hs_audit.sqlite")
	con.text_factory = str
	cur = con.cursor()
	cur.execute("SELECT * FROM T3 WHERE audit_ver = '%s'" % (max_audit_version))
	result = cur.fetchall()
	all_audit_questions = []
	while result:
		all_audit_questions.extend(result.pop(0))
	print "Complete Return = %s" % (all_audit_questions)
	del all_audit_questions[-1]
	print "All questions = %s" % (all_audit_questions)
	print type(all_audit_questions)
	return all_audit_questions


def get_columns(state):
	global my_list_col
	global my_list_id
	my_list_col = ""
	my_list_id = ""
	con = sqlite3.connect("hs_audit.sqlite")
	con.text_factory = str
	cur = con.cursor()

	if state == "2":
		cur.execute("SELECT rowid FROM T1")

	else:
		cur.execute("SELECT rowid FROM T1 WHERE active =?", (state))

	my_list_id = [lists[0] for lists in cur.fetchall()]
	con.close()
	con = sqlite3.connect("hs_audit.sqlite")
	con.text_factory = str
	cur = con.cursor()

	if state == "2":
		cur.execute("SELECT engineer FROM T1")

	else:
		cur.execute("SELECT engineer FROM T1 WHERE active =?", (state))

	my_list_col = [lists[0] for lists in cur.fetchall()]
	con.close()
	print my_list_col

################################################
###Functions to display various message boxes###
################################################
def YesNo(parent, question, caption = 'Yes or no?'):
	dlg = wx.MessageDialog(parent, question, caption, wx.YES_NO | wx.ICON_QUESTION)
	result = dlg.ShowModal() == wx.ID_YES
	dlg.Destroy()
	return result

def Info(parent, message, caption = 'Insert program title'):
	dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_INFORMATION)
	dlg.ShowModal()
	dlg.Destroy()

def Warn(parent, message, caption = 'Warning!'):
	dlg = wx.MessageDialog(parent, message, caption, wx.OK | wx.ICON_WARNING)
	dlg.ShowModal()
	dlg.Destroy()

#Function that converts nested lists into one list.
def traverse(o, tree_types=(list, tuple)):
	if isinstance(o, tree_types):
		for value in o:
			for subvalue in traverse(value):
				yield subvalue
	else:
		yield o

##################################
##########Frame Setups############
##################################

# This is the front main menu panel
class FrontMenuFrame(wx.Frame):
	def __init__(self, parent=None):  # Pass frame height, width, name, and panel.
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
		frame = CreateAuditFrame()

	def manage_colleagues(self, event):
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = ManageColleagueFrame()

	def view_audit(self, event):
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = SetUpFrame(500, 700, "View Previous Audit - Select Colleague", PreviousAuditPanel)

	def close_app(self, event):
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()
		exit('Good Bye')




class ManageColleagueFrame(wx.Frame):
	def __init__(self, parent=None):  # Pass frame height, width, name, and panel.
		#wx.Frame.__init__(self, None, title="EPS - Health and Safety Audit.", size=(500, 300))
		super(ManageColleagueFrame, self).__init__(parent, title="EPS - Manage Colleagues.", size=(500, 300))
		self.SetBackgroundColour("default")
		self.InitUI()
		self.Centre()
		self.Show()

	def InitUI(self):
		panel = wx.Panel(self)
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
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = CreateNewColleagueFrame()

	def existing_colleague(self, event):
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = ManageColleagueFrame("existing")

	def leaver_colleague(self, event):
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = ManageColleagueFrame("leavers")

	def main_menu(self, event):
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = FrontMenuFrame()


# This creates the panel for the Create New Audit Menu
class CreateAuditFrame(wx.Frame):

	def __init__(self, parent=None):  # Pass frame height, width, name, and panel.
		#wx.Frame.__init__(self, None, title="EPS - Health and Safety Audit.", size=(500, 300))
		super(CreateAuditFrame, self).__init__(parent, title="EPS - Create New Audit.", size=(410, 500))
		self.SetBackgroundColour("default")
		self.InitUI()
		self.Centre()
		self.Show()

	def InitUI(self):
		panel = wx.Panel(self, 0)
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
		global audit_id
		audit_id = 0 #This will contain the unique audit ID.
		global audit_job_number #This will hold the EPS Job Number.
		audit_job_number = self.job_number.GetValue()
		global audit_site
		audit_site = self.site_name.GetValue() #Holds the site name.
		global audit_engineer
		audit_engineer = self.engineer_name.GetValue() # Hold the engineers name.
		#Connect to db and retrieve the last audit-id
		con = sqlite3.connect("hs_audit.sqlite")
		cur = con.execute('SELECT max(audit_id) FROM T2')
		audit_number = cur.fetchone()[0]
		print type(audit_number)
		if audit_number < 1: #This checks if this is the first audit and gives it the id 1 if it is.
			audit_id = 1
		else:
			audit_id = audit_number + 1 #This takes the audit_id of the last audit and adds 1 to allocate the new audit_id
		#Connect to db and retrieve the current audit version.
		cur = con.execute('SELECT max(audit_ver) FROM T3')
		global audit_ver
		max_audit_ver = cur.fetchone()[0]
		con.close()
		audit_ver = max_audit_ver
		####Kill Frame####
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = CreateQuestionsFrame("Van Audit", 0)

	#Function to close frame on button event and return to main menu.
	def cancel_audit_details(self, event):
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = FrontMenuFrame()


#This is the panel that displays all employees so previous audits can be viewed.
class PreviousAuditPanel(wx.Panel):
		def __init__(self, parent = None):
			wx.Panel.__init__(self, parent)
			# Set up panel to display previous audits.
			top_sizer = wx.BoxSizer(wx.HORIZONTAL)
			main_sizer1 = wx.BoxSizer(wx.VERTICAL)
			main_sizer2 = wx.BoxSizer(wx.VERTICAL)
			top_sizer.AddStretchSpacer()
			top_sizer.Add(main_sizer1)
			top_sizer.Add(main_sizer2)
			top_sizer.AddStretchSpacer()
			get_columns("2")
			main_sizer1.AddStretchSpacer()
			main_sizer2.AddStretchSpacer()

			#This section checks if the list has a single, odd amount , or even amount of employees to display
			#and plans the layout accordingly.
			if len(my_list_id) == 1:
				main_sizer1.Add(wx.Button(self, label=str(my_list_col[0]), id=int(my_list_id[(0)]), size=(200, 40)), 2,
								wx.CENTER)
				self.Bind(wx.EVT_BUTTON, self.detect_on_button)

			# The for loop adds the row_ids from table 1 to each button to identify the engineer.
			elif len(my_list_id) % 2 == 1:
				for n in range(0, len(my_list_col) - 1, 2):
					main_sizer1.Add(wx.Button(self, label=str(my_list_col[n]), id=int(my_list_id[(n)]), size=(200, 40)), 2,
									wx.CENTER)
					self.Bind(wx.EVT_BUTTON, self.detect_on_button)
					main_sizer2.Add(
						wx.Button(self, label=str(my_list_col[n + 1]), id=int(my_list_id[(n + 1)]), size=(200, 40)), 2,
						wx.CENTER)
					self.Bind(wx.EVT_BUTTON, self.detect_on_button)
				main_sizer1.Add(wx.Button(self, label=str(my_list_col[(len(my_list_id) - 1)]), id=int(my_list_id[(n + 2)]),
										  size=(200, 40)), 2, wx.CENTER)
				self.Bind(wx.EVT_BUTTON, self.detect_on_button)

			else:
				for n in range(0, len(my_list_id) - 1, 2):
					main_sizer1.Add(wx.Button(self, label=str(my_list_col[n]), id=int(my_list_id[(n)]), size=(200, 40)), 2,
									wx.CENTER)
					self.Bind(wx.EVT_BUTTON, self.detect_on_button)
					main_sizer2.Add(
						wx.Button(self, label=str(my_list_col[n + 1]), id=int(my_list_id[(n + 1)]), size=(200, 40)), 2,
						wx.CENTER)
					self.Bind(wx.EVT_BUTTON, self.detect_on_button)

			main_sizer1.AddStretchSpacer()
			main_sizer2.AddStretchSpacer()
			self.SetSizer(top_sizer)
			self.back_button = wx.Button(self, label="Back", id=999, pos=(350, 500))
			self.back_button.Bind(wx.EVT_BUTTON, self.detect_on_button)

		def detect_on_button(self, event):
			global colleague_row_id
			colleague_row_id = event.GetId() #Colleague id from button event set by loop in layout above.

			if colleague_row_id == 999:
				frame = self.GetParent()  # This assigns parent frame to frame.
				frame.Close()  # This then closes frame removing the main menu.
				frame = SetUpFrame(500, 300, "H&S Audit App", FrontMenuPanel)

			else:
				frame = self.GetParent()  # This assigns parent frame to frame.
				frame.Close()  # This then closes frame removing the main menu.
				#Get the engineers name from the row_id(button id).
				con = sqlite3.connect("hs_audit.sqlite")
				con.text_factory = str
				cur = con.cursor()
				cur.execute("SELECT engineer FROM T1 WHERE rowid='%s'" % (colleague_row_id))
				audit_colleague_name = cur.fetchall()
				final_colleague_name = audit_colleague_name[0]
				con.close()
				#Get a list of the audit_id's for the engineer.
				con = sqlite3.connect("hs_audit.sqlite")
				con.text_factory = str
				cur = con.cursor()
				cur.execute("SELECT audit_id FROM T2 WHERE engineer='%s'" % (final_colleague_name))
				my_audits = [[str(item) for item in results] for results in cur.fetchall()]
				con.close()
				print "The amount of audits found =%s" % (len(my_audits))
				if len(my_audits) < 1:# Check there is a history of audits.
					Warn(self, "No Audit History!!")# Display warning box if there are no historical audits.
					frame = SetUpFrame(500, 700, "View Previous Audit - Select Colleague", PreviousAuditPanel)
				else:
					# Send engineer name to frame that displays audit history.  ID's in global my_audits list.
					frame = SelectAuditFrame(final_colleague_name)


class SelectAuditPanel(wx.Panel):
	def __init__(self, parent, colleage_name):
		self.colleague_name = colleage_name
		wx.Panel.__init__(self, parent)
		font1 = wx.Font(15, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD)
		main_sizer = wx.BoxSizer(wx.VERTICAL)
		second_sizer = wx.BoxSizer(wx.VERTICAL)
		self.text = wx.StaticText(self, label = "Engineer :-      %s" % (self.colleague_name), pos=(0,0))
		self.text.SetFont(font1)
		main_sizer.Add(self.text, 0, wx.CENTER)
		con = sqlite3.connect("hs_audit.sqlite")
		con.text_factory = str
		cur = con.cursor()
		cur.execute("SELECT job_no, site, date, audit_id  FROM T2 WHERE engineer = '%s'" % (self.colleague_name))
		audit_return = cur.fetchall()
		con.close()
		print audit_return
		final_data = list(traverse(audit_return)) #Convert nested lists into one long list.
		print "Final data %s" % (final_data)
		second_sizer.AddStretchSpacer()
		for f in range(0, len(final_data)-1, 4):
			#Create a button and label it for each previous audit.
			btn = wx.Button(self, label='Job Number :- %s.     Site :- %s.     Date :- %s.' % (final_data[f], final_data[f+1], final_data[f+2]), id = final_data[f+3], size=(500, 30))
			btn.Bind(wx.EVT_BUTTON, self.on_button)
			second_sizer.Add(btn, 0, wx.TEXT_ALIGNMENT_LEFT)
		second_sizer.AddStretchSpacer()
		main_sizer.Add(second_sizer, 0, wx.CENTER)
		self.SetSizer(main_sizer)

	def on_button(self, event):
		audit_id_call = event.GetId()# Capture id of audit to be displayed.
		frame = self.GetParent()  # This assigns parent frame to frame.
		frame.Close()  # This then closes frame removing the main menu.
		frame = SetUpAuditFrame(audit_id_call)


# Creates Panel for adding a new colleague.
class CreateNewColleagueFrame(wx.Frame):
	def __init__(self, parent=None):
		super(CreateNewColleagueFrame, self).__init__(parent, title="EPS - Create New Colleague.", size=(300, 500))
		self.SetBackgroundColour("default")
		self.InitUI()
		self.Centre()
		self.Show()
	def InitUI(self):
		panel = wx.Panel(self, 0)
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

	def cancel_new_colleague(self, event):
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = ManageColleagueFrame()

	def save_engineer_details(self, event):
		new_engineer = self.engineer_name.GetValue()
		new_email = self.engineer_email.GetValue()
		new_role = self.engineer_role.GetValue()
		con = sqlite3.connect("hs_audit.sqlite")
		con.execute('INSERT INTO T1 VALUES (?,?,?,?)', (new_engineer, new_email, new_role, 1))
		con.commit()
		con.close()
		self.GetParent()  # This assigns parent frame to frame.
		self.Close()  # This then closes frame removing the main menu.
		frame = FrontMenuFrame()


class DisplayColleagueFrame(wx.Frame):
	def __init__(self, parent, state):
		wx.Panel.__init__(self, parent)
		top_sizer = wx.BoxSizer(wx.HORIZONTAL)
		main_sizer1 = wx.BoxSizer(wx.VERTICAL)
		main_sizer2 = wx.BoxSizer(wx.VERTICAL)
		top_sizer.AddStretchSpacer()
		top_sizer.Add(main_sizer1)
		top_sizer.Add(main_sizer2)
		top_sizer.AddStretchSpacer()
		if state == "existing":
			get_columns("1")# Get amount of existing colleagues by passing "1" to get columns.

		else:
			get_columns("2")

		main_sizer1.AddStretchSpacer()
		main_sizer2.AddStretchSpacer()

		# This section checks if the list of existing colleagues has a single, odd amount , or even
		# amount of employees to display and plans the layout accordingly.
		if len(my_list_id) == 1:
			main_sizer1.Add(wx.Button(self, label=str(my_list_col[0]), id=int(my_list_id[(0)]), size=(200, 40)), 2,
							wx.CENTER)
			self.Bind(wx.EVT_BUTTON, self.detect_on_button)

		elif len(my_list_id) % 2 == 1:
			for n in range(0, len(my_list_col) - 1, 2):
				main_sizer1.Add(wx.Button(self, label=str(my_list_col[n]), id=int(my_list_id[(n)]), size=(200, 40)), 2,
								wx.CENTER)
				self.Bind(wx.EVT_BUTTON, self.detect_on_button)
				main_sizer2.Add(
					wx.Button(self, label=str(my_list_col[n + 1]), id=int(my_list_id[(n + 1)]), size=(200, 40)), 2,
					wx.CENTER)
				self.Bind(wx.EVT_BUTTON, self.detect_on_button)
			main_sizer1.Add(wx.Button(self, label=str(my_list_col[(len(my_list_id) - 1)]), id=int(my_list_id[(n + 2)]),
									  size=(200, 40)), 2, wx.CENTER)
			self.Bind(wx.EVT_BUTTON, self.detect_on_button)

		else:
			for n in range(0, len(my_list_id) - 1, 2):
				main_sizer1.Add(wx.Button(self, label=str(my_list_col[n]), id=int(my_list_id[(n)]), size=(200, 40)), 2,
								wx.CENTER)
				self.Bind(wx.EVT_BUTTON, self.detect_on_button)
				main_sizer2.Add(
					wx.Button(self, label=str(my_list_col[n + 1]), id=int(my_list_id[(n + 1)]), size=(200, 40)), 2,
					wx.CENTER)
				self.Bind(wx.EVT_BUTTON, self.detect_on_button)

		main_sizer1.AddStretchSpacer()
		main_sizer2.AddStretchSpacer()
		self.SetSizer(top_sizer)
		self.back_button = wx.Button(self, label="Back", id=999, pos=(400, 500))
		self.back_button.Bind(wx.EVT_BUTTON, self.detect_on_button)

	def detect_on_button(self, event):
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
		self.engineer_name = wx.TextCtrl(self, pos=(150, 60), size=(250, -1), value=final_list[0])
		self.text = wx.StaticText(self, label="e-Mail Address :", pos=(20, 120))
		self.engineer_email = wx.TextCtrl(self, pos=(150, 120), value=final_list[1], size=(250, -1))
		self.text = wx.StaticText(self, label="Role :", pos=(20, 180))
		self.engineer_role = wx.ComboBox(self, pos=(230, 180), size=(170, -1), choices=role_list, value=final_list[2])
		self.text = wx.StaticText(self, label="Current Employee (0=No 1=Yes):", pos=(20, 240))
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
		# Update db with new Colleague details.
		con = sqlite3.connect("hs_audit.sqlite")
		con.execute("UPDATE T1 SET engineer='%s', email='%s', role='%s', active='%s' WHERE rowid='%s'" % (
			new_engineer, new_email, new_role, new_active, colleague_row_id))
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
		get_columns("0")# Get amount of leaver colleagues by passing "2" to get columns.
		main_sizer1.AddStretchSpacer()
		main_sizer2.AddStretchSpacer()

		if len(my_list_id) == 1:
			main_sizer1.Add(wx.Button(self, label=str(my_list_col[0]), id=int(my_list_id[(0)]), size=(200, 40)), 2,
							wx.CENTER)
			self.Bind(wx.EVT_BUTTON, self.detect_on_button)

		elif len(my_list_id) % 2 == 1:
			for n in range(0, len(my_list_col) - 1, 2):
				main_sizer1.Add(wx.Button(self, label=str(my_list_col[n]), id=int(my_list_id[(n)]), size=(200, 40)), 2,
								wx.CENTER)
				self.Bind(wx.EVT_BUTTON, self.detect_on_button)
				main_sizer2.Add(
					wx.Button(self, label=str(my_list_col[n + 1]), id=int(my_list_id[(n + 1)]), size=(200, 40)), 2,
					wx.CENTER)
				self.Bind(wx.EVT_BUTTON, self.detect_on_button)
			main_sizer1.Add(wx.Button(self, label=str(my_list_col[(len(my_list_id) - 1)]), id=int(my_list_id[(n + 2)]),
									  size=(200, 40)), 2, wx.CENTER)
			self.Bind(wx.EVT_BUTTON, self.detect_on_button)

		else:
			for n in range(0, len(my_list_id) - 1, 2):
				main_sizer1.Add(wx.Button(self, label=str(my_list_col[n]), id=int(my_list_id[(n)]), size=(200, 40)), 2,
								wx.CENTER)
				self.Bind(wx.EVT_BUTTON, self.detect_on_button)
				main_sizer2.Add(
					wx.Button(self, label=str(my_list_col[n + 1]), id=int(my_list_id[(n + 1)]), size=(200, 40)), 2,
					wx.CENTER)
				self.Bind(wx.EVT_BUTTON, self.detect_on_button)

		main_sizer1.AddStretchSpacer()
		main_sizer2.AddStretchSpacer()
		self.SetSizer(top_sizer)
		self.back_button = wx.Button(self, label="Back", id=999, pos=(400, 500))
		self.back_button.Bind(wx.EVT_BUTTON, self.detect_on_button)

	def detect_on_button(self, event):
		# event.Skip()
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
#############################Question Panels#################################
#############################################################################

class CreateQuestionsFrame(wx.Frame):
	def __init__(self, area, running_total = 0, aa={}, position = 0, parent = None):  # Pass frame height, width, name, and panel.
		self.title = "EPS - %s" % (area)
		super(CreateQuestionsFrame, self).__init__(parent, title = self.title, size=(800, 500))
		self.running_total = running_total
		self.area = area
		self.aa = aa
		self.position = position
		self.SetBackgroundColour("default")
		self.InitUI()
		self.Centre()
		self.Show()


	def InitUI(self):
		panel = wx.Panel(self)
		if self.area == "Van Audit":
			aa = {}
			global labels
			labels = []
			global question
			question = 0
			global all_audit_questions
			all_audit_questions = get_all_questions()
			sizerControl = wx.GridBagSizer(hgap=4, vgap=4)
		rboxPick = ["Yes", "No", "N/A", "Not answered yet"]
		#number of questions per section
		global required_questions
		if self.area == "Van Audit":
			self.running_total = 0
			required_questions = 5
		elif self.area == "RAMS Audit":
			required_questions = 7
		elif self.area == "PPE Audit":
			required_questions = 4
		elif self.area == "Tools Audit":
			required_questions = 5
		elif self.area == "HV Documentation Audit":
			required_questions = 5
		else:
			exit()

		self.running_total += required_questions
		print "Answers so far =%s" % self.aa
		print "Number of answers so far=%s" %(len(self.aa))
		print "Running Total = %s" %(self.running_total)
		sizerControl = wx.GridBagSizer(hgap=4, vgap=4)
		print "Range = %s to %s." % ((self.running_total- required_questions),self.running_total)
		for item in range(self.running_total - required_questions ,self.running_total):
			lbl = wx.StaticText(self)
			print type(item)
			print type(self.position)
			print type (all_audit_questions)
			rbox = wx.RadioBox(self, id=item, label="Q%r - %s" % (self.position + 1, all_audit_questions[item]), choices=rboxPick)
			rbox.SetSelection(3)
			self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, rbox)
			sizerControl.Add(rbox, pos=(self.position + 1, 1), span=(1, 5),
							 flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=2)
			self.position += 1
		self.save_button = wx.Button(self, label="Save")
		self.save_button.Bind(wx.EVT_BUTTON, self.save_answers)
		sizerControl.Add(self.save_button, pos=(self.position + 3, 5),
						 flag=wx.EXPAND | wx.LEFT | wx.RIGHT, border=2)

		sizerMain = wx.BoxSizer()
		sizerMain.Add(sizerControl)
		self.SetSizerAndFit(sizerMain)


	def onRadioBox(self, event):
		"""Event handler for RadioBox.."""
		rbox = event.GetEventObject()
		answer = rbox.GetSelection()
		question = rbox.GetId()
		print "Question = %s" % (question)
		print "Answer = %s" % (answer)
		self.aa[question] = answer
		print "Answers so far =%s" % self.aa
		print "Number of answers so far=%s" %(len(self.aa))

	def save_answers(self, event):
		print "Length of aa is %s, running total is %s." % (len(self.aa), self.running_total)
		if len(self.aa) < (self.running_total):  # Have all questions been answered
			Warn(self, "All answers have not been answered", caption = 'Warning!')
			return

		else:
			self.running_total = len(self.aa)
			self.GetParent()  # This assigns parent frame to frame.
			self.Close()  # This then closes frame removing the main menu.
			if len(self.aa) == 5:
				frame = CreateQuestionsFrame("RAMS Audit", self.running_total, self.aa)
			elif len(self.aa) == 12:
				frame = CreateQuestionsFrame("PPE Audit", self.running_total, self.aa)
			elif len(self.aa) == 16:
				frame = CreateQuestionsFrame("Tools Audit", self.running_total, self.aa)
			elif len(self.aa) == 21:
				frame = CreateQuestionsFrame("HV Documentation Audit", self.running_total, self.aa)
			else:
				self.aa[len(self.aa) + 1] = audit_id
				answers_db = dict.values(self.aa)
				del self.aa
				print answers_db
				print str(audit_id)
				print type(answers_db)
				print answers_db
				audit_date = dt.date.today()
				con = sqlite3.connect("hs_audit.sqlite")
				cur = con.cursor()
				cur.execute('INSERT INTO T4 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (answers_db))
				con.commit()
				con.close()
				con = sqlite3.connect("hs_audit.sqlite")
				con.execute('INSERT INTO T2 VALUES (?,?,?,?,?,?)',
							(audit_engineer, audit_date, audit_site, audit_job_number, audit_ver, audit_id))
				con.commit()
				con.close()
				self.GetParent()  # This assigns parent frame to frame.
				self.Close()  # This then closes frame removing the main menu.
				frame = AuditResultFrame(audit_id)


class AuditResultFrame(wx.Frame):
	def __init__(self, audit_no, parent = None,):
		super(AuditResultFrame, self).__init__(parent, title="EPS - Audit Result.", size=(500, 300))
		self.SetBackgroundColour("default")
		self.audit_no = audit_no
		self.InitUI()
		self.Centre()
		self.Show()

	def __init__(self):
		panel = wx.Panel(self)
		con = sqlite3.connect("hs_audit.sqlite")
		con.text_factory = str
		cur = con.cursor()
		cur.execute("SELECT * FROM T2 WHERE audit_id ='%s'" % (self.audit_no))
		result = cur.fetchall()
		con.close()
		print "Result is %s" % (result)
		variables_list = []
		while result:
			variables_list.extend(result.pop(0))
		print variables_list
		del variables_list[-1]
		print variables_list
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
		cur.execute("SELECT * FROM T4 WHERE audit_id = '%s'" % (self.audit_no))
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
		self.text = wx.StaticText(self, label=str("%.2f" % round(percent_correct,2)), style=wx.ALIGN_RIGHT)
		self.text.SetFont(font2)
		self.sizerControl.Add(self.text, pos=(31, 3))
		self.text = wx.StaticText(self, label="Audit ID        = ", style=wx.TEXT_ALIGNMENT_RIGHT)
		self.sizerControl.Add(self.text, pos=(32, 7))
		self.text = wx.StaticText(self, label=str(self.audit_no), style=wx.TEXT_ALIGNMENT_RIGHT)
		self.sizerControl.Add(self.text, pos=(32,8))
		self.text = wx.Button(self, label="Close")
		self.text.Bind(wx.EVT_BUTTON, self.close_audit)
		self.sizerControl.Add(self.text, pos=(33, 7))
		self.SetSizer(self.sizerControl)
		self.Show()

	def close_audit(self,event):
		frame = self.GetParent()  # This assigns parent frame to frame.
		frame.Close()  # This then closes frame removing the main menu.
		frame = SetUpFrame(500, 300, "H&S Audit App", FrontMenuPanel)


###################################
###########Frame Setup############
###################################

"""
class SetUpAuditFrame(wx.Frame):
	def __init__(self, audit_id):  # Pass frame height, width, name, and panel.
		wx.Frame.__init__(self, None, title="Audit Result", size=(750, 700))
		panel = AuditResultPanel(self, audit_id)
		self.Centre()
		self.Show()

class SelectAuditFrame(wx.Frame):
	def __init__(self, colleague_row_id):
		wx.Frame.__init__(self, None, title="Select Audit.", size=(750, 700))
		panel = SelectAuditPanel(self, colleague_row_id)
		self.Centre()
		self.Show()
"""

# This kicks everything off by calling frame and starting the app loop.
if __name__ == '__main__':
	app = wx.App(False)
	frame = FrontMenuFrame()
	app.MainLoop()

