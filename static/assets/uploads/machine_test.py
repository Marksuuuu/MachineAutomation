from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter.constants import DISABLED, NORMAL
from tkinter.messagebox import showinfo
import time as time_count
from threading import Timer
import psycopg2
import psycopg2.extras
import os
db_host = 'localhost'
db_port = 5432
db_name = 'machine_automation_tbl'
db_user = 'flask_user'
db_password = '-clear1125'
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)
cur = conn.cursor()
running = True
while running:
    try:
    # root window
        root = tk.Tk()
        root.geometry('900x300')
        root.resizable(False, False)
        # root.iconbitmap('/machinery-svgrepo-com.png')
        root.title('TIME CAPTURE HERE')
        title_idle = 'IDLE'
        time_stamp = datetime.now()
        started = time_stamp.strftime("%Y-%m-%d %H:%M:%S.%f")
        print(started)
        # Get the filename without path
        filename = os.path.basename(__file__)
        query = """INSERT INTO date_time_capture (current_path, status, date_time)
                   VALUES (%s, %s, %s)
                   ON CONFLICT (current_path) DO UPDATE
                   SET current_path = EXCLUDED.current_path"""  # Specify the column to update
        values = (filename,title_idle,started)
        cur.execute(query,values)
        conn.commit()
        sec = 0
        class MainFunction:
            def __init__ (self,master):
                self.start_button = ttk.Button(root,text='START',width=40,command=lambda:[self.machine_started(), self.idle_function()])
                self.start_button.pack(expand=True)
                self.start_button.place(x=30,y=30,)
                self.production_stop = ttk.Button(root,text='STOP',state = DISABLED, command=lambda:[self.enable_production(), self.idle_function()],width=20)
                self.production_stop.pack(ipadx=10,ipady=10,expand=True)
                self.production_stop.place(x=300,y=70,)
                self.production_button = ttk.Button(root,text='PRODUCTION',state = DISABLED,command= self.machine_run,width=40)
                self.production_button.pack(ipadx=10,ipady=10,expand=True)
                self.production_button.place(x=30,y=70,)
                
                self.downtime_stop = ttk.Button(root,text='STOP',command=lambda:[self.enable_downtime(), self.idle_function()],state = DISABLED,width = 20)
                self.downtime_stop.pack(padx=10,ipady=10,expand=True)
                self.downtime_stop.place(x=300,y=110,)
                self.downtime_button = ttk.Button(root,text='DOWNTIME',command= self.machine_stop,state = DISABLED,width = 40)
                self.downtime_button.pack(ipadx=10,ipady=10,expand=True)
                self.downtime_button.place(x=30,y=110,)
                self.label_here1 = ttk.Label(root,text='STATUS : ',font = ("Courier Prime", 13 ))
                self.label_here1.place(x=350,y=30,)
                self.label_here = ttk.Label(root,text='',font = ("Courier Prime", 13 ))
                self.label_here.place(x=450,y=30,)
            def tick(self):
                started = time_stamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                print(started, '<-- IDLE')
                title_idle = 'IDLE'
                self.label_here.config(text = title_idle + ' AT: ' + ' '+ started)
                query = f"UPDATE date_time_capture SET status = '{title_idle}', date_time = '{started}' WHERE current_path = '{filename}'"
                values = (title_idle,started)
                cur.execute(query,values)
                conn.commit()
            def idle_function(self):
                prod = str(self.production_button['state'])
                down = str(self.downtime_button['state'])
                if prod == NORMAL and down == NORMAL:
                    Timer(10, self.tick).start()
            def machine_started(self):
                self.start_button['state'] = DISABLED
                self.downtime_button['state'] = NORMAL
                self.production_button['state'] = NORMAL
                title_idle = 'STARTED'
                time_stamp = datetime.now()
                started = time_stamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                print(started)
                self.label_here.config(text = title_idle + ' AT: ' + ' '+ started)
                query = f"UPDATE date_time_capture SET status = '{title_idle}', date_time = '{started}' WHERE current_path = '{filename}'"
                values = (title_idle,started)
                cur.execute(query,values)
                conn.commit()
            def machine_run(self):
                self.start_button['state'] = DISABLED
                self.production_stop['state'] = NORMAL
                self.production_button['state'] = DISABLED
                self.downtime_button['state'] = DISABLED
                title_idle = 'IN PRODUCTION'
                time_stamp = datetime.now()
                started = time_stamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                self.label_here.config(text = title_idle + ' AT: ' + ' '+ started)
                print(started)
                query = f"UPDATE date_time_capture SET status = '{title_idle}', date_time = '{started}' WHERE current_path = '{filename}'"
                values = (title_idle,started)
                cur.execute(query,values)
                conn.commit()
            def machine_stop(self):
                title_idle = 'MACHINE DOWNTIME'
                self.downtime_stop['state'] = NORMAL
                self.production_button['state'] = DISABLED
                self.production_stop['state'] = DISABLED
                time_stamp = datetime.now()
                started = time_stamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                print(started)
                self.label_here.config(text = title_idle + ' AT: ' + ' '+ started)
                query = f"UPDATE date_time_capture SET status = '{title_idle}', date_time = '{started}' WHERE current_path = '{filename}'"
                values = (title_idle,started)
                cur.execute(query,values)
                conn.commit()
            def enable_downtime(self):
                self.downtime_button['state'] = NORMAL
                self.production_stop['state'] = DISABLED
                self.downtime_stop['state'] = DISABLED
                self.production_button['state'] = NORMAL 
                title_idle = 'STOP DOWNTIME'
                time_stamp = datetime.now()
                started = time_stamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                print(started)
                self.label_here.config(text = title_idle + ' AT: ' + ' '+ started)
                query = f"UPDATE date_time_capture SET status = '{title_idle}', date_time = '{started}' WHERE current_path = '{filename}'"
                values = (title_idle,started)
                cur.execute(query,values)
                conn.commit()
                
            def enable_production(self):
                self.downtime_button['state'] = NORMAL
                self.downtime_stop['state'] = DISABLED
                self.production_stop['state'] = DISABLED
                self.production_button['state'] = NORMAL 
                title_idle = 'STOP PRODUCTION'
                time_stamp = datetime.now()
                started = time_stamp.strftime("%Y-%m-%d %H:%M:%S.%f")
                print(started)
                self.label_here.config(text = title_idle + ' AT: ' + ' '+ started)
                query = f"UPDATE date_time_capture SET status = '{title_idle}', date_time = '{started}' WHERE current_path = '{filename}'"
                values = (title_idle,started)
                cur.execute(query,values)
                conn.commit()
                # exit button
        func = MainFunction(root)
        root.mainloop()
    except KeyboardInterrupt:
            # Catch KeyboardInterrupt (Ctrl+C) to stop the application
            running = False