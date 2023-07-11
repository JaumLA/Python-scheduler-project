import re
from tkinter import Misc, Variable, ttk
from tkinter import Tk
from tkinter import Toplevel

from guiLogic import *
from dayOfWeek import DayOfWeek

import abc


class MainFrame:
    """Has the main root TK and the main Frame."""

    def __init__(self) -> None:
        self._createRoot()
        self._createMainFrame()
        self._root.mainloop()
        pass

    def _createRoot(self) -> None:
        self._root = Tk()
        self._root.title("Scheduler")
        self._root.geometry("600x400")
        self._root.minsize(width=500, height=400)
        self._root.columnconfigure(0, weight=1)
        self._root.rowconfigure(0, weight=1)

    def _createMainFrame(self) -> None:
        self._mainFrame = ttk.Frame(self._root)
        self._mainFrame.grid(column=0, row=0, sticky="NESW")
        self._mainFrame.grid_columnconfigure(index=0, weight=1)
        self._mainFrame.grid_rowconfigure(index=0, weight=1)
        self._noteDays = NotebookDays(self._mainFrame)


class NotebookDays(ttk.Notebook):
    """The NotebookDays tabs represents the week days"""

    def __init__(self, parent: Misc) -> None:
        ttk.Notebook.__init__(self, parent)
        self._tabs = dict()
        self._addFrames = dict()
        self._createNoteDays()

    def _createNoteDays(self) -> None:
        """Create the Notebook ttk and add the 7 tabs and its
        frames to hold the tasks."""
        self.config(width=600, height=400, padding="5")
        self.grid(sticky="NESW")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        days = DayOfWeek.getDaysName()
        for day in days:
            dayNum = DayOfWeek[day].value
            tab = self._createNoteTab(dayNum)
            self._tabs.update({dayNum: tab})
            self.add(tab, text=day)

    def _createNoteTab(self, dayNum: int) -> ttk.Frame:
        """Create a ttk Frame"""
        tab = ttk.Frame(self, padding="4")
        self._tabs.update({dayNum: tab})
        self.fillTab(dayNum)

        addButton = ttk.Button(tab, name="addButton", text="+ add task",
                               command=lambda: self._addFrameCommand(dayNum))
        addButton.place(relx=1, rely=1, anchor="se")

        return tab

    def fillTab(self, dayNum: int) -> None:
        """Get the tasks from GuiLogic and format to the tab[dayNum]."""
        taskList = GuiLogic.getTasksDay(dayNum)
        tab = self._tabs[dayNum]
        ypos = 1
        for task in taskList:
            taskLabel = TaskLabel(self, tab, ypos)
            taskLabel.create(task, dayNum)
            ypos += 1

    def destroyTasks(self, dayNum: int):
        """Destroy all the labels with the tasks and only leave the
        add button and the Frame."""
        for widget in self._tabs[dayNum].winfo_children():
            if (widget.winfo_name() == "addButton"):
                continue
            widget.destroy()

    def _addFrameCommand(self, dayNum: int) -> None:
        """The command to open the frame to add tasks."""

        # Keep only one instance open.
        if(self._addFrames.get(dayNum) == None):
            addFrame = AddFrame("+ add task", self, dayNum)
            addFrame.open(dayNum)
            self._addFrames.update({dayNum: addFrame})
        else:
            self._addFrames.get(dayNum).open(dayNum)


class FormFrame(metaclass=abc.ABCMeta):
    LABELNAMERELWIDTH = 0.5
    LABELNAMERELX = 0.5
    LABELNAMERELY = 0.15

    LABELHEIGHT = 33
    LABELRELWIDTH = 0.25
    LABELRELX = 0.20
    LABELRELY = 0.40

    ENTRYRELHEIGHT = 1
    ENTRYRELWIDTH = 0.98
    ENTRYRELX = 0.01

    def __init__(self, buttonName: str, noteBook: NotebookDays, dayNum: int, taskName="",
                 beginTime="", endTime="", ) -> None:
        self.frame = None
        self.noteBook = noteBook
        self.taskName = Variable()
        self.taskName.set(taskName)
        self.beginTime = Variable()
        self.beginTime.set(beginTime)
        self.endTime = Variable()
        self.endTime.set(endTime)
        self.buttonName = buttonName
        self.dayNum = dayNum

    def open(self, dayNum: int) -> None:
        """Create the Frame if it's None, else it's already open."""
        if(self.frame == None):
            self._createFrame(dayNum)

    def _createFrame(self, dayNum: int) -> None:
        """Fill the Frame with the form widgets."""
        self.frame = Toplevel(width=400, height=200, padx=4, pady=4)
        self.frame.protocol('WM_DELETE_WINDOW', self._closeframeFrame)

        nameLabel = ttk.Labelframe(self.frame, text="Task Name")
        nameLabel.place(anchor='center', relwidth=self.LABELNAMERELWIDTH,
                        height=self.LABELHEIGHT, relx=self.LABELNAMERELX, rely=self.LABELNAMERELY)

        nameEntry = ttk.Entry(
            nameLabel, textvariable=self.taskName)
        nameEntry.place(relheight=self.ENTRYRELHEIGHT,
                        relwidth=self.ENTRYRELWIDTH, relx=self.ENTRYRELX)

        beginHourLabel = ttk.Labelframe(self.frame, text="Begin time")
        beginHourLabel.place(anchor='w', relwidth=self.LABELRELWIDTH,
                             height=self.LABELHEIGHT, relx=self.LABELRELX, rely=self.LABELRELY)

        beginHourEntry = ttk.Entry(beginHourLabel, textvariable=self.beginTime)
        beginHourEntry.config(validate='key', validatecommand=(
            beginHourEntry.register(self._validateTime), '%d', '%P', '%S'))
        beginHourEntry.place(relheight=self.ENTRYRELHEIGHT,
                             relwidth=self.ENTRYRELWIDTH, relx=self.ENTRYRELX)

        endHourLabel = ttk.Labelframe(self.frame, text="End time")
        endHourLabel.place(anchor='e', relwidth=self.LABELRELWIDTH,
                           height=self.LABELHEIGHT, relx=self.LABELRELX * 4, rely=self.LABELRELY)

        endHourEntry = ttk.Entry(endHourLabel, textvariable=self.endTime)
        endHourEntry.config(validate='key', validatecommand=(
            endHourEntry.register(self._validateTime), '%d', '%P', '%S'))
        endHourEntry.place(relheight=self.ENTRYRELHEIGHT,
                           relwidth=self.ENTRYRELWIDTH, relx=self.ENTRYRELX)

        button = ttk.Button(self.frame, name="button", text=self.buttonName,
                            command=lambda: self._buttonCommand(dayNum))
        button.place(relx=1, rely=1, anchor="se")

    def _validateTime(self, d, p: str, S):
        """Accept only numbers, the delete operation and the char ':'"""
        result = False
        if(d == '0'):
            result = True
        elif(len(p) == 2 and S == ":"):
            result = True
        elif(len(p) == 3 and S == ':'):
            result = True
        elif(re.fullmatch("[0-9]{1,2}|[0-9]{1,2}[:][0-9]{1,2}", p) != None):
            result = True
        return result

    @abc.abstractmethod
    def _buttonCommand(self, dayNum: int) -> None:
        """Take the entries of the form and pass it to 
        frameTaks function of the GuiLogic class."""

    def _closeframeFrame(self) -> None:
        """When the frame is closed, destroy it and reset the entries."""
        if(self.frame == None):
            return
        self.frame.destroy()
        self.frame = None
        self._resetEntries()

    def _resetEntries(self):
        self.beginTime.set('')
        self.endTime.set('')
        self.taskName.set('')


class AddFrame(FormFrame):
    def _buttonCommand(self, dayNum: int) -> None:
        if(GuiLogic.addTask(self.taskName, self.beginTime,
                            self.endTime, dayNum) == 0):
            self._resetEntries()
            self.noteBook.destroyTasks(dayNum)
            self.noteBook.fillTab(dayNum)


class UpdateFrame(FormFrame):
    def _buttonCommand(self, dayNum: int) -> None:
        pass

class TaskLabel(ttk.LabelFrame):

    RELX = 0.01
    RELY = 0.14
    RELHEIGHT = 0.13
    RELWIDTH = 0.98

    def __init__(self, notebook: NotebookDays, parent: Misc, ypos: int) -> None:
        ttk.LabelFrame.__init__(self, parent)
        self._notebook = notebook
        self.ypos = ypos

    def create(self, task: dict, dayNum: int):
        """Create the labels for the task info and button actions."""
        self.config(border=1, text=task["name"], labelanchor="nw", padding="4")

        self.place(relx=self.RELX, rely=self.RELY * self.ypos,
                   relheight=self.RELHEIGHT, relwidth=self.RELWIDTH, anchor="w")

        l = ttk.Label(
            self, text=f"{task['begin']} - {task['end']}", anchor="w")
        l.place(relx=0, rely=0)

        self._createTaskConfigButton(task, dayNum)
        self._createRemoveButton(task, dayNum)

    def _createRemoveButton(self, task: dict, dayNum: int):
        removeButton = ttk.Button(self, name="removeButton", text="R",
                                  command=lambda: self._removeButtonCommand(task, dayNum))
        removeButton.place(relx=0.95, rely=0,
                           relwidth=0.05, relheight=1)

    def _removeButtonCommand(self, task: dict, dayNum: int):
        GuiLogic.removeTask(task, dayNum)
        self.destroy()
        self._notebook.destroyTasks(dayNum)
        self._notebook.fillTab(dayNum)

    def _createTaskConfigButton(self, task: dict, dayNum: int):
        button = ttk.Button(self, name="taskConfigButton", text="MOVE")
        button.place(relx=0.90, relwidth=0.05, relheight=1)
        button.config(command=lambda: task)
