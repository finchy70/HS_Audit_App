import wx
import sqlite3

class VanAuditAnswersPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        sizerControl = wx.GridBagSizer(hgap=4,vgap = 4)


        rboxPick = ["Yes", "No", "N/A", "Not answered yet"]
        con = sqlite3.connect("hs_audit.sqlite")
        con.text_factory = str
        cur = con.cursor()
        cur.execute("SELECT vaq1, vaq2, vaq3, vaq4 FROM T3 WHERE audit_ver =1")#, (change 1 to max_audit_id))
        result = [[str(item) for item in results] for results in cur.fetchall()]
        con.close()
        global vaa
        vaa ={}
        global labels
        labels = []
        while result:
            labels.extend(result.pop(0))

        #Create, layout and bind the RadioBoxes
        question = 1
        for row, label in enumerate(labels):

            lbl = wx.StaticText(self)
            rbox = wx.RadioBox(self, id=question, label="Q%r - %s" % (question, label), choices=rboxPick)
            rbox.SetSelection(3)
            self.Bind(wx.EVT_RADIOBOX, self.onRadioBox, rbox)              
            sizerControl.Add(rbox, pos=(row+1, 1), span=(1,5), 
                             flag=wx.EXPAND|wx.LEFT|wx.RIGHT,border=2)
            question += 1
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
        vaa[question] = answer
        print vaa

    def save_answers(self, event):
        if len(vaa) < len(labels):
            return

        else:
            global full_audit_answers
            full_audit_answers = {}
            for f in range (1, 5):
                full_audit_answers[f] = vaa[f]
                print full_audit_answers

        frame = self.GetParent()  # This assigns parent frame to frame.
        frame.Close()  # This then closes frame removing the main menu.
        frame = SetUpFrame(600, 500, "Method Statement and RAMS.", RamsAuditAnswersPanel)



# This creates the frame for the all menus.
class SetUpFrame(wx.Frame):
    def __init__(self, fwide, fhigh, ftitle, Panel):  # Pass frame height, width, name, and panel.
        wx.Frame.__init__(self, None, title=ftitle, size=(fwide, fhigh))
        panel = Panel(self)
        self.Centre()
        self.Show()


#This kicks everything off by calling frame and starting the app loop.
if __name__ == '__main__':
    app = wx.App(False)
    frame = SetUpFrame(600, 500, "Van Audit", VanAuditAnswersPanel)
    app.MainLoop()