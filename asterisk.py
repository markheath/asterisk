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
        xaml.Root.KeyDown += self.onKeyDown
        xaml.Root.KeyUp += self.onKeyUp
        xaml.Root.Closing += lambda sender, args: self.Timer.Stop()

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
            if self.xPosition >= self.gameArea.Width:
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
        self.Person = 'Nobody'
        self.LoadHighScore()

    def getMessage(self):
        return 'Level {0} by {1}'.format(self.Level, self.Person)

    Message = property(getMessage)

    def SaveHighScore(self, score, person):
        f = open('record.txt', 'w')
        f.write('{0}:{1}'.format(score,person))

    def LoadHighScore(self):
        if os.path.isfile('record.txt'):
            record = open('record.txt').readline()
            parts = record.split(':')

xaml = mvvm.XamlLoader('asterisk.xaml')
xaml.Root.DataContext = ViewModel(xaml)
mvvm.RunApp(xaml.Root)