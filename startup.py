import time
import sys
import os
while True:
    try: 
        print ("Starter snart")
        time.sleep(5)
        exec(open('kioVisits.py').read())
    
    except Exception as e: 
        print ("Error:")
        print (e)
        print("Restarter...")
        
        os.execv(sys.executable, ['python'] + sys.argv)
        continue