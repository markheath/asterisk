using System;
using System.Net;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Documents;
using System.Windows.Ink;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Animation;
using System.Windows.Shapes;
using System.ComponentModel;
using System.Windows.Threading;

namespace Asterisk
{
    public class MainPageViewModel : ViewModelBase
    {
        private string level;
        private string record;
        private readonly HighScore highScore;
        private int currentLevel;
        private int xPosition;
        private int yPosition;
        private bool keyDown;
        private DispatcherTimer timer;
        private readonly GameArea gameArea;
        private GameOverViewModel gameOver;
        private RelayCommand newGameCommand;

        public string Level
        {
            get { return level; }
            set
            {
                if (level != value)
                {
                    level = value;
                    RaisePropertyChanged("Level");
                }
            }
        }

        public string Record
        {
            get { return record; }
            set
            {
                if (record != value)
                {
                    record = value;
                    RaisePropertyChanged("Record");
                }
            }
        }

        public ICommand NewGameCommand
        {
            get { return this.newGameCommand; }
        }

        public GameOverViewModel GameOverViewModel
        {
            get
            {
                return gameOver;
            }
        }

        public MainPageViewModel(MainPage mainPage)
        {
            this.highScore = new HighScore();
            this.Level = "Level 1";
            this.Record = this.highScore.Message;
            this.SetupGameLoop();
            this.currentLevel = 0;
            this.xPosition = 0;
            this.yPosition = 0;
            this.keyDown = false;
            this.gameArea = new GameArea(mainPage.gameCanvas);

            this.gameOver = new GameOverViewModel();
            mainPage.KeyDown += this.OnKeyDown;
            mainPage.KeyUp += this.OnKeyUp;
            //xaml.Closing += lambda sender, args: self.Timer.Stop()

            this.newGameCommand = new RelayCommand(NewGame);
        }

        private void SetupGameLoop()
        {
            this.timer = new DispatcherTimer();
            this.timer.Interval = TimeSpan.FromMilliseconds(20.0);
            this.timer.Tick += this.OnTick;
        }

        private void OnTick(object sender, EventArgs args)
        {
            this.xPosition++;
            this.yPosition += (this.keyDown ? -1 : 1);
            this.CheckPosition();
        }

        private void CheckPosition()
        {
            bool crash = !this.gameArea.AddNewPosition(new Point(this.xPosition, this.yPosition));

            if (crash)
            {
                Action<string> onDone = (message) =>
                {
                    this.gameOver.IsHighScore = Visibility.Collapsed;
                    if (this.IsHighScore())
                    {
                        this.highScore.Name = message;
                        this.highScore.Level = this.currentLevel;
                        this.newGameCommand.SetCanExecute(true);
                        this.Record = this.highScore.Message;
                        this.highScore.Save();
                    }
                    else
                    {
                        this.NewGame();
                    }
                };
                this.timer.Stop();
                if (this.IsHighScore())
                {
                    this.gameOver.Show("High Score", onDone, true);
                }
                else
                {
                    this.gameOver.Show("Game Over, Play Again?", onDone);
                }
            }
            else
            {
                if (this.xPosition >= this.gameArea.Width)
                {
                    this.NewLevel();
                }
            }
        }

        private bool IsHighScore()
        {
            return this.currentLevel > this.highScore.Level;
        }

        private void NewGame()
        {
            this.currentLevel = 0;
            this.newGameCommand.SetCanExecute(false);
            this.NewLevel();
            this.timer.Start();
        }

        private void NewLevel()
        {
            this.currentLevel++;
            this.xPosition = 0;
            this.yPosition = this.gameArea.Height / 2;
            this.Level = String.Format("Level {0}", this.currentLevel);
            this.keyDown = false;
            this.gameArea.RedrawScreen(this.currentLevel);
            this.gameArea.AddNewPosition(new Point(this.xPosition, this.yPosition));
        }

        private void OnKeyDown(object sender, KeyEventArgs args)
        {
            if (args.Key == Key.Space)
            {
                this.keyDown = true;
            }
        }

        private void OnKeyUp(object sender, KeyEventArgs args)
        {
            if (args.Key == Key.Space)
            {
                this.keyDown = false;
            }
        }
    }
}
