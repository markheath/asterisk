# Asterisk for Silverlight using IronPython, 
# by Mark Heath, http://mark-dot-net.blogspot.com
import clr
import mvvm
import gameover
import highscore
from gamearea import GameArea

from System import TimeSpan
from System.Windows.Threading import DispatcherTimer
from System.Windows.Input import Key
from System.Windows import Visibility

class Asterisk():
    def __init__(self, xaml):
        self.labelLevel = xaml.labelLevel
        self.labelRecord = xaml.labelRecord
        self.highScore = highscore.HighScore()
        self.labelLevel.Text = "Level 1"
        self.labelRecord.Text = self.highScore.Message        
        self.setupGameLoop()
        self.currentLevel = 0
        self.xPosition = 0
        self.yPosition = 0
        self.keyDown = False
        self.gameArea = GameArea(xaml.gameCanvas)
        def messageLoaded(root):
            xaml.highScorePresenter.Content = root
        self.message = gameover.GameOver(messageLoaded)
        xaml.KeyDown += self.onKeyDown
        xaml.KeyUp += self.onKeyUp
        #xaml.Closing += lambda sender, args: self.Timer.Stop()
        self.buttonNewGame = xaml.buttonNewGame
        xaml.buttonNewGame.Click += self.newGameClick
        
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
                    self.buttonNewGame.IsEnabled = True
                    self.labelRecord.Text = self.highScore.Message
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

    def newGameClick(self, sender, args):
        self.newGame()
    
    def newGame(self):
        self.currentLevel = 0
        self.buttonNewGame.IsEnabled = False
        self.newLevel()
        self.Timer.Start()
        
    def newLevel(self):
        self.currentLevel += 1
        self.xPosition = 0
        self.yPosition = self.gameArea.Height / 2
        self.labelLevel.Text = 'Level ' + str(self.currentLevel)
        self.keyDown = False
        self.gameArea.RedrawScreen(self.currentLevel);
        self.gameArea.AddNewPosition(self.xPosition, self.yPosition)

    def onKeyDown(self, sender, args):
        if (args.Key == Key.Space):
            self.keyDown = True

    def onKeyUp(self, sender, args):
        if (args.Key == Key.Space):
            self.keyDown = False

Asterisk(xaml)