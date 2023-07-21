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
        self.labelFrame = ttk.Labelframe(parent, text="Actual Task")
        self.remainingTime = Variable()
        self.schedule = GuiLogic.getTasksDay(self.getActualWeek())
        self._createLabelFrame(parent)

    def _createLabelFrame(self, parent: Misc):
        self.labelFrame = ttk.Labelframe(parent, text="Actual Task")
        nameLabel = ttk.Label(self.labelFrame, text="Name")
        nameLabel.place(relx=0.05, rely=1, relheight=1,
                        relwidth=0.30, anchor='sw')

        reaminingLabel = ttk.Label(
            self.labelFrame, textvariable=self.remainingTime)
        reaminingLabel.place(relx=0.6, rely=1, relheight=0.14,
                             relwidth=0.3, anchor="sw")

    def getLabelFrame(self):
        return self.labelFrame

    def getActualWeek(self) -> int:
        return datetime.now().weekday()

    def getActualName(self) -> str:
        return ""

    def loop(self):
        remaining = 0
        actualTask = None
        while True:
            asyncio.run(asyncio.sleep(1))
            print(self.findActualTask())


    def findActualTask(self):
        weekDay = self.getActualWeek()
        timeNow = datetime.now().time()
        hoursNow = ActualTaskFrame.timeToHours(timeNow)
        for task in GuiLogic.getTasksDay(weekDay):
            taskBeginTime = ActualTaskFrame.timeToHours(task["begin"])
            taskEndTime = ActualTaskFrame.timeToHours(task["end"])
            if((hoursNow - taskBeginTime) >= 0 and (hoursNow - taskEndTime) >= 0):
                return task
    
    @staticmethod
    def timeToHours(time: time):
        return time.hour + time.minute/60 + time.second/3600