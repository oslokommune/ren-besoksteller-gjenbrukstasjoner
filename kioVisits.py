# Raspberrypi/Haraldrud
#RIKTIG FIL!##
import pprint
import sys
import os
import time
import serial
from datetime import datetime
from origo.event.post_event import PostEvent
from origo.config import Config
import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials

post_event = PostEvent(Config())

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials_path = "/home/pi/ren-besoksteller-gjenbrukstasjoner/credentials.json"

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    credentials_path, scope)

gc = gspread.authorize(credentials)
teller = 0
timer = 0
OLD_MINUTTER = 1
OLDDATE = 0
error = 0
day = 0
ser_bytes = serial.Serial('/dev/ttyUSB0', 9600)
besokende = 0
rad_samleside = 0
sensorId = 2  # ID for datakilden
stasjonId = 31
plasseringId = 1
siste_event = 0


def main():
    while True:
        try:
            # Innlogging
            date = datetime.now().strftime('%a-%d-%m-%Y')

            # gc = gspread.authorize(credentials)

            # sps = gc.open("REN Gjenbruksstasjoner")
            day = datetime.now().strftime('%a')
            timer = int(datetime.now().strftime("%H"))
            minutter = datetime.now().minute

            stasjon = 1
            # Åpningstider
            if day == "Mon" or day == "Tue" or day == "Wed" or day == "Thu":
                if timer == 7 and minutter == 30:
                    stasjon = 1
                if (timer > 20 or timer < 7):
                    stasjon = 0

            elif day == "Fri" or day == "Sat":
                if (timer < 9 or timer > 16):
                    stasjon = 0
                else:
                    stasjon = 1

            elif day == "Sun":
                stasjon = 0

            # Nytt ark med dagens dato
            global OLDDATE
            if date != OLDDATE:
                OLDDATE = date
                scope = ['https://spreadsheets.google.com/feeds',
                         'https://www.googleapis.com/auth/drive']
                credentials = ServiceAccountCredentials.from_json_keyfile_name(
                    credentials_path, scope)

                gc = gspread.authorize(credentials)
                sps = gc.open("REN Gjenbruksstasjoner")
                titles_list = []
                for worksheet in sps:
                    titles_list.append(worksheet.title)
                if date not in titles_list:
                    if not day == "Sun":
                        print("Lager nytt ark")
                        time.sleep(300)
                        wks = sps.add_worksheet(
                            title=(date), rows="2000", cols="7")
                        wks.update_acell('A1', 'Stasjon:')
                        wks.update_acell('B1', 'Haraldrud Gjenbruk')
                        wks.update_acell('C1', 'Haraldrud Hage')
                        wks.update_acell('D1', 'Grønmo')
                        wks.update_acell('E1', 'Ryen')
                        wks.update_acell('F1', 'Grefsen')
                        wks.update_acell('G1', 'Smestad')
                        wks.update_acell('A2', 'Besøkende i dag:')
                        wks.update_acell('B2', "=COUNTA(B3:B)")
                        wks.update_acell('C2', "=COUNTA(C3:C)")
                        wks.update_acell('D2', "=COUNTA(D3:D)")
                        wks.update_acell('E2', "=COUNTA(E3:E)")
                        wks.update_acell('F2', "=COUNTA(F3:F)")
                        wks.update_acell('G2', "=COUNTA(G3:G)")
                    else:
                        print("Sunday - No sheet")
                        time.sleep(6200)  # 12 hours sleep
                        continue

            # oppdater dato og tid
            timer = int(datetime.now().strftime("%H"))
            minutter = int(datetime.now().strftime("%M"))
            klokkeslett = (datetime.now().strftime('%H:%M:%S'))
            tid = datetime.now().strftime('%Y%m%dT%H%M%S+0200')

            # Iterasjoner siden siste event
            # siste_event = siste_event + 1
            global OLD_MINUTTER
            if not minutter == OLD_MINUTTER:
                print(klokkeslett)
                OLD_MINUTTER = minutter

            # Se etter ny data fra Arduino utenfor åpningstid
            # if incoming bytes are waiting to be read from the serial input buffer
            if ser_bytes.in_waiting > 0 and stasjon == 0:
                # read the bytes and convert from binary array to ASCII
                data_str = ser_bytes.read(ser_bytes.in_waiting).decode('utf-8')
                print(data_str, end='')
                print("Input utenfor åpningstid")
                print(klokkeslett)
                time.sleep(0.01)
            # Skriv data til gspred ved ny data innenfor åpningstid
            # if incoming bytes are waiting to be read from the serial input buffer
            if ser_bytes.in_waiting > 0 and stasjon == 1:
                print("-----------------------")
                # read the bytes and convert from binary array to ASCII
                data_str = ser_bytes.read(ser_bytes.in_waiting).decode('utf-8')
                # print(data_str, end='')
                time.sleep(0.01)
                print("Authorizing credentials: ")

                scope = ['https://spreadsheets.google.com/feeds',
                         'https://www.googleapis.com/auth/drive']
                credentials = ServiceAccountCredentials.from_json_keyfile_name(
                    credentials_path, scope)

                gc = gspread.authorize(credentials)
                print("OK")
                sps = gc.open("REN Gjenbruksstasjoner")
                wks = sps.worksheet(date)
                # Les av siste verdi fra dagens ark
                teller = wks.acell('C2').value

                tellerstr = int(teller)
                besokende = tellerstr + 1
                tellerstr = tellerstr + 3
                print("Total i dag:", besokende)
                # Skriv ut ny verdi

                # Dagens dato ark
                # sps = gc.open("REN Gjenbruksstasjoner")
                # wks = sps.worksheet(date)
                upt = wks.update_cell(tellerstr, 3, klokkeslett)
                # Oversiktsark for alle stasjoner
                rad_samleside = tellerstr + 40
                sps = gc.open("REN Gjenbruksstasjoner")
                wks = sps.worksheet("Oversikt")
                upt = wks.update_acell('C4', besokende)
                upt = wks.update_cell(rad_samleside, 3, timer)
                print(klokkeslett)

                # Total ark for CSV eksport
                # sps = gc.open("REN Gjenbruksstasjoner")
                # wks = sps.worksheet("Total")
                # values = [date, klokkeslett, stasjonId]
                # upt = wks.append_row (values)

                # ORIGO Dataplattform

                data = {"tidspunkt": tid, "sensorId": sensorId,
                        "stasjonId": stasjonId, "plasseringId": plasseringId}
                origo_response = post_event.post_event(
                    event_payload=data, dataset_id="besoksdata-gjenbruksstasjoner", version_id="1")
                pprint.pprint(origo_response)

            # Rebooter Pi om det ikke har skjedd noe den siste halvtimen
            if stasjon == 1 and siste_event > 50000000:
                print("Rebooter på grunn av inaktivitet fra sensor (Mulig systemfeil)")
                os.system("sudo reboot")

                # Gårsdagens
            if timer == 21 and minutter == 30:
                print("Oppdaterer Haraldrud Gjenbruksstasjon - Oversikt")
                scope = ['https://spreadsheets.google.com/feeds',
                         'https://www.googleapis.com/auth/drive']
                credentials = ServiceAccountCredentials.from_json_keyfile_name(
                    credentials_path, scope)

                gc = gspread.authorize(credentials)
                sps = gc.open("REN Gjenbruksstasjoner")
                wks = sps.worksheet("Oversikt")
                teller = wks.acell('C4').value
                besokende = int(teller)
                upt = wks.update_acell('C5', besokende)
                upt = wks.update_acell('C4', "0")
                upt = wks.update_acell('C6', "23")
                time.sleep(65)

            # Reboot tellesystemet annenhver natt
            # if (day == "Mon" or day == "Wed" or day == "Fri"):
            if timer == 5 and minutter == 21:
                print("Rebooting...")
                time.sleep(65)
                os.system("sudo reboot")

    # Fanger opp error og prøver på nytt
        except Exception as e:
            print(e)
            print("Starter på nytt om 30 sek")
            time.sleep(30)
            os.execv(sys.executable, ['python3'] + sys.argv)

            continue


if __name__ == "__main__":
    print("Starting kioVisits visitor counter...")
    main()
