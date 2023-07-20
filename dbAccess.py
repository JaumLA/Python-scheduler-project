import pickle
from dayOfWeek import DayOfWeek
import os 

GENERALERROR = "Something went wrong."

class Database:

    @staticmethod
    def getTask() -> dict:
        schedule = dict()
        try:
            fd = os.open(path="./testTestData.json", flags=os.O_CREAT|os.O_RDONLY)
            with os.fdopen(fd, "rb") as seriaBin:
                dnk = pickle.load(seriaBin)
                for x in DayOfWeek:
                    schedule[x.value] = dnk[x.value]
        except PermissionError as err:
            print(err.strerror)
        except EOFError:
            for x in DayOfWeek:
                schedule[x.value] = []
        except BaseException:
            print(GENERALERROR)
            for x in DayOfWeek:
                schedule[x.value] = []
        finally:
            return schedule

    @staticmethod
    def writeToFile(schedule: dict):
        try:
            with open(file="./testTestData.json", mode='wb') as file:
                pickle.dump(schedule, file=file)
        except PermissionError as err:
            print(err.strerror)
        except EOFError:
            print("Can't save changes: File deleted.")
        except BaseException:
            print(GENERALERROR)    
            return -1