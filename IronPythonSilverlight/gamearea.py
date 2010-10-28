import clr
import mvvm

from System import Random
from System.Windows import Point
from System.Windows.Shapes import Line, Polyline
from System.Windows.Media import SolidColorBrush, Color
from System.Windows.Controls import Canvas
from System.Net import WebClient
from System import Uri, UriKind
from System.Diagnostics import Debug

class GameArea:
    Height = 200
    Width = 300
    starXaml = """
<Path xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
  Stroke="White" 
  StrokeThickness="2" 
  StrokeStartLineCap="Round" 
  StrokeEndLineCap="Round" 
  StrokeLineJoin="Round" 
  Data="M 0,0 l 5,0 l 2.5,-5 l 2.5,5 l 5,0 l -3.5,5 l 1,5 l -5,-2.5 l -5,2.5 l 1,-5 Z">
  <Path.RenderTransform>
    <ScaleTransform ScaleX="0.8" ScaleY="0.8" />
  </Path.RenderTransform>
</Path>"""    
    
    def __init__(self, canvas):
        self.canvas = canvas
        self.findRootVisual()
        self.rand = Random()
        self.RedrawScreen(0)
        wc = WebClient()
        wc.DownloadStringCompleted += self.xamlDownloaded
        wc.DownloadStringAsync(Uri('star.xaml',UriKind.Relative))
    
    def findRootVisual(self):
        self.rootVisual = self.canvas
        while self.rootVisual.Parent:
            self.rootVisual = self.rootVisual.Parent
    
    def xamlDownloaded(self, sender, args):
        if not args.Error:
            self.starXaml = args.Result
        else:
            pass #raise args.Error
            
    def addLine(self, _from, to):
        line = Line()
        line.X1 = _from[0]
        line.Y1 = _from[1]
        line.X2 = to[0]
        line.Y2 = to[1]
        line.Stroke = SolidColorBrush(Color.FromArgb(255,255,255,255)) # Brushes.White
        line.StrokeThickness = 2.0
        self.canvas.Children.Add(line)
    
    def isCollision(self, x, y):
        width = self.Width
        height = self.Height
        if y <= 0 or y >= height:
            return True
        if x >= width:
            return not ((height / 2 + 15) > y > (height / 2 - 15))
        testPoint = Point(x,y)
        hostPoint = self.canvas.TransformToVisual(self.rootVisual).Transform(testPoint)
        #Debug.WriteLine('Test Point: {0}, Host Point: {1}'.format(testPoint,hostPoint))
        if mvvm.CheckCollisionPoint(hostPoint, self.canvas):
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
            star = mvvm.XamlLoader(self.starXaml).Root
            self.stars.append(star)
            Canvas.SetLeft(star, self.rand.Next(10, self.Width - 10))
            Canvas.SetTop(star, self.rand.Next(2, self.Height - 10))
            self.canvas.Children.Add(star)
            
        self.polyline = Polyline()
        self.polyline.Stroke = SolidColorBrush(Color.FromArgb(255,255,255,0)) # Brushes.Yellow
        self.polyline.StrokeThickness = 2.0
        self.canvas.Children.Add(self.polyline)