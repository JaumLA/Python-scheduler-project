import pickle
from dayOfWeek import DayOfWeek


class Database:

    def __init__(self):
        self.schedule = dict()
        with open(file="./testTestData.json", mode='rb') as seriaBin:
            dnk = pickle.load(seriaBin)
            for x in DayOfWeek:
                self.schedule[x.value] = dnk[x.value]

    def getDaySchedule(self, dayNum: int):
        return self.schedule[dayNum]

    def addTask(self, task, dayNum: int):
        self.schedule[dayNum].append(task)

    def removeTask(self, task, day: int):
        self.schedule[day].remove(task)

    def writeToFile(self):
        with open(file="./testTestData.json", mode='wb') as file:
            pickle.dump(self.schedule, file=file)
