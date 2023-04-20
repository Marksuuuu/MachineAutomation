import tkinter as tk
from tkinter.constants import DISABLED, NORMAL
from threading import Timer
import datetime
import psycopg2
import os



conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="machine_automation_tbl",
            user="flask_user",
            password="-clear1125")
cur = conn.cursor()


title_idle = 'IDLE'

time_stamp = datetime.datetime.now()
start_time = time_stamp.strftime("%Y-%m-%d %H:%M:%S.%f")

filename = os.path.basename(__file__)
print(filename)

query = """INSERT INTO date_time_capture (current_path, status)
                   VALUES (%s, %s)
                   ON CONFLICT (current_path) DO UPDATE
                   SET current_path = EXCLUDED.current_path"""
values = (filename, title_idle)
cur.execute(query,values)
conn.commit()

class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.start_time = None
        self.stop_time = None
        self.pause_time = None
        self.resume_time = None
        self.paused = False
        self.create_widgets()

    def create_widgets(self):
        self.start_button = tk.Button(self.master,width=20,height=10, text="Start", command=lambda:[self.start()])
        self.start_button.pack(side="left")
        self.stop_button = tk.Button(self.master,width=20,height=10, text="Stop", command=lambda:[self.stop()], state="disabled")
        self.stop_button.pack(side="left")
        self.pause_button = tk.Button(self.master,width=20,height=10, text="Pause/Resume", command=lambda:[self.pause_resume()], state="disabled")
        self.pause_button.pack(side="left")

    def start(self):
        self.status = 'STARTED'
        self.start_time = datetime.datetime.now()
        self.stop_time = self.start_time.replace(minute=30)
        print(self.start_time)
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.pause_button.config(state="normal")
        cur = conn.cursor()
        cur.execute(f"UPDATE date_time_capture SET status = '{self.status}', start_time = '{self.start_time}' WHERE current_path = '{filename}';")
        conn.commit()

    def stop(self):
        self.status = 'STOP'
        self.stop_time = datetime.datetime.now()
        self.save_to_database()
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.pause_button.config(state="disabled")
        cur = conn.cursor()
        cur.execute(f"UPDATE date_time_capture SET status = '{self.status}', end_time = '{self.stop_time}' WHERE current_path = '{filename}';")
        conn.commit()

    def pause_resume(self):
        if not self.paused:
            self.status = 'PAUSE'
            self.pause_time = datetime.datetime.now()
            self.paused = True
            cur = conn.cursor()
            cur.execute(f"UPDATE date_time_capture SET status = '{self.status}', resume_time = '{self.pause_time}' WHERE current_path = '{filename}';")
            conn.commit()
        else:
            self.resume_time = datetime.datetime.now()
            pause_duration = self.resume_time - self.pause_time
            self.start_time += pause_duration
            self.paused = False
            cur = conn.cursor()
            cur.execute(f"UPDATE date_time_capture SET status = '{self.status}', resume_time = '{self.start_time}' WHERE current_path = '{filename}';")
            conn.commit()

    def tick(self):
            self.idle_time = datetime.datetime.now()
            self.status = 'IDLE'
            print(self.status)
            cur = conn.cursor()
            cur.execute(f"UPDATE date_time_capture SET status = '{self.status}', idle_time = '{self.idle_time}' WHERE current_path = '{filename}';")
            conn.commit()
    def idle_function(self):
            stop_but = str(self.stop_button['state'])
            start_but = str(self.pause_button['state'])
            if stop_but == NORMAL and start_but == NORMAL:
                Timer(10, self.tick).start()
                print(Timer(10, self.tick))

    def save_to_database(self):
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname="machine_automation_tbl",
            user="flask_user",
            password="-clear1125")
        cur = conn.cursor()
        # cur.execute("INSERT INTO date_time_capture (start_time, end_time, pause_time, resume_time) VALUES (%s, %s, %s, %s)", (self.start_time, self.stop_time, self.pause_time, self.resume_time))
        # conn.commit()
        # cur.close()
        # conn.close()

root = tk.Tk()
root.geometry('450x150')
root.resizable(False, False)
app = App(master=root)
app.mainloop()
