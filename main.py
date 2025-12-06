import wx
import pandas
from matplotlib import pyplot
import numpy

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
        if self.data1 is None or self.data2 is None:
            wx.LogError("Please load both CSV files first.")
            return
        
        want = ("fixed acidity","volatile acidity","citric acid","residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol","quality")
        if want not in self.data1.columns or want not in self.data2.columns:
            wx.LogError("Please load in the correct file.")
            return

        num1 = self.data1.to_numpy()
        num2 = self.data2.to_numpy()
        
        info1 = []
        info2 = []

        for i in range(12):
            one = 0
            two = 0
            for v in num1:
                one += float(str(v)[2:-2].split(';')[i])
            one /= len(num1)
            info1.append(round(one, 3))
            for v in num2:
                two += float(str(v)[2:-2].split(';')[i])
            two /= len(num2)
            info2.append(round(two, 3))
        
        means = {
            "Red Wine": info1,
            "White Wine": info2
        }
        
        x = numpy.array([i for i in range(12)])
        width = 0.25
        multiplier = 0.5

        fig, ax = pyplot.subplots(layout='constrained')

        for attribute, measurement in means.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, measurement, width, label=attribute)
            ax.bar_label(rects, padding=3)
            multiplier += 1

        ax.set_title('Wine Quality')
        ax.set_yscale('log', base=2)
        ax.set_ylabel('Volume (ml)')
        ax.set_xticks(x + width, want)
        ax.legend(loc='upper left', ncols=3)
        pyplot.show()
        
if __name__ == "__main__":
    app = wx.App(False)
    Vegetable()
    app.MainLoop()