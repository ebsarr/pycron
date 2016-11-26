# pycron

pycron is a simple module that emulates cron.
You can import it in a python program to run a function periodically.

Example
```python
import datetime
try:
    for i in Cron():
        print("[{0:s}] {1:s}".format(datetime.datetime.now(), "Printing \"Hello World\" every minute."))
except KeyboardInterrupt:
    print("Ending, au revoir et merci...")
```
