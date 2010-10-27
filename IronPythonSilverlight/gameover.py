import clr
import mvvm
from System.Windows import Visibility
from System.Net import WebClient
from System import Uri, UriKind

class GameOver:
    def __init__(self,loaded):
        self.loaded = loaded
        wc = WebClient()
        wc.DownloadStringCompleted += self.xamlDownloaded
        wc.DownloadStringAsync(Uri('gameover.xaml',UriKind.Relative))
        self.viewModel = GameOverViewModel()
        
    def xamlDownloaded(self, sender, args):
        if not args.Error:
            self.xaml = mvvm.XamlLoader(args.Result)
            self.xaml.Root.DataContext = self.viewModel
            self.xaml.Root.Visibility = Visibility.Collapsed
            #callback
            self.loaded(self.xaml.Root)
    
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