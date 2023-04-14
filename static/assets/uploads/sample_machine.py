from tkinter import *
import tkinter as tk
from tkinter import ttk
from datetime import datetime
from tkinter.constants import DISABLED, NORMAL
from tkinter.messagebox import showinfo
import mysql.connector
import time as time_count
from threading import Timer

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="machine_sample"
)

my_cursor = mydb.cursor()


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
query = "INSERT INTO date_time_capture (status,date_time) VALUES (%s, %s)"
values = (title_idle,started)
my_cursor.execute(query,values)
mydb.commit()
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
        query = "INSERT INTO date_time_capture (status,date_time) VALUES (%s, %s)"
        values = (title_idle,started)
        my_cursor.execute(query,values)
        mydb.commit()

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
       query = "INSERT INTO date_time_capture (status,date_time) VALUES (%s, %s)"
       values = (title_idle,started)
       my_cursor.execute(query,values)
       mydb.commit()

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
       query = "INSERT INTO date_time_capture (status,date_time) VALUES (%s, %s)"
       values = (title_idle,started)
       my_cursor.execute(query,values)
       mydb.commit()

    def machine_stop(self):
       title_idle = 'MACHINE DOWNTIME'
       self.downtime_stop['state'] = NORMAL
       self.production_button['state'] = DISABLED
       self.production_stop['state'] = DISABLED
       time_stamp = datetime.now()
       started = time_stamp.strftime("%Y-%m-%d %H:%M:%S.%f")
       print(started)
       self.label_here.config(text = title_idle + ' AT: ' + ' '+ started)
       query = "INSERT INTO date_time_capture (status,date_time) VALUES (%s, %s)"
       values = (title_idle,started)
       my_cursor.execute(query,values)
       mydb.commit()

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
       query = "INSERT INTO date_time_capture (status,date_time) VALUES (%s, %s)"
       values = (title_idle,started)
       my_cursor.execute(query,values)
       mydb.commit()
     
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
       query = "INSERT INTO date_time_capture (status,date_time) VALUES (%s, %s)"
       values = (title_idle,started)
       my_cursor.execute(query,values)
       mydb.commit()
    # exit button


func = MainFunction(root)


    

root.mainloop()