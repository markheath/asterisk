# Asterisk for WPF using IronPython, 
# by Mark Heath, http://mark-dot-net.blogspot.com
import mvvm
import clr
import GameOver
import HighScore
from GameArea import GameArea

clr.AddReference("WindowsBase")
clr.AddReference("PresentationCore")
clr.AddReference("PresentationFramework")

from System import TimeSpan
from System.Windows.Threading import DispatcherTimer
from System.Windows.Input import Key
from System.Windows import Visibility

class ViewModel(mvvm.ViewModelBase):
    def __init__(self, xaml):
        mvvm.ViewModelBase.__init__(self)
        self.highScore = HighScore.HighScore()
        self.Level = "Level 1"
        self.Record = self.highScore.Message
        self.NewGameCommand = mvvm.Command(self.newGame)
        self.setupGameLoop()
        self.currentLevel = 0
        self.xPosition = 0
        self.yPosition = 0
        self.keyDown = False
        self.gameArea = GameArea(xaml.gameCanvas)
        self.message = GameOver.GameOver()
        xaml.Root.KeyDown += self.onKeyDown
        xaml.Root.KeyUp += self.onKeyUp
        xaml.Root.Closing += lambda sender, args: self.Timer.Stop()
        xaml.highScorePresenter.Content = self.message.xaml.Root

    def setupGameLoop(self):
        self.Timer = DispatcherTimer()
        self.Timer.Interval = TimeSpan.FromMilliseconds(20.0)
        self.Timer.Tick += self.onTick
    
    def onTick(self, sender, args):
        self.xPosition += 1
        self.yPosition += (-1 if self.keyDown else 1)
        
        self.checkPosition()

    def checkPosition(self):
        crash = not self.gameArea.AddNewPosition(self.xPosition, self.yPosition)

        if crash:
            def OnDone(message):
                self.message.xaml.Root.Visibility = Visibility.Collapsed
                if self.isHighScore():
                    self.highScore.Name = message
                    self.highScore.Level = self.currentLevel
                    self.NewGameCommand.canExecute = True
                    self.NewGameCommand.RaiseCanExecuteChanged()
                    self.Record = self.highScore.Message
                    self.RaisePropertyChanged("Record")
                    self.highScore.Save()
                else:
                    self.newGame()
                
            self.Timer.Stop()
            print "Game Over"
            if self.isHighScore():
                self.message.Show("High Score", OnDone, True)
            else:
                self.message.Show("Game Over, Play Again?", OnDone)
        else:
            if self.xPosition >= self.gameArea.Width:
                self.newLevel()

    def isHighScore(self):
        return self.currentLevel > self.highScore.Level

    def newGame(self):
        self.NewGameCommand.canExecute = False
        self.NewGameCommand.RaiseCanExecuteChanged()
        self.currentLevel = 0
        self.newLevel()
        self.Timer.Start()
        
    def newLevel(self):
        self.currentLevel += 1
        self.xPosition = 0
        self.yPosition = self.gameArea.Height / 2
        self.Level = 'Level ' + str(self.currentLevel)
        self.RaisePropertyChanged("Level")
        self.keyDown = False
        self.gameArea.RedrawScreen(self.currentLevel);
        self.gameArea.AddNewPosition(self.xPosition, self.yPosition)

    def onKeyDown(self, sender, args):
        if (args.Key == Key.Space):
            self.keyDown = True

    def onKeyUp(self, sender, args):
        if (args.Key == Key.Space):
            self.keyDown = False



xaml = mvvm.XamlLoader('asterisk.xaml')
xaml.Root.DataContext = ViewModel(xaml)
mvvm.RunApp(xaml.Root)