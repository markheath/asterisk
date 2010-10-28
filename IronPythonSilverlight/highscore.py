
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
        isf = IsolatedStorageFile.GetUserStoreForApplication()
        try:                
            isfs = IsolatedStorageFileStream(filename, FileMode.Create, isf)
            try:
                sw = StreamWriter(isfs)
                try:
                    sw.Write(data)
                finally:
                    sw.Dispose()
            finally:
                isfs.Dispose()
        finally:
            isf.Dispose()

    def LoadHighScore(self):
        filename = "record.txt"
        isf = IsolatedStorageFile.GetUserStoreForApplication()
        try:
            if not isf.FileExists(filename):
                return
            isfs = IsolatedStorageFileStream(filename, FileMode.Open, isf)
            try:
                sr = StreamReader(isfs)
                try:
                    record = sr.ReadLine()
                    parts = record.split(':')
                    if(len(parts) == 2):
                        self.Level = int(parts[0])
                        self.Name = parts[1]
                finally:
                    sr.Dispose()
            finally:
                isfs.Dispose()
        finally:
            isf.Dispose()
        pass #TODO: implement using isolated store