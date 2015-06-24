__author__ = 'Paul Finch'
import wx


class VanAuditPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)
        main_sizer = wx.GridBagSizer(5, 5)
        main_sizer.Add(wx.StaticText(self, label="Van Audit Questions"), (0, 0), span=(1, 7), flag=wx.ALIGN_CENTER)
        for n in range(1, 6):
            print n
            main_sizer.Add(wx.StaticText(self, label="Q%s" %(n)), (n, 0))
        self.SetSizer(main_sizer)





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
