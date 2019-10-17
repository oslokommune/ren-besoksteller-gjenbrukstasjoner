import time
import sys
import os
while True:
    try: 
        print ("Starter snart")
        time.sleep(5)
        exec(open('/home/pi/ren/kioVisits/kioVisits.py').read())
    
    except Exception as e: 
        print ("Error:")
        print (e)
        print("Restarter...")
        
        os.execv(sys.executable, ['python3'] + sys.argv) 
        continue