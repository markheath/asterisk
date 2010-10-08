# Asterisk for WPF using IronPython, 
# by Mark Heath, http://mark-dot-net.blogspot.com
import mvvm
import clr
clr.AddReference("WindowsBase")
clr.AddReference("PresentationCore")
clr.AddReference("PresentationFramework")
from System import TimeSpan, Random
from System.Windows import Point
from System.Windows.Controls import Canvas
from System.Windows.Threading import DispatcherTimer
from System.Windows.Shapes import Line, Polyline
from System.Windows.Media import Brushes
from System.Windows.Input import Key

class ViewModel(mvvm.ViewModelBase):
    def __init__(self, xaml):
        mvvm.ViewModelBase.__init__(self)
        self.Level = "Level 1"
        self.Record = "Level 1 by nobody"
        self.canvas = xaml.gameCanvas
        self.NewGameCommand = mvvm.Command(self.newGame)
        self.setupGameLoop()
        self.currentLevel = 0
        self.xPosition = 0
        self.yPosition = 0
        self.keyDown = False
        self.gameArea = (300,200)
        self.redrawScreen()
        self.rand = Random()
        xaml.Root.KeyDown += self.onKeyDown
        xaml.Root.KeyUp += self.onKeyUp
        xaml.Root.Closing += lambda sender, args: self.Timer.Stop()
        self.stars = []

    def setupGameLoop(self):
        self.Timer = DispatcherTimer()
        self.Timer.Interval = TimeSpan.FromMilliseconds(20.0)
        self.Timer.Tick += self.onTick
    
    def onTick(self, sender, args):
        self.xPosition += 1
        self.yPosition += (-1 if self.keyDown else 1)
        self.checkPosition()
        self.polyline.Points.Add(Point(self.xPosition, self.yPosition))

    def isCollision(self):
        width = self.gameArea[0]
        height = self.gameArea[1]
        if self.yPosition <= 0 or self.yPosition >= height:
            return True
        if self.xPosition >= width:
            return not ((height / 2 + 15) > self.yPosition > (height / 2 - 15))
        for star in self.stars:
            testX = self.xPosition - Canvas.GetLeft(star)
            testY = self.yPosition - Canvas.GetTop(star)
            if mvvm.CheckCollisionPoint(Point(testX, testY), star):
                return True

    def checkPosition(self):
        crash = False

        if self.isCollision():
            crash = True

        if crash:
            self.Timer.Stop()
            print "Game Over"
            #if self.currentLevel > self.recordLevel:
            #    InputStringDialog dlg = new InputStringDialog("High Score! Enter your name:",recordName,20);
            #    dlg.ShowDialog();
            #    recordName = dlg.UserInput;
            #    nRecordLevel = nLevel;
            #    ShowRecord();
            #else:
            #    MessageBox.Show("Game Over");
            self.NewGameCommand.canExecute = True
            self.NewGameCommand.RaiseCanExecuteChanged()
        else:
            if self.xPosition >= self.gameArea[0]:
                self.newLevel()

    def newGame(self):
        self.NewGameCommand.canExecute = False
        self.NewGameCommand.RaiseCanExecuteChanged()
        self.currentLevel = 0
        self.newLevel()
        self.Timer.Start()
        
    def newLevel(self):
        self.currentLevel += 1
        self.xPosition = 0
        self.yPosition = self.gameArea[1] / 2
        self.Level = 'Level ' + str(self.currentLevel)
        self.RaisePropertyChanged("Level")
        self.keyDown = False
        self.redrawScreen();
        self.polyline.Points.Clear()
        self.polyline.Points.Add(Point(self.xPosition, self.yPosition))
    
    def addLine(self, _from, to):
        line = Line()
        line.X1 = _from[0]
        line.Y1 = _from[1]
        line.X2 = to[0]
        line.Y2 = to[1]
        line.Stroke = Brushes.White
        line.StrokeThickness = 2.0
        self.canvas.Children.Add(line)
        
    def redrawScreen(self):
        self.canvas.Children.Clear()
        width = self.gameArea[0]
        height = self.gameArea[1]
        self.addLine((0,0), (width,0)) #line across top
        self.addLine((0,height), (width, height)) # line across botom
        self.addLine((width,0), (width, height / 2 - 15))
        self.addLine((width,height / 2 + 15), (width, height))

        self.stars = []
        for n in range(self.currentLevel * 3):
            star = mvvm.XamlLoader('star.xaml').Root
            self.stars.append(star)
            Canvas.SetLeft(star, self.rand.Next(10, self.gameArea[0] - 10))
            Canvas.SetTop(star, self.rand.Next(0, self.gameArea[1] - 10))
            self.canvas.Children.Add(star)
            
        #   g.DrawString("*",fnt,new SolidBrush(Color.White),new Point(rand.Next(10, rectMain.Width - 10),rand.Next(0, rectMain.Height - 10)));
        self.polyline = Polyline()
        self.polyline.Stroke = Brushes.Yellow
        self.polyline.StrokeThickness = 2.0
        self.canvas.Children.Add(self.polyline)

    def onKeyDown(self, sender, args):
        if (args.Key == Key.Space):
            self.keyDown = True

    def onKeyUp(self, sender, args):
        if (args.Key == Key.Space):
            self.keyDown = False

xaml = mvvm.XamlLoader('asterisk.xaml')
xaml.Root.DataContext = ViewModel(xaml)
mvvm.RunApp(xaml.Root)