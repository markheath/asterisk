import clr
import mvvm
from System.Windows import Visibility

class GameOver:
    gameOverXaml = """<Border
    xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
    xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
    Width="300"
    Background="Black"
    BorderBrush="White"
    BorderThickness="2"
    CornerRadius="5">
        <StackPanel Orientation="Vertical">
            <TextBlock Foreground="White" FontSize="16" Text="{Binding Message}" HorizontalAlignment="Center" />
            <StackPanel Visibility="{Binding IsHighScore}" Orientation="Horizontal">
                <TextBlock 
                    FontSize="12" 
                    Foreground="White"
                    Text="Enter your name:" 
                    Margin="5" />
                <TextBox 
                    Text="{Binding Name, Mode=TwoWay}" 
                    Width="150" 
                    MaxLength="20" 
                    Margin="5" />
            </StackPanel>
            <Button 
                FontSize="12" 
                Content="OK" 
                Command="{Binding OKCommand}" 
                HorizontalAlignment="Center"
                Margin="5"
                Width="50" />
    </StackPanel>
</Border>"""
    
    def __init__(self,loaded):
        self.loaded = loaded
        self.viewModel = GameOverViewModel()
        self.xaml = mvvm.XamlLoader(self.gameOverXaml)
        self.xaml.Root.DataContext = self.viewModel
        self.xaml.Root.Visibility = Visibility.Collapsed
        loaded(self.xaml.Root)
            
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