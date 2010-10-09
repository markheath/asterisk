# Asterisk for WPF using IronPython, 
# by Mark Heath, http://mark-dot-net.blogspot.com
import mvvm
import clr
import os
from GameArea import GameArea

clr.AddReference("WindowsBase")
clr.AddReference("PresentationCore")
clr.AddReference("PresentationFramework")

from System import TimeSpan
from System.Windows import Visibility
from System.Windows.Threading import DispatcherTimer
from System.Windows.Input import Key

class ViewModel(mvvm.ViewModelBase):
    def __init__(self, xaml):
        mvvm.ViewModelBase.__init__(self)
        self.highScore = HighScore()
        self.Level = "Level 1"
        self.Record = self.highScore.Message
        self.NewGameCommand = mvvm.Command(self.newGame)
        self.setupGameLoop()
        self.currentLevel = 0
        self.xPosition = 0
        self.yPosition = 0
        self.keyDown = False
        self.gameArea = GameArea(xaml.gameCanvas)
        self.message = GameOver()
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

class HighScore:
    def __init__(self):
        self.Level = 0
        self.Name = 'Nobody'
        self.LoadHighScore()

    def getMessage(self):
        return 'Level {0} by {1}'.format(self.Level, self.Name)

    Message = property(getMessage)

    def Save(self):
        f = open('record.txt', 'w')
        f.write('{0}:{1}'.format(self.Level, self.Name))

    def LoadHighScore(self):
        if os.path.isfile('record.txt'):
            record = open('record.txt').readline()
            parts = record.split(':')
            if(len(parts) == 2):
                self.Level = int(parts[0])
                self.Name = parts[1]

class GameOver:
    def __init__(self):
        self.xaml = mvvm.XamlLoader('gameover.xaml')
        self.viewModel = GameOverViewModel()
        self.xaml.Root.DataContext = self.viewModel
        self.xaml.Root.Visibility = Visibility.Collapsed
        
    def Show(self, message, callback, isHighScore=False):
        self.viewModel.Message = message
        self.viewModel.IsHighScore = Visibility.Visible if isHighScore else Visibility.Collapsed
        self.xaml.Root.Visibility = Visibility.Visible
        self.viewModel.callback=callback

class GameOverViewModel(mvvm.ViewModelBase):
    def __init__(self):
        mvvm.ViewModelBase.__init__(self)
        self._message = ''
        self._name = ''
        self.callback = None
        self.OKCommand = mvvm.Command(self.onOK)
        self._isHighScore = Visibility.Collapsed
        
    def onOK(self):
        if self.callback:
            self.callback(self.Name)
    
    def setMessage(self, message):
        if self._message != message:
            self._message = message
            self.RaisePropertyChanged("Message")
    
    def getMessage(self):
        return self._message
        
    def setIsHighScore(self, isHighScore):
        if self._isHighScore != isHighScore:
            self._isHighScore = isHighScore
            self.RaisePropertyChanged("IsHighScore")
    
    def getIsHighScore(self):
        return self._isHighScore
    
    def getName(self):
        return self._name
        
    def setName(self, name):
        if self._name != name:
            self._name = name
            self.RaisePropertyChanged("Name")
    
    Message = property(getMessage, setMessage)
    Name = property(getName, setName)
    IsHighScore = property(getIsHighScore, setIsHighScore)

xaml = mvvm.XamlLoader('asterisk.xaml')
xaml.Root.DataContext = ViewModel(xaml)
mvvm.RunApp(xaml.Root)