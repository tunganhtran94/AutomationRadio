import time
from time import gmtime, strftime
from datetime import datetime

import webbrowser
import pandas as pd

import os
import sys
import alsaaudio

m = alsaaudio.Mixer('PCM')
current_volume = m.getvolume() # Get the current Volume

class radio():

    data_radio = pd.read_csv('data-radio-tet.csv', sep=';')
    row, col = data_radio.shape
    #data_history = pd.read_csv('data-history.csv', sep=';')
    #d = {'content': ['First'], 'start': ['08:00:00'], 'stop': ['09:00:00']}
    #df = pd.DataFrame(data=d)
    #print("Original DataFrame")
    #df.to_csv('data-history.csv', sep=';')
    
    
    #print(data_radio)

    def timenow(self):
        now = datetime.now()
        realtime = now.strftime("%H:%M:%S")
        return realtime

    def isTime(self):
        now = datetime.now()
        realtime = now.strftime("%H:%M:%S")
        start_trigger = self.data_radio[self.data_radio['start']==realtime].index.tolist()
        stop_trigger = self.data_radio[self.data_radio['stop']==realtime].index.tolist()
        if len(start_trigger)!=0:
            #os.system('pkill -3 chromium')
            #time.sleep(1)
            link = "python3 -m webbrowser -t " + str(self.data_radio.iloc[start_trigger[0], 5])
            os.system(link)
            m.setvolume(self.data_radio.iloc[start_trigger[0], 2])
            print("Open: "+ self.data_radio.iloc[start_trigger[0], 6] +" at "+self.time_display())
            #record = {'content': [self.data_radio.iloc[start_trigger[0], 6]], 'start': [self.data_radio.iloc[start_trigger[0], 3]], 'stop': [self.data_radio.iloc[start_trigger[0], 4]]}
            #print(record)
            #self.data_history = pd.read_csv('data-history.csv', sep=';')
            #self.data_history.append(record, ignore_index=True)
            #self.data_history.to_csv('data-history.csv', sep=';')
        if len(stop_trigger)!=0:
            #os.system('pkill -3 chromium')
            os.system('pkill -3 chromium')
            print("Close"+" at "+self.time_display()+ ", " + self.measure_temp())
            self.update_data_table()
            print(self.data_radio[['no.', 'comment', 'competed']].to_string(index=False))

       
    def time_display(self): 
        now = datetime.now()
        string = now.strftime("%H:%M:%S - %d/%m/%Y")
        return string
    
    def measure_temp(self):
        res = os.popen('vcgencmd measure_temp').readline()
        return "T=" + str(res.replace("temp=","").replace("'C\n","")) + "'C"
    def time_to_seconde(self, timexx):
        timelist =  [int(i) for i in timexx.split(':') if i.isdigit()]
        return (timelist[0]*3600 + timelist[1]*60 + timelist[2])
    def update_data_table(self):
        self.data_radio = pd.read_csv('data-radio-tet.csv', sep=';')
        for i in range(self.row):
            time_now = self.time_to_seconde(self.timenow())
            time_start = self.time_to_seconde(self.data_radio.iloc[i, 3])
            time_stop = self.time_to_seconde(self.data_radio.iloc[i, 4])
            percent = int(((time_now-time_start)/(time_stop-time_start))*100)
            if percent > 100:
                self.data_radio.iloc[i,1] = "100%"
            elif percent < 0:
                self.data_radio.iloc[i,1]= "0%"
            else:
                self.data_radio.iloc[i,1]= str(percent)+"%"
                
    def reset_Pi3(self,reboot_time):
        if reboot_time==self.timenow():
            os.system("sudo reboot")
                     
#Main loop            
    def __init__(self):
        print("Automation RADIO - author: Mr.Tony Tran")
        print("---------------------------------------------------------------")
        print("Today Radio Listing:")
        self.update_data_table()
        pd.set_option('display.max_columns', None)
        print(self.data_radio[['no.', 'comment', 'start', 'stop', 'link']].to_string(index=False))
        print('---------------------------------------------------------------')
        print('History record:')
        
        while True:
            self.update_data_table()
            self.isTime()
            self.reset_Pi3('01:00:00')
            time.sleep(1)          
              
        
if __name__ == "__main__":
    radio = radio()
