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

namespace Asterisk
{
    public class GameOverViewModel : ViewModelBase
    {
        private string message;
        private string name;
        private readonly ICommand okCommand;
        private Visibility isHighScore;
        private Visibility visibility;
        private Action<string> callback;

        public GameOverViewModel()
        {
            this.okCommand = new RelayCommand(onOK);
            this.isHighScore = Visibility.Collapsed;
            this.visibility = Visibility.Collapsed;
        }

        public Visibility Visibility
        {
            get { return visibility; }
            set
            {
                if (visibility != value)
                {
                    visibility = value;
                    RaisePropertyChanged("Visibility");
                }
            }
        }

        public ICommand OKCommand
        {
            get { return this.okCommand; }
        }

        private void onOK()
        {
            this.Visibility = Visibility.Collapsed;
            if (this.callback != null)
            {
                this.callback(Name);
            }
        }

        public string Message
        {
            get 
            {
                return this.message;
            }
            set
            {
                if (this.message != value)
                {
                    this.message = value;
                    RaisePropertyChanged("Message");
                }
            }
        }
    
        public Visibility IsHighScore
        {
            get 
            {
                return this.isHighScore;
            }
            set
            {
                if (this.isHighScore != value)
                {
                    this.isHighScore = value;
                    RaisePropertyChanged("IsHighScore");
                }
            }
        }
        
        public string Name
        {
            get 
            {
                return this.name;
            }
            set
            {
                if (this.name != value)
                {
                    this.name = value;
                    RaisePropertyChanged("Name");
                }
            }
        }

        public void Show(string message, Action<string> callback, bool isHighScore=false)
        { 
            this.Message = message;
            this.IsHighScore = isHighScore ? Visibility.Visible : Visibility.Collapsed;
            this.callback = callback;
            this.Visibility = Visibility.Visible;
        }
    }
}
