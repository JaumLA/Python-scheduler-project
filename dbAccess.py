import pickle
from dayOfWeek import DayOfWeek
import os 

GENERALERROR = "Something went wrong."

class Database:

    def __init__(self):
        self.schedule = dict()
        try:
            fd = os.open(path="./testTestData.json", flags=os.O_CREAT|os.O_RDONLY)
            with os.fdopen(fd, "rb") as seriaBin:
                dnk = pickle.load(seriaBin)
                for x in DayOfWeek:
                    self.schedule[x.value] = dnk[x.value]
        except PermissionError as err:
            print(err.strerror)
        except EOFError:
            for x in DayOfWeek:
                self.schedule[x.value] = []
        except BaseException:
            print(GENERALERROR)
            for x in DayOfWeek:
                self.schedule[x.value] = []

    def getDaySchedule(self, dayNum: int):
        return self.schedule[dayNum]

    def addTask(self, task: dict, dayNum: int):
        self.schedule[dayNum].append(task)

    def removeTask(self, task: dict, day: int):
        try:
            self.schedule[day].remove(task)
        except ValueError:
            print("Task already removed.")
        except BaseException:
            print(GENERALERROR)    
            return -1

    def writeToFile(self):
        try:
            with open(file="./testTestData.json", mode='wb') as file:
                pickle.dump(self.schedule, file=file)
        except PermissionError as err:
            print(err.strerror)
        except EOFError:
            print("Can't save changes: File deleted.")
        except BaseException:
            print(GENERALERROR)    
            return -1