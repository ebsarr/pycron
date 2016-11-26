#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
# File: cron.py
"""Cron functionnality for python programs

Run tasks periodically.
This toll replicates Crontab in linux environment or tasks in Windows.
The action to be taken once a run schedule is reached is
a callable  python object( a function or a method of an instance), and any 
given number of  arguments( positional or keyword arguments) can be passed
to the callabe.

procedure to use a `Cron`
# First we create a `CronSchedule` objet
s = CronSchedule()

# Set up the schedule. In this case, we want the task to run every 5 minutes,
# starting from 1 minute in every hour
s.mins = range(1, 60, 5) #  we get a list: [1, 6, 11,...] and so on until 56

# Create a `Cron` object by passing the `CronSchedule` we created 
# Note that if a `CronSchedule` object is not passed to the
# constructor, a default schedule that makes the cron task run every minute
# is automatically created.
c = Cron(s)

# Set up an action for the `Cron` object we created.
# `func_print` is a function that prints its string argument to standard output.
# if you want to run this example, make sure to define `func_print` first
import datetime
def func_print(s):
    print("[%s] Printing `%s` periodically." % (datetime.datetime.now(), s)
c.set_action(func_print, 'Hello world')

# We can now ask the cron to run the task periodically
c.run()
# the `run` will execute for ever
"""

import time
import multiprocessing

SCHED_FREQUENCY = 0.1

class Cron:
    """Class that implements the cron functionnality"""
    
    def __init__(self, schedule=None):
        """Constructor

        Initialize a new `Cron` object,with a default schedule if a `shchedule`
        object wasn't passed to it.
        The default schedule runs the specified task once every minutes.
        """
        if schedule is None:
            self.schedule = CronSchedule()
        else:
            self.schedule = schedule
        self.action = None
        self.timeout = None
        self.args = None
        self.kwargs = None
        self.last_run = None

    def set_schedule(self, schedule):
        """Setup a schedule for this `Cron` object
        
        This must be done before calling on the `run` method
        @param schedule: `CronSchedule` object
        """
        self.schedule = schedule

    def set_action(self, action, *args, **kwargs):
        """Set the action(a callable object) to be taken

        This must be done before calling on the `run` method
        
        @param action : a callable object
        @param args : positional arguments to be passed to the callable
        @param kwargs: keyword arguments to be passed to the callable
        """
        self.action = action
        self.args = args
        self.kwargs = kwargs
        
    def __iter__(self):
        """returns this iterable object."""
        return self

    def next(self):
        """Determine if the next running schedule is reached"""
        while True:
            t = Time()
            if self.last_run is not None and t.min == self.last_run:
                time.sleep(SCHED_FREQUENCY)
                continue
            if int(t.month) in self.schedule.months and \
                int(t.day) in self.schedule.days and \
                int(t.weekday) in self.schedule.weekdays and \
                int(t.hour) in self.schedule.hours and \
                int(t.min) in self.schedule.mins and \
                int(t.sec) in [0, 1]:
                self.last_run = t.min
                return True
            else:
                time.sleep(SCHED_FREQUENCY)
                continue

    def run(self, timeout=None):
        """Run this `Cron` object indefinitly
        
        @param timeout: 
         a float that defines task running timeout. the default value is 59.0 .
         If a task does not finish untill the defined timeout, it will be
         terminated so that a new task can run once the next schedule is reached.
         If the task should not be terminated, just leave timeout to None
        """
        cp_name = multiprocessing.current_process().name
        if timeout is not None:
            self.timeout = timeout
        if self.action is None:
            raise RuntimeError("action is not a callable")
        try:
            while self.next():
                p = multiprocessing.Process(
                    name=cp_name + "." + self.action.__name__,
                    target=self.action,
                    args=self.args,
                    kwargs=self.kwargs
                )
                p.daemon = False
                try:
                    p.start()
                except Exception as e:
                    raise RuntimeError("Could not start a process for task to run: {0:s}".format(e))
                p.join(self.timeout)
                if p.is_alive():
                    p.terminate()
        except:
            pass


class CronSchedule:
    """A `CronSchedule` defines a schedule for a `Cron` object.
    
    It has attributes that define the minutes, hours, days, months or weekdays
    in which a `Cron` object should run its task:
    """
    def __init__(
        self, mins=xrange(60), hours=xrange(24), days=xrange(32),
            months=xrange(1, 13), weekdays=xrange(8)):
        """Constructor

        Initialize a new `CronSchedule` object with the following parameters:
        
        @param mins: a list that defines schedule as minutes, must be integers from 0 to 59
        @parma hours: a list that defines schedule as hours, must be integers from 0 to 23
        @param days: a list that defines schedule as days in the month, must be integers from 0 to 31
        @param weekdays: a list that defines schedule as days in the week, must be integers from 0 to 7
         0 is for Monday, 1 for Tuesday and so on
        """
        self.mins = mins
        self.hours = hours
        self.days = days
        self.months = months
        self.weekdays = weekdays


class Time:

    def __init__(self, time_tpl=None):
        """Initialize a Time object."""
        if time_tpl is None:
            self.format_string = None
            self.epoch_time = int(time.time())
        else:
            self.format_string = time_tpl[0]
            if isinstance(time_tpl[1], int):
                self.epoch_time = time_tpl[1]
            else:
                self.epoch_time = int(time.mktime(time.strptime(
                    time_tpl[1], self.format_string)))

    @property
    def year(self):
        return self.stringify("%Y")

    @property
    def month(self):
        return self.stringify("%m")

    @property
    def day(self):
        return self.stringify("%d")

    @property
    def weekday(self):
        return self.stringify("%w")

    @property
    def hour(self):
        return self.stringify("%H")

    @property
    def min(self):
        return self.stringify("%M")

    @property
    def sec(self):
        return self.stringify("%S")

    def stringify(self, format=None):
        """return time representation with the specified fomrat
        Keyword Argumants:
        format(str)     : time format, the default is the format specified for
                          this Time object.
        """
        if format is None:
            format = self.format_string
        return time.strftime(format, time.localtime(self.epoch_time))

    def __str__(self):
        """return the value of get_string() method with the default format."""
        if self.format_string is not None:
            return self.stringify(self.format_string)
        else:
            return str(self.epoch_time)


if __name__ == '__main__':
    import datetime
    print("Type Ctrl+C to abort!!!\n")
    try:
        for i in Cron():
            print("[{0:s}] {1:s}".format(datetime.datetime.now(), "Printing `Hello World` every minute."))
    except KeyboardInterrupt:
        print("Ending, au revoir et merci...")