import os

class HighScore:
    def __init__(self):
        self.Level = 0
        self.Name = 'Nobody'
        self.LoadHighScore()

    def getMessage(self):
        return 'Level {0} by {1}'.format(self.Level, self.Name)

    Message = property(getMessage)

    def Save(self):
        f = open('record.txt', 'w')
        f.write('{0}:{1}'.format(self.Level, self.Name))

    def LoadHighScore(self):
        if os.path.isfile('record.txt'):
            record = open('record.txt').readline()
            parts = record.split(':')
            if(len(parts) == 2):
                self.Level = int(parts[0])
                self.Name = parts[1]