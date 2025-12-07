import wx
import pandas
from matplotlib import pyplot
import numpy

class Vegetable(wx.Frame):
    def __init__(self, parent=None, title=""):
        super().__init__(parent, title=title, size=(720,480))
        panel = wx.Panel(self)
        def createbutton(panel, label, callback):
            button = wx.Button(panel, label=label)
            button.Bind(wx.EVT_BUTTON, callback)
            font = button.GetFont()
            font.PointSize += 2
            button.SetFont(font)
            return button
        button1 = createbutton(panel, "Select Red Wine", self.open1)
        button2 = createbutton(panel, "Select White Wine", self.open2)
        startbutton1 = createbutton(panel, "Generate Individual", self.start1)
        startbutton2 = createbutton(panel, "Generate Grouped", self.start2)
        togglelog = createbutton(panel, "Y-axis Log Scaling", self.mod)
        kittybutton = createbutton(panel, "  ／l、\n（ﾟ､ ｡７ \n⠀l、ﾞ~ヽ  \n     じし(_,  )ノ", self.kitty)

        sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer2.AddStretchSpacer(1)
        sizer2.Add(button1, 0, wx.RIGHT, 8)
        sizer2.Add(button2, 0, wx.ALIGN_CENTER, 8)
        sizer2.AddStretchSpacer(1)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddStretchSpacer(4)
        sizer.Add(sizer2, 0, wx.ALIGN_CENTER | wx.ALL, 8)
        sizer.AddStretchSpacer(2)
        sizer.Add(startbutton1, 0, wx.ALIGN_CENTER | wx.ALL, 8)
        sizer.AddStretchSpacer(1)
        sizer.Add(startbutton2, 0, wx.ALIGN_CENTER | wx.ALL, 8)
        sizer.AddStretchSpacer(1)
        sizer.Add(togglelog, 0, wx.ALIGN_CENTER | wx.ALL, 8)
        sizer.AddStretchSpacer(2)
        sizer.Add(kittybutton, 12, wx.ALIGN_CENTER | wx.ALL, 8)
        sizer.AddStretchSpacer(4)
        panel.SetSizer(sizer)
    
        self.Centre()
        self.Show()
        self.data1 = None
        self.data2 = None
        self.log = False

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
            
    def start(self):
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
        return info1, info2
        
    def start1(self, _):
        if self.data1 is None or self.data2 is None:
            wx.LogError("Please load both CSV files first.")
            return

        want = ["fixed acidity","volatile acidity","citric acid","residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol","quality"]
        if set(want).issubset(self.data1.columns) or set(want).issubset(self.data2.columns):
            wx.LogError("Please load in the correct file.")
            return
        
        info1, info2 = self.start()
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
        if self.log:
            ax.set_yscale('log', base=2)
        ax.set_ylabel('Volume (ml)')
        ax.set_xticks(x + width, want)
        ax.legend(loc='upper left', ncols=3)
        pyplot.show()

    def start2(self, _):
        if self.data1 is None or self.data2 is None:
            wx.LogError("Please load both CSV files first.")
            return

        want = ["fixed acidity","volatile acidity","citric acid","residual sugar","chlorides","free sulfur dioxide","total sulfur dioxide","density","pH","sulphates","alcohol","quality"]
        types = ["Red Wine", "White Wine"]
        if set(want).issubset(self.data1.columns) or set(want).issubset(self.data2.columns):
            wx.LogError("Please load in the correct file.")
            return
        
        info1, info2 = self.start()
        means = dict(zip(want, zip(info1, info2)))
        
        x = numpy.array([i for i in range(2)])
        width = 0.07
        multiplier = -4.5

        fig, ax = pyplot.subplots(layout='constrained')

        for attribute, measurement in means.items():
            offset = width * multiplier
            rects = ax.bar(x + offset, measurement, width, label=attribute)
            ax.bar_label(rects, padding=3)
            multiplier += 1

        ax.set_title('Wine Quality')
        if self.log:
            ax.set_yscale('log', base=2)
        ax.set_ylabel('Volume (ml)')
        ax.set_xticks(x + width, types)
        ax.legend(loc='upper left', ncols=3)
        pyplot.show()
    
    def mod(self, _):
        self.log = not self.log
    
    def kitty(self, _):
        wx.LogError("   ／l、                  meow\n （ﾟ､ ｡７ \n⠀l、ﾞ~ヽ  \n  じし(_,  )ノ")
        
if __name__ == "__main__":
    app = wx.App(False)
    Vegetable()
    app.MainLoop()