import clr
clr.AddReference("PresentationFramework")
clr.AddReference("PresentationCore")
 
from System import EventArgs
from System.IO import File
from System.Windows.Markup import XamlReader
from System.Windows.Media import VisualTreeHelper, HitTestResultCallback, PointHitTestParameters, HitTestResultBehavior, HitTestFilterBehavior
 
class XamlLoader(object):
    def __init__(self, xamlPath):
        stream = File.OpenRead(xamlPath)
        self.Root = XamlReader.Load(stream)
         
    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        return self.Root.FindName(item)
        
from System.ComponentModel import INotifyPropertyChanged
from System.ComponentModel import PropertyChangedEventArgs
 
class ViewModelBase(INotifyPropertyChanged):
    def __init__(self):
        self.propertyChangedHandlers = []
 
    def RaisePropertyChanged(self, propertyName):
        args = PropertyChangedEventArgs(propertyName)
        for handler in self.propertyChangedHandlers:
            handler(self, args)
             
    def add_PropertyChanged(self, handler):
        self.propertyChangedHandlers.append(handler)
         
    def remove_PropertyChanged(self, handler):
        self.propertyChangedHandlers.remove(handler)
        
from System.Windows.Input import ICommand
 
class Command(ICommand):
    def __init__(self, execute, canExecute = True):
        self.execute = execute
        self.canExecute = canExecute
        self.canExecuteChangedHandlers = []
     
    def Execute(self, parameter):
        self.execute()
         
    def add_CanExecuteChanged(self, handler):
        self.canExecuteChangedHandlers.append(handler)
     
    def remove_CanExecuteChanged(self, handler):
        self.canExecuteChangedHandlers.remove(handler)
        
    def RaiseCanExecuteChanged(self):
        for handler in self.canExecuteChangedHandlers:
            handler(self, EventArgs.Empty)
 
    def CanExecute(self, parameter):
        return self.canExecute

# WPF Check Collision function
def CheckCollisionPoint(point, control):
    hits = []
    def callbackFunc(hit):
        hits.append(hit.VisualHit)
        return HitTestResultBehavior.Stop
    callback = HitTestResultCallback(callbackFunc)
    VisualTreeHelper.HitTest(control, None, callback,
        PointHitTestParameters(point))    
    return len(hits) > 0



from System.Windows import Application
  
def RunApp(rootElement):
    app = Application()
    app.Run(rootElement)