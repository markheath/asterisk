
class HighScore:
    def __init__(self):
        self.Level = 0
        self.Name = 'Nobody'
        self.LoadHighScore()

    def getMessage(self):
        return 'Level {0} by {1}'.format(self.Level, self.Name)

    Message = property(getMessage)

    def Save(self):
        pass #TODO: implement using isolated store

    def LoadHighScore(self):
        pass #TODO: implement using isolated store