__author__ = 'Paul Finch'
import wx
import sqlite3


class VanAuditPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        font1 = wx.Font(20, wx.FONTFAMILY_MODERN, wx.FONTSTYLE_SLANT, wx.FONTWEIGHT_BOLD)
        text1 = "Van Audit Questions"
        heading = wx.StaticText(self, -1, label=text1, style=wx.ALIGN_CENTER)
        heading.SetFont(font1)
        con = sqlite3.connect("hs_audit.sqlite")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT vaq1, vaq2, vaq3, vaq4 FROM T3 WHERE audit_ver =1")#, (change 1 to max_audit_id))
        result = [[str(item) for item in results] for results in cur.fetchall()]
        con.close()
        questions = []
        while result:
            questions.extend(result.pop(0))
        print questions
        print type(questions)
        audit_questions = wx.GridSizer(5,3)
        question_number = 1

            print "This is n :-  %s" %(n)
            audit_questions.for n in questions:Add(wx.GridSizer(wx.StaticText(self, label="Q%r %r" % (question_number, n))))
            audit_questions.Add(wx.StaticText(self, label=" "))
            question_number += 1
        self.SetSizer(audit_question)





class SetUpFrame(wx.Frame):
    def __init__(self, fwide, fhigh, ftitle, Panel):  # Pass frame height, width, name, and panel.
        wx.Frame.__init__(self, None, title=ftitle, size=(fwide, fhigh))
        panel = Panel(self)
        self.Centre()
        self.Show()


# This kicks everything off by calling frame and starting the app loop.
if __name__ == '__main__':
    app = wx.App(False)
    frame = SetUpFrame(1000, 500, "H&S Audit App", VanAuditPanel)
    app.MainLoop()
