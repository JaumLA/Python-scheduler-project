from datetime import time
import random
from dbAccess import Database

from tkinter import Variable


class GuiLogic:

    db = Database()

    @classmethod
    def getTasksDay(cls, dayNum: int) -> list:
        daySchedule = cls.db.getDaySchedule(dayNum)
        return sorted(daySchedule, key=lambda x: (cls._createTuple(x)))

    @staticmethod
    def _createTuple(val):
        return (val["begin"].hour, val["begin"].minute, val["end"].hour, val["end"].minute)

    @classmethod
    def addTask(cls, tname: Variable, beginTimeStr: Variable, endTimeStr: Variable, dayNum: int):
        """Take the name, begin time and end time as str value."""
        beginSplit = beginTimeStr.get().split(":")
        if(len(beginSplit) == 1 or beginSplit[1] == ''):
            beginMinute = 0
        else:
            beginMinute = int(beginSplit[1])
        beginTime = time(int(beginSplit[0]), beginMinute)

        endSplit = endTimeStr.get().split(":")
        if(len(endSplit) == 1 or endSplit[1] == ''):
            endMinute = 0
        else:
            endMinute = int(endSplit[1])
        endTime = time(int(endSplit[0]), endMinute)

        task = dict(
            id=f"{random.randint(0, 100000)}",
            name=tname.get(),
            begin=beginTime,
            end=endTime
        )
        cls.db.addTask(task, dayNum)

    @classmethod
    def changeTaskName(cls, newName: str):
        pass

    @classmethod
    def removeTask(cls, task, dayNum: int):
        """Given the task and the number of the weekday, delete the task."""
        cls.db.removeTask(task, dayNum)

    @classmethod
    def saveFile(cls):
        cls.db.writeToFile()

    @staticmethod
    def moveTask():
        pass
