import datetime
from threading import Timer
import time

from Candidate import candidate

firstFlag = True

# Warning: run this one before the target time

def triggerCandidate():
    # avoid the short timeslot to call itself
    time.sleep(2)

    global firstFlag
    currTime = datetime.datetime.today()

    # first day
    if currTime.hour < 16:
        runTime = currTime.replace(hour = 16, minute = 0, second=0 , microsecond=0)
    else:
        runTime = currTime + datetime.timedelta(days=1)
    delta_t = runTime - currTime
    secs=delta_t.seconds

    print "Wait for {0} seconds".format(secs), runTime
    Timer(secs, triggerCandidate).start()
    # Ignore the first call
    if firstFlag == True:
        firstFlag = False
    else:
        print "Call Candidate", datetime.datetime.now()
        # Check current date
        if datetime.datetime.today().weekday() <= 4:
            candidate()

triggerCandidate()

