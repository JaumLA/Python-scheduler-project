from enum import Enum


class DayOfWeek(Enum):
    SUNDAY = 0
    MONDAY = 1
    TUESDAY = 2 
    WEDNESDAY = 3 
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6

    @staticmethod
    def getDaysName() -> list:
        return [x.name for x in DayOfWeek]
