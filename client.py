import tkinter as tk
import json
import socketio
import uuid

# Create a Tkinter window
window = tk.Tk()
window.title("Client")

# Create a Socket.IO client
sio = socketio.Client()
client_id = str(uuid.uuid4())

# Define the JSON data
json_data = {
  "index1": {
    "id": "1",
    "operator": "John Raymark LLavanes",
    "assigned_gl": "John Rey Dalit",
    "operation_code": 2010,
    "area": 'Die Prep',
    "operation": "2nd optical Insp-HPS"
  },
  "index2": {
    "id": "2",
    "operator": "Juan Dikalimot",
    "assigned_gl": "John Rey Dalit",
    "operation_code": 2011,
    "area": 'Die Attached',
    "operation": "2nd Opt.Insp-Waffle Pack MPPG/MPMP"
  },
  "index3": {
    "id": "3",
    "operator": "Juana Dinalimot",
    "assigned_gl": "John Rey Dalit",
    "operation_code": 2012,
    "area": 'Wirebond',
    "operation": "2nd Opt.Insp-Waffle Pack IXYS-Germany"
  }
}

# Define the start and stop functions
def start():
    global index
    if not index:
        print("No data found. Please add or set up data first.")
    else:
        if index <= len(json_data):
            stat_var = 'STARTED'
            uID = str(client_id)
            data = json_data[f'index{index}'], stat_var, uID
            sio.emit('data', data)
            index += 1
            start_button.config(state=tk.DISABLED)
            
        else:
            print("All indexes have been sent.")

def stop():
    global index
    if not index:
        print("No data found. Please add or set up data first.")
    else:
        stat_var = 'STOP'
        uID = str(client_id)
        data = stat_var, uID
        sio.emit('stop_data', data)
        start_button.config(state=tk.NORMAL)

# Initialize the index to 1
index = 1

# Create the GUI
start_button = tk.Button(window, text="Start", command=start)
start_button.pack()

stop_button = tk.Button(window, text="Stop", command=stop)
stop_button.pack()

# Connect to the Socket.IO server
sio.connect('http://10.0.2.150:8090')
# Run the Tkinter event loop
window.mainloop()
