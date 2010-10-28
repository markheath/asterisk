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
            <TextBlock x:Name="labelMessage" Foreground="White" FontSize="16" HorizontalAlignment="Center" />
            <StackPanel x:Name="highScorePanel" Orientation="Horizontal">
                <TextBlock 
                    FontSize="12" 
                    Foreground="White"
                    Text="Enter your name:" 
                    Margin="5" />
                <TextBox 
                    x:Name="textBoxName"
                    Width="150" 
                    MaxLength="20" 
                    Margin="5" />
            </StackPanel>
            <Button 
                FontSize="12" 
                Content="OK" 
                x:Name="buttonOK"
                HorizontalAlignment="Center"
                Margin="5"
                Width="50" />
    </StackPanel>
</Border>"""
    
    def __init__(self,loaded):
        self.loaded = loaded
        self.xaml = mvvm.XamlLoader(self.gameOverXaml)
        self.xaml.Root.Visibility = Visibility.Collapsed
        self.xaml.buttonOK.Click += self.onOK
        loaded(self.xaml.Root)

    def onOK(self, sender, args):
        if self.callback:
            self.callback(self.xaml.textBoxName.Text)
            
    def Show(self, message, callback, isHighScore=False):
        self.xaml.labelMessage.Text = message
        self.xaml.highScorePanel.Visibility = Visibility.Visible if isHighScore else Visibility.Collapsed
        self.xaml.Root.Visibility = Visibility.Visible
        self.callback=callback