from datetime import time
import random
from dbAccess import Database

from tkinter import Variable

TIMERANGEERROR = """The minute must be in range [0-59] inclusive and the hour must be in range [0-24] inclusive."""
GENERALERROR = "Something went wrong."

class GuiLogic:

    db = Database()

    @classmethod
    def getTasksDay(cls, dayNum: int) -> list:
        daySchedule = cls.db.getDaySchedule(dayNum)
        return sorted(daySchedule, key=lambda x: (cls._createTuple(x)))

    @staticmethod
    def _createTuple(val):
        try:
            return (val["begin"].hour, val["begin"].minute, val["end"].hour, val["end"].minute)
        except KeyError:
            print("Some tasks are missing the times.")
            return (0, 0, 0, 0)
        except BaseException:
            print(GENERALERROR)
            return (0, 0, 0, 0)

    @classmethod
    def addTask(cls, tname: Variable, beginTimeStr: Variable, endTimeStr: Variable, dayNum: int) -> int:
        """Take the name, begin time and end time as str value.\n
        Return -1 if the task isn't added, 0 otherwise."""

        try:
            beginSplit = beginTimeStr.get().split(":")
            if(len(beginSplit) == 1 or beginSplit[1] == ''):
                beginMinute = 0
            else:
                beginMinute = int(beginSplit[1])
            beginTime = time(int(beginSplit[0]), beginMinute)
        except ValueError:
            print(TIMERANGEERROR)
            return -1
        except BaseException:
            print(GENERALERROR)    
            return -1
        
        try:
            endSplit = endTimeStr.get().split(":")
            if(len(endSplit) == 1 or endSplit[1] == ''):
                endMinute = 0
            else:
                endMinute = int(endSplit[1])
            endTime = time(int(endSplit[0]), endMinute)
        except ValueError:
            print(TIMERANGEERROR)
            return -1
        except BaseException:
            print(GENERALERROR)    
            return -1

        task = dict(
            id=f"{random.randint(0, 100000)}",
            name=tname.get(),
            begin=beginTime,
            end=endTime
        )
        cls.db.addTask(task, dayNum)
        return 0

    @classmethod
    def changeTaskName(cls, newName: str):
        pass

    @classmethod
    def removeTask(cls, task: dict, dayNum: int):
        """Given the task and the number of the weekday, delete the task."""
        cls.db.removeTask(task, dayNum)

    @classmethod
    def saveFile(cls):
        cls.db.writeToFile()

    @staticmethod
    def moveTask():
        pass
