using System;
using System.IO;
using System.IO.IsolatedStorage;

namespace Asterisk
{
    public class HighScore
    {
        public int Level { get; set; }
        public string Name { get; set; }
        private static readonly string filename = "record.txt";

        public HighScore()
        {
            Level = 0;
            Name = "Nobody";
            LoadHighScore();
        }

        public string Message
        {
            get
            {
                return String.Format("Level {0} by {1}", this.Level, this.Name);
            }
        }

        public void Save()
        {
            
            string data = String.Format("{0}:{1}",this.Level,this.Name);
            using (var isf = IsolatedStorageFile.GetUserStoreForApplication())
            {
                using (var isfs = new IsolatedStorageFileStream(filename, FileMode.Create, isf))
                {
                    using (var sw = new StreamWriter(isfs))
                    {
                        sw.Write(data);
                    }
                }
            }
        }

        private void LoadHighScore()
        {
            using (var isf = IsolatedStorageFile.GetUserStoreForApplication())
            {
                if (!isf.FileExists(filename))
                {
                    return;
                }

                using (var isfs = new IsolatedStorageFileStream(filename, FileMode.Open, isf))
                {
                    using (var sr = new StreamReader(isfs))
                    {
                        var record = sr.ReadLine();
                        var parts = record.Split(':');
                        if (parts.Length == 2)
                        {
                            this.Level = int.Parse(parts[0]);
                            this.Name = parts[1];
                        }
                    }
                }
            }
        }
    }
}
