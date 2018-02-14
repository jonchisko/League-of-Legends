

#Class that read desired data
import pandas as pd
import pickle

class ReadData:

    def __init__(self, path, *args, **kwargs):
        self.path = path
        self.dataFiles = {}
        self.startRow = 0
        self.endRow = -1
        if "read" in kwargs:
            if kwargs["read"]:
                for fileName in args:
                    self.readData(fileName)
            else:
                for fileName in args:
                    actualPath = path+'/'+fileName+".csv"
                    self.dataFiles[fileName] = pd.read_csv(actualPath, encoding="latin1")
        else:
            raise AttributeError("Missing read argument")
        if "startRow" in kwargs:
            self.startRow = kwargs["startRow"]
        if "endRow" in kwargs:
            self.endRow = kwargs["endRow"]


    def saveData(self, fileName):
        pickle.dump(self.dataFiles[fileName], fileName+"Saved")


    def readData(self, fileName):
        self.dataFiles[fileName] = pickle.load(self.path+'/'+fileName)


    def returnDataFrame(self, fileName):
        dataFrame = self.dataFiles[fileName]
        if self.endRow == -1:
            selection = dataFrame.iloc[self.startRow:]
        else:
            selection = dataFrame.iloc[self.startRow:self.endRow]
        return selection



