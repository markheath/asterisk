import clr
import mvvm
clr.AddReference("WindowsBase")
clr.AddReference("PresentationCore")
clr.AddReference("PresentationFramework")

from System import Random
from System.Windows import Point
from System.Windows.Shapes import Line, Polyline
from System.Windows.Media import Brushes
from System.Windows.Controls import Canvas

class GameArea:
    Height = 200
    Width = 300
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.rand = Random()
        self.RedrawScreen(0)
    
    def addLine(self, _from, to):
        line = Line()
        line.X1 = _from[0]
        line.Y1 = _from[1]
        line.X2 = to[0]
        line.Y2 = to[1]
        line.Stroke = Brushes.White
        line.StrokeThickness = 2.0
        self.canvas.Children.Add(line)
    
    def isCollision(self, x, y):
        width = self.Width
        height = self.Height
        if y <= 0 or y >= height:
            return True
        if x >= width:
            return not ((height / 2 + 15) > y > (height / 2 - 15))
        for star in self.stars:
            testX = x - Canvas.GetLeft(star)
            testY = y - Canvas.GetTop(star)
            if mvvm.CheckCollisionPoint(Point(testX, testY), star):
                return True
    
    def AddNewPosition(self, x, y):
        self.polyline.Points.Add(Point(x, y))
        if self.isCollision(x, y):
            return False
        return True
    
    def drawBorders(self, width, height):
        self.addLine((0,0), (width,0)) #line across top
        self.addLine((0,height), (width, height)) # line across botom
        self.addLine((width,0), (width, height / 2 - 15))
        self.addLine((width,height / 2 + 15), (width, height))
    
    def RedrawScreen(self, level):
        self.canvas.Children.Clear()
        self.drawBorders(self.Width, self.Height)

        self.stars = []
        for n in range(level * 3):
            star = mvvm.XamlLoader('star.xaml').Root
            self.stars.append(star)
            Canvas.SetLeft(star, self.rand.Next(10, self.Width - 10))
            Canvas.SetTop(star, self.rand.Next(2, self.Height - 10))
            self.canvas.Children.Add(star)
            
        self.polyline = Polyline()
        self.polyline.Stroke = Brushes.Yellow
        self.polyline.StrokeThickness = 2.0
        self.canvas.Children.Add(self.polyline)