import subprocess
import sys
import time


counter = 0
keep_running = True
while keep_running:
    p = subprocess.Popen('powershell.exe -ExecutionPolicy RemoteSigned -file "C:/Users/TracyTD/OneDrive - Truth Data Insights/TD/Software/VMtools/test.ps1"', stdout=sys.stdout)
    print(counter)
    p.communicate()
    time.sleep(10)
    counter += 1
    if counter >= 10:
        keep_running = False
