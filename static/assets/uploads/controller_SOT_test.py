import psycopg2
import tkinter as tk
from datetime import datetime

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.running = True # Flag to indicate whether the application should continue running

        while self.running: # Start the main loop to continually update the GUI 
            self.master.update()
            self.master.update_idletasks()

    def create_widgets(self):
        # Create labels and entry fields for user input
        self.status_label = tk.Label(self, text="Status:")
        self.status_label.pack()
        self.status_entry = tk.Entry(self)
        self.status_entry.pack()

        self.setup_type_label = tk.Label(self, text="Setup Type:")
        self.setup_type_label.pack()
        self.setup_type_entry = tk.Entry(self)
        self.setup_type_entry.pack()
        
        self.total_qty_to_produce_label = tk.Label(self, text="Total Quantity to Produce:")
        self.total_qty_to_produce_label.pack()
        self.total_qty_to_produce_entry = tk.Entry(self)
        self.total_qty_to_produce_entry.pack()
        
        self.running_mo_label = tk.Label(self, text="Running MO:")
        self.running_mo_label.pack()
        self.running_mo_entry = tk.Entry(self)
        self.running_mo_entry.pack()
        
        self.operator_label = tk.Label(self, text="Operator:")
        self.operator_label.pack()
        self.operator_entry = tk.Entry(self)
        self.operator_entry.pack()

        # Create a button to submit the user input to the database
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_data)
        self.submit_button.pack()

    def submit_data(self):
        # Get the user input from the entry fields
        status = self.status_entry.get()
        setup_type = self.setup_type_entry.get()
        total_qty_to_proccess = self.total_qty_to_produce_entry.get()
        running_mo = self.running_mo_entry.get()
        operator = self.operator_entry.get()
        timestamp = datetime.now()
        

        # Connect to the database and execute the SQL insert statement
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
        cursor = conn.cursor()
        insert_query = "INSERT INTO controller_tbl (status, total_qty_to_proccess, running_mo, operator, timestamp, setup_type) VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.execute(insert_query, (status, total_qty_to_proccess, running_mo, operator, timestamp, setup_type))

        # Commit the changes and close the connection
        conn.commit()
        cursor.close()
        conn.close()
        
    def stop(self):
        self.running = False


if __name__ == '__main__':
    root = tk.Tk()
    app = Application(master=root)
    app.geometry('500x300')
    app.resizable(False, False)
    root.protocol("WM_DELETE_WINDOW", app.stop) # Add handler for the close button
    root.mainloop()
