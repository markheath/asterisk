using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Input;

namespace Asterisk
{
    class RelayCommand : ICommand
    {
        Action executeAction;
        private bool canExecute;

        public RelayCommand(Action executeAction)
        {
            this.executeAction = executeAction;
            this.canExecute = true;
        }

        public bool CanExecute(object parameter)
        {
            return this.canExecute;
        }

        public void SetCanExecute(bool value)
        {
            if (this.canExecute != value)
            {
                this.canExecute = value;
                if (CanExecuteChanged != null)
                {
                    this.CanExecuteChanged(this, EventArgs.Empty);
                }
            }
        }

        public event EventHandler CanExecuteChanged;

        public void Execute(object parameter)
        {
            this.executeAction();
        }
    }
}
