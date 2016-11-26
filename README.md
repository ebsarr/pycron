# pycron

pycron is a simple module that emulates cron.
You can import it in a python program to run a function periodically.

Example: easiest way to use
```python
import datetime
try:
    for i in Cron():
        print("[{0:s}] {1:s}".format(datetime.datetime.now(), "Printing \"Hello World\" every minute."))
except KeyboardInterrupt:
    print("Ending, au revoir et merci...")
```

Example: another way
```python
import datetime

# func_print is the function we'll run every 5 minutes
def func_print(message):
    print("[%s] Printing `%s` periodically." % (datetime.datetime.now(), message)

# cron schedule
s = CronSchedule()
s.mins = range(1, 60, 5) # if passed this schedule, the cron will run every 5 minutes counting from 1

# create the cron
c = Cron(s)

# set the action
c.set_action(func_print, 'Hello world')

# Start
c.run()
```