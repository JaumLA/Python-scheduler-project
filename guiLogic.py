from datetime import time
import random
from dbAccess import Database

from tkinter import Variable

from typing import Union

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
    def addTask(cls, tname: Variable, beginTimeVar: Variable, endTimeVar: Variable, dayNum: int) -> int:
        """Take the name, begin time and end time as str value.\n
        Return -1 if the task isn't added, 0 otherwise."""

        beginTime = cls.variableToTime(beginTimeVar.get())
        endTime = cls.variableToTime(endTimeVar.get())

        if(beginTime == None or endTime == None):
            return -1

        task = dict(
            id=f"{random.randint(0, 100000)}",
            name=tname.get(),
            begin=beginTime,
            end=endTime
        )
        cls.db.addTask(task, dayNum)
        return 0

    @staticmethod
    def variableToTime(strTime: str) -> Union[time, None]:
        try:
            timeSplit = strTime.split(":")
            if(len(timeSplit) == 1 or timeSplit[1] == ''):
                timeMinute = 0
            else:
                timeMinute = int(timeSplit[1])
            convertedTime = time(int(timeSplit[0]), timeMinute)
            return convertedTime
        except ValueError:
            print(TIMERANGEERROR)
            return None
        except BaseException:
            print(GENERALERROR)
            return None

    @classmethod
    def changeTaskInfo(cls, newNameVar: Variable, newBeginVar: Variable, newEndVar: Variable, oldTask: dict, dayNum: int):
        newName = newNameVar.get()
        newBeginTime = cls.variableToTime(newBeginVar.get())
        newEndTime = cls.variableToTime(newEndVar.get())
        if(newBeginTime == None or newEndTime == None):
            return -1

        newTask = dict(
            id=oldTask["id"],
            name=newName,
            begin=newBeginTime,
            end=newEndTime
        )
        cls.db.updateTask(newTask, dayNum)

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
