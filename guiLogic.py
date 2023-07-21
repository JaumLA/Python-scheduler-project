from datetime import time
import random
from dbAccess import Database

from tkinter import Variable

from typing import Union

TIMERANGEERROR = """The minute must be in range [0-59] inclusive and the hour must be in range [0-24] inclusive."""
GENERALERROR = "Something went wrong."


class GuiLogic:

    _schedule = Database.getTask()

    @classmethod
    def getTasksDay(cls, dayNum: int) -> list:
        daySchedule = cls._schedule[dayNum]
        return sorted(daySchedule, key=lambda x: (cls._createTuple(x)))

    @classmethod
    def getSchedule(cls):
        return cls._schedule

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
        cls._schedule[dayNum].append(task)
        return 0

    @staticmethod
    def variableToTime(strTime: str) -> Union[time, None]:
        try:
            timeSplit = strTime.split(":")
            if(len(timeSplit) == 1 or timeSplit[1] == ''):
                timeMinute = 0
            else:
                timeMinute = int(timeSplit[1])
            convertedTime = time(hour=int(timeSplit[0]), minute=timeMinute)
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

        pos = cls.findTaskPosAtWeekday(oldTask, dayNum)
        if(pos == -1):
            return -1
        cls._schedule[dayNum][pos] = newTask

    @classmethod
    def findTaskPos(cls, taskToFind: dict):
        pos = None
        for daySchedule in cls._schedule:
            pos = next((i for i, task in enumerate(daySchedule)
                       if task["id"] == taskToFind["id"]), None)
            if(pos != None):
                return daySchedule[pos]

        return -1

    @classmethod
    def findTaskPosAtWeekday(cls, taskToFind, dayNum):
        daySchedule = cls._schedule[dayNum]
        pos = next((i for i, task in enumerate(daySchedule)
                    if task["id"] == taskToFind["id"]), None)
        if(pos == None):
            return -1
        else:
            return pos

    @classmethod
    def removeTask(cls, task: dict, dayNum: int):
        """Given the task and the number of the weekday, delete the task."""
        try:
            cls._schedule[dayNum].remove(task)
        except ValueError:
            print("Task already removed.")
        except BaseException:
            print(GENERALERROR)
            return -1

    @classmethod
    def saveFile(cls):
        Database.writeToFile(cls._schedule)

    @staticmethod
    def moveTask():
        pass
