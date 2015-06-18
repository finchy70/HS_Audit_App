__author__ = 'Paul'

import pandas
import wx
import sqlite3

con = sqlite3.connect("hs_audit.sqlite")
cur = con.cursor()
con.row_factory = lambda cursor, row: row[0]
c = con.cursor()
ids = c.execute('SELECT engineer FROM T1').fetchall()

########################################################################
class MyFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Test")
        panel = wx.Panel(self)

        myList = ids
        cbo = wx.ComboBox(panel)
        cbo.SetItems(myList)

        self.Show()

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyFrame()
    app.MainLoop()