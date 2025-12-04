import wx
import pandas
from matplotlib import pyplot

class Vegetable(wx.Frame):
    def __init__(self, parent=None, title=""):
        super().__init__(parent, title=title, size=(720,480))
        panel = wx.Panel(self)
        button = wx.Button(panel, label="meow")
        button.Bind(wx.EVT_BUTTON, self.open)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(button, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        panel.SetSizer(sizer)
    
        self.Centre()
        self.Show()

    def open(self, _):
        with wx.FileDialog(self, "Open CSV File", wildcard="CSV files (*.csv)|*.csv") as fileDialog:
            if fileDialog.ShowModal() == wx.ID_CANCEL:
                return
            path = fileDialog.GetPath()
        
            try:
                data = pandas.read_csv(path)
                print(data)
            except IOError:
                wx.LogError("Cannot open file. ")
            

if __name__ == "__main__":
    app = wx.App(False)
    Vegetable()
    app.MainLoop()