#Raspberrypi/Haraldrud
#RIKTIG FIL!##
import json
import requests
import pprint
import sys
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
import datetime
from datetime import datetime
from time import sleep 
import keyboard #Using module keyboard
import serial
from time import gmtime, strftime
from datetime import timedelta, datetime
from origo.event.post_event import PostEvent
from origo.config import Config

post_event = PostEvent(Config)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)

gc = gspread.authorize(credentials)
teller = 0
timer = 0
minutter = 0
old_minutter = 1
olddate = 0
error = 0
stasjon = 1
day = 0
ser_bytes = serial.Serial('/dev/ttyUSB0', 9600)
besokende = 0
rad_samleside = 0
sensorId = 2 #ID for datakilden
stasjonId = 31
plasseringId = 1
siste_event = 0
print (strftime)

while True:
    try:    
        
        #Innlogging
        date = datetime.now().strftime('%a-%d-%m-%Y')
        
        
        #gc = gspread.authorize(credentials)
         
        #sps = gc.open("REN Gjenbruksstasjoner")
        day = datetime.now().strftime('%a')
        timer = int(datetime.now().strftime("%H"))
        
        
        #Åpningstider
        if (day == "Mon" or day == "Tue" or day == "Wed" or day == "Thu"):            
            if (timer == 7 and minutter == 30):
                stasjon = 1
            if (timer > 20 or timer < 7): 
                stasjon = 0
                
        if (day == "Fri" or day == "Sat"):
            if (timer < 9 or timer > 16):
                stasjon = 0
            else:
                stasjon = 1
                
        if (day == "Sun"):
            stasjon = 0   
        

        # Nytt ark med dagens dato
        if not (date == olddate):
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name('hahage.json', scope)
        
            gc = gspread.authorize(credentials)
            sps = gc.open("REN Gjenbruksstasjoner")            
            worksheet_list = sps.worksheets()
            titles_list=[]
            for worksheet in sps:
                titles_list.append(worksheet.title)
                print ("Henter liste")
            if date not in titles_list:
                if not (day == "Sun"):
                    print ("Lager nytt ark")
                    time.sleep(300)
                    wks = sps.add_worksheet(title = (date), rows="2000", cols="7")
                    upt = wks.update_acell('A1', 'Stasjon:')
                    upt = wks.update_acell('B1', 'Haraldrud Gjenbruk')
                    upt = wks.update_acell('C1', 'Haraldrud Hage')
                    upt = wks.update_acell('D1', 'Grønmo')
                    upt = wks.update_acell('E1', 'Ryen')
                    upt = wks.update_acell('F1', 'Grefsen')
                    upt = wks.update_acell('G1', 'Smestad')
                    upt = wks.update_acell('A2', 'Besøkende i dag:')
                    upt = wks.update_acell('B2', "=COUNTA(B3:B)")
                    upt = wks.update_acell('C2', "=COUNTA(C3:C)")
                    upt = wks.update_acell('D2', "=COUNTA(D3:D)")
                    upt = wks.update_acell('E2', "=COUNTA(E3:E)")
                    upt = wks.update_acell('F2', "=COUNTA(F3:F)")
                    upt = wks.update_acell('G2', "=COUNTA(G3:G)")
                else:
                    print ("Sunday - No sheet")
                    time.sleep(6200) #12 hours sleep
                    continue
            
        #oppdater dato og tid
        olddate = date
        timer = int(datetime.now().strftime("%H"))
        minutter = int(datetime.now().strftime("%M"))
        klokkeslett = (datetime.now().strftime('%H:%M:%S'))
        tid = datetime.now().strftime('%Y%m%dT%H%M%S+0200')
        
        #Iterasjoner siden siste event
        #siste_event = siste_event + 1
        
        if not (minutter == old_minutter):            
            print(klokkeslett)
            
        old_minutter = minutter
        #Se etter ny data fra Arduino utenfor åpningstid
        if (ser_bytes.in_waiting > 0) and (stasjon == 0): #if incoming bytes are waiting to be read from the serial input buffer
            data_str = ser_bytes.read(ser_bytes.in_waiting).decode('utf-8') #read the bytes and convert from binary array to ASCII
            print(data_str, end='')
            print("Input utenfor åpningstid")
            print(klokkeslett)
            time.sleep(0.01)   
        # Skriv data til gspred ved ny data innenfor åpningstid
        if (ser_bytes.in_waiting > 0) and (stasjon == 1): #if incoming bytes are waiting to be read from the serial input buffer
            data_str = ser_bytes.read(ser_bytes.in_waiting).decode('utf-8') #read the bytes and convert from binary array to ASCII
            #print(data_str, end='')
            time.sleep(0.01)
            print("Authorizing credentials: ")
            
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name('hahage.json', scope)
        
            gc = gspread.authorize(credentials)
            print ("OK")
            sps = gc.open("REN Gjenbruksstasjoner")   
            wks = sps.worksheet(date)            
            #Les av siste verdi fra dagens ark  
            teller = wks.acell('C2').value
            
            tellerstr = int(teller)
            besokende = tellerstr + 1
            tellerstr = tellerstr + 3
            print ("Total i dag:", besokende)
            #Skriv ut ny verdi
                      
            #Dagens dato ark            
            #sps = gc.open("REN Gjenbruksstasjoner")   
            #wks = sps.worksheet(date)            
            upt = wks.update_cell(tellerstr, 3, klokkeslett)
            #Oversiktsark for alle stasjoner
            rad_samleside = tellerstr + 40
            sps = gc.open("REN Gjenbruksstasjoner")   
            wks = sps.worksheet("Oversikt")
            upt = wks.update_acell('C4', besokende)
            upt = wks.update_cell(rad_samleside, 3, timer)
            error = 0
            print (klokkeslett)
            
            #Total ark for CSV eksport
            #sps = gc.open("REN Gjenbruksstasjoner")
            #wks = sps.worksheet("Total")
            #values = [date, klokkeslett, stasjonId]
            #upt = wks.append_row (values)
            
            #ORIGO Dataplattform
            
            url = "https://l2hhccv0ij.execute-api.eu-west-1.amazonaws.com/dev/event/besoksdata-gjenbruksstasjoner/1"
            data = {"tidspunkt" : tid, "sensorId" : sensorId, "stasjonId" : stasjonId, "plasseringId" : plasseringId}
            data_json = json.dumps(data)
            headers = {"x-api-key": x_api_key}
            response = requests.post(url, data=data_json, headers=headers)
            print (data_json)
            pprint.pprint(response.json())
            
        # Rebooter Pi om det ikke har skjedd noe den siste halvtimen
        if stasjon == 1 and siste_event > 50000000:
            print("Rebooter på grunn av inaktivitet fra sensor (Mulig systemfeil)")
            os.system("sudo reboot") 
            
            #Gårsdagens
        if timer == 21 and minutter == 30:
            print("Oppdaterer Haraldrud Gjenbruksstasjon - Oversikt")
            scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
            credentials = ServiceAccountCredentials.from_json_keyfile_name('hahage.json', scope)
        
            gc = gspread.authorize(credentials)
            sps = gc.open("REN Gjenbruksstasjoner")   
            wks = sps.worksheet("Oversikt")
            teller = wks.acell('C4').value
            besokende = int(teller)            
            upt = wks.update_acell('C5', besokende)
            upt = wks.update_acell('C4', "0")
            upt = wks.update_acell('C6', "23")
            n = int(wks.acell('C6').value)
            time.sleep(65)
        '''

            #Sletter liste i oversiktsark for å gjøre plass til morgendagens tall
        if timer == 22 or timer == 23 or timer == 1 or timer == 2 or timer == 3 and n < 1990:   
            gc = gspread.authorize(credentials)
            sps = gc.open("REN Gjenbruksstasjoner")   
            wks = sps.worksheet("Oversikt")
            n = int(wks.acell('C6').value)
            
            print ("Nullstiller")
            
            while n < 2000 and n > 0:
                timer = int(datetime.now().strftime("%H"))
                if timer > 4:
                    print("Restarter kode...")
        
                    os.execv(sys.executable, ['python3'] + sys.argv)
                gc = gspread.authorize(credentials)
                sps = gc.open("REN Gjenbruksstasjoner")   
                wks = sps.worksheet("Oversikt")                
                n = n + 1
                p = n                 
                upt = wks.update_acell('C6', p)
                upt = wks.update_cell(p, 3, "")
                continue
            time.sleep(1000)
            print ("Gårsdagens liste i ¨Oversikt¨ slettet")     
        ''' 
        #Reboot tellesystemet annenhver natt
        #if (day == "Mon" or day == "Wed" or day == "Fri"):            
        if (timer == 5 and minutter == 21):
                print("Rebooting...")
                time.sleep(65)
                os.system("sudo reboot") 
        
   # Fanger opp error og prøver på nytt
    except Exception as e:
        print("Error:")
        print (e)
        print ("Sender mail til Jørgen")
        olddate = 0
        error = 1
        errormsg = str(e)
        #Send Email til ansvarlig:
        import subprocess
        
        import smtplib
        
        import socket
        
        import os
        
        from email.mime.text import MIMEText
        
        import datetime
        
        
        # Change to your own account information
        
        to = to
        
        gmail_user = gmail_user
        
        gmail_password = gmail_password
        
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        
        smtpserver.ehlo()
        
        smtpserver.starttls()
        
        smtpserver.ehlo
        
        smtpserver.login(gmail_user, gmail_password)
        
        #today = datetime.date.today()
        
        # Very Linux Specific
        
        arg="ip route list"
        
        p=subprocess.Popen(arg,shell=True,stdout=subprocess.PIPE)
        
        data = p.communicate()
        
        split_data = data[0].split()
        
        #ipaddr = split_data[split_data.index(src)+1]
        
        # Get the current CPU speed
        
        f = os.popen("/opt/vc/bin/vcgencmd get_config arm_freq")
        
        cpu = f.read()
        
        mail_body = "Raspberry Pi Haraldrud Hage har fått en error. Lukk terminal og restart: python3 HAHage2.py for å igangsette teller på nytt. Føgende error:" + errormsg
        
        msg = MIMEText(mail_body)
        
        msg["Subject"] =  "Haraldrud hage ERROR: " + errormsg
        
        msg["From"] = gmail_user
        
        msg["To"] = to
        
        smtpserver.sendmail(gmail_user, [to], msg.as_string())
        
        smtpserver.quit()

        
        print("Restarter...")
        
        os.execv(sys.executable, ['python3'] + sys.argv)
        
        continue
    

