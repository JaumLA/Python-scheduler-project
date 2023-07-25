from typing import Union
from datetime import datetime
from datetime import time
from guiLogic import GuiLogic

from tkinter import Misc
from tkinter import Variable
from tkinter import ttk

import asyncio


class ActualTaskFrame:

    def __init__(self, parent: Misc) -> None:
        self.parent = parent
        self.keepAlive = True
        self.labelFrame = ttk.Labelframe(parent, text="Actual Task")
        self.remainingTime = Variable()
        self.taskName = Variable()
        self._createLabelFrame(parent)

    def _createLabelFrame(self, parent: Misc):
        self.labelFrame = ttk.Labelframe(parent, text="Actual Task")
        nameLabel = ttk.Label(self.labelFrame, textvariable=self.taskName)
        nameLabel.place(relx=0.05, rely=1, relheight=1,
                        relwidth=0.30, anchor='sw')

        reaminingLabel = ttk.Label(
            self.labelFrame, textvariable=self.remainingTime)
        reaminingLabel.place(relx=0.43, rely=1, relheight=1,
                             relwidth=0.5, anchor="sw")

    def getLabelFrame(self):
        return self.labelFrame

    def getActualWeek(self) -> int:
        return datetime.now().weekday()

    def loop(self):
        actualTask = None
        while True:
            if(not self.keepAlive):
                return
            actualTask = self.findActualTask()
            if(actualTask != None):
                self.updateLabelVar(actualTask)
            asyncio.run(asyncio.sleep(1))

    def updateLabelVar(self, task: dict):
        self.taskName.set(task["name"])
        endtimeHours = ActualTaskFrame.timeToHours(task["end"])
        timeNowHours = ActualTaskFrame.timeToHours(datetime.now().time())
        seconds = (endtimeHours - timeNowHours)*3600
        self.remainingTime.set(f"Remaining time: {int(seconds/3600)}:{int(seconds/60)%60}:{int(seconds%60)}")

    def findActualTask(self) -> Union[None, dict]:
        weekDay = self.getActualWeek()
        timeNow = datetime.now().time()
        hoursNow = ActualTaskFrame.timeToHours(timeNow)
        for task in GuiLogic.getTasksDay(weekDay):
            taskBeginTime = ActualTaskFrame.timeToHours(task["begin"])
            taskEndTime = ActualTaskFrame.timeToHours(task["end"])
            if((hoursNow - taskBeginTime) >= 0 and (taskEndTime - hoursNow) >= 0):
                return task

    def stop(self):
        self.keepAlive = False

    @staticmethod
    def timeToHours(time: time):
        return time.hour + time.minute/60 + time.second/3600
