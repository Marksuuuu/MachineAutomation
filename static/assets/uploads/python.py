import time
import schedule



counter = 0
qtOfHours = 0

def task():
    counter += 1

while True:
    schedule.run_pending()
    time.sleep(1)
    if counter == qtOfHours:
        sys.exit()