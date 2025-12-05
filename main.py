import wx
import pandas
from matplotlib import pyplot

class Vegetable(wx.Frame):
    def __init__(self, parent=None, title=""):
        super().__init__(parent, title=title, size=(720,480))
        panel = wx.Panel(self)
        button1 = wx.Button(panel, label="1")
        button1.Bind(wx.EVT_BUTTON, self.open1)
        button2 = wx.Button(panel, label="2")
        button2.Bind(wx.EVT_BUTTON, self.open2)
        startbutton = wx.Button(panel, label="start")
        startbutton.Bind(wx.EVT_BUTTON, self.start) 

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.AddStretchSpacer(1)
        sizer2.Add(button1, 0, wx.RIGHT, 10)
        sizer2.Add(button2, 0, wx.ALIGN_CENTER, 10)
        sizer2.AddStretchSpacer(1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(4)
        sizer.Add(sizer2, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.AddStretchSpacer(1)
        sizer.Add(startbutton, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.AddStretchSpacer(6)
        panel.SetSizer(sizer)
    
        self.Centre()
        self.Show()
        self.data1 = None
        self.data2 = None

    def open1(self, _):
        with wx.FileDialog(self, "Open CSV File", wildcard="CSV files (*.csv)|*.csv") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
        
            try:
                self.data1 = pandas.read_csv(path)
            except IOError:
                wx.LogError("Cannot open file. ")
    
    def open2(self, _):
        with wx.FileDialog(self, "Open CSV File", wildcard="CSV files (*.csv)|*.csv") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
        
            try:
                self.data2 = pandas.read_csv(path)
            except IOError:
                wx.LogError("Cannot open file. ")
            
    def start(self, _):
        print(self.data1, self.data2)

if __name__ == "__main__":
    app = wx.App(False)
    Vegetable()
    app.MainLoop()