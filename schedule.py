from time import sleep
from datetime import datetime

class Scheduler:
    def __init__(self):
        self.day_names = {
            'Sunday': 0,
            'Monday': 1,
            'Tuesday': 2,
            'Wednesday': 3,
            'Thursday': 4,
            'Friday': 5,
            'Saturday': 6
            }
        self.week= [
            'Monday',
            'Tuesday',
            'Wednesday',
            'Thursday',
            'Friday'
            ]
        self.end = [
            'Saturday',
            'Sunday'
            ]
        self.times = []

    def __str__(self):
        return str(self.times)

    def day(self, day, when):
        day_of_week = str(self.day_names[day])
        self.times.append([day_of_week, when])
        del day_of_week

    def weekdays(self, when):
        for day in self.week:
            self.day(day, when)

    def weekend(self, when):
        for day in self.end:
            self.day(day, when)

    def once(self, action, var = None):
        if var != None:
            action(var)
        else:
            action()

    def run(self, action, var = None):
        if var != None:
            while True:
                now = [datetime.now().strftime("%w"), datetime.now().strftime("%H%M")]
                for date in self.times:
                    if date == now:
                        action(var)
                sleep(60)
        else:
            while True:
                now = [datetime.now().strftime("%w"), datetime.now().strftime("%H%M")]
                for date in self.times:
                    if date == now:
                        action()
                sleep(60)