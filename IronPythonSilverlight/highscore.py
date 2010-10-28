
from System.IO import FileMode, StreamWriter, StreamReader
from System.IO.IsolatedStorage import IsolatedStorageFile, IsolatedStorageFileStream

class HighScore:
    def __init__(self):
        self.Level = 0
        self.Name = 'Nobody'
        self.LoadHighScore()

    def getMessage(self):
        return 'Level {0} by {1}'.format(self.Level, self.Name)

    Message = property(getMessage)

    def Save(self):
        filename = "record.txt"
        data = "{0}:{1}".format(self.Level,self.Name)
        with IsolatedStorageFile.GetUserStoreForApplication() as isf:
            with IsolatedStorageFileStream(filename, FileMode.Create, isf) as isfs:
                with StreamWriter(isfs) as sw:
                    sw.Write(data)

    def LoadHighScore(self):
        filename = "record.txt"
        with IsolatedStorageFile.GetUserStoreForApplication() as isf:
            if not isf.FileExists(filename):
                return
            with IsolatedStorageFileStream(filename, FileMode.Open, isf) as isfs:
                with StreamReader(isfs) as sr:
                    record = sr.ReadLine()
                    parts = record.split(':')
                    if(len(parts) == 2):
                        self.Level = int(parts[0])
                        self.Name = parts[1]        