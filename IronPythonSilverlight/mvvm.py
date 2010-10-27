import clr
 
from System import EventArgs
from System.Windows.Media import VisualTreeHelper
from System.Windows.Markup import XamlReader

from System.ComponentModel import INotifyPropertyChanged
from System.ComponentModel import PropertyChangedEventArgs

class XamlLoader(object):
    def __init__(self, xaml):
        try:
            self.Root = XamlReader.Load(xaml)
        except SystemError, e:
            print 'Error parsing xaml: {0}'.format(xaml)
            raise e

    def __getattr__(self, item):
        """Maps values to attributes.
        Only called if there *isn't* an attribute with this name
        """
        return self.Root.FindName(item)
 
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

# Silverlight Check Collision function
def CheckCollisionPoint(point, control):
    #MRH: not sure why this is coming through as identity, but Inverse is calculated as None
    #for a MatrixTransform
    inverse = control.RenderTransform.Inverse
    if not inverse:
        transformPoint = point
    else:
        transformPoint = inverse.Transform(point)
    hits = VisualTreeHelper.FindElementsInHostCoordinates(transformPoint, control)
    return hits.Contains(control)