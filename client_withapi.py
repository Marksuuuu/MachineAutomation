import tkinter as tk
import json
import socketio
import uuid
import os
import re
import signal
import sys
import requests
from datetime import datetime

# Create a Tkinter window
window = tk.Tk()
window.title("Client")

# Create a Socket.IO client
sio = socketio.Client()
client_id = str(uuid.uuid4())
filename = os.path.basename(__file__)
file_path = 'rfid_config.ini'

# Fetch data from the API
url = 'http://odoodev.teamglac.com:3001/data'
response = requests.get(url)
data = json.loads(response.text)['data']

# Define the start and stop functions
@sio.event
def connect():
    print('Connected to server')
    sio.emit('client_connected', {'machine_name': filename})
    sio.on('dataPassed', receive_data)


@sio.event
def disconnect():
    print('Disconnected from server')
    window.destroy()
    sys.exit(0)


@sio.event
def send_file():
    with open(file_path, 'rb') as file:
        # Read the file as binary data
        file_data = file.read()

    # Create a payload dictionary or tuple with the file data and filename
    payload = {'file_data': file_data, 'filename': filename}

    # Emit the 'file_event' with the payload
    sio.emit('file_event', payload)


def start():
    global index
    if not index:
        print("No data found. Please add or set up data first.")
    else:
        if index <= len(data):
            stat_var = 'STARTED'
            machine_name = filename
            get_start_date = datetime.now()
            result = re.sub('.py', '', machine_name)
            uID = str(client_id)
            machine = data[f'index{index}']
            if machine['CLASS'] == result:
                data_to_send = machine, stat_var, uID, result, str(get_start_date)
                sio.emit('data', data_to_send)
                print('Data emitted:', data_to_send)

            index += 1

            if index > len(data):
                print("All indexes have been sent.")
                start_button.config(state=tk.NORMAL)
        else:
            print("All indexes have been sent.")


def stop():
    global index
    if not index:
        print("No data found. Please add or set up data first.")
    else:
        stat_var = 'STOP'
        get_stop_date = datetime.now()
        uID = str(client_id)
        data = stat_var, uID, str(get_stop_date)
        sio.emit('stop_data', data)
        start_button.config(state=tk.NORMAL)


@sio.event
def receive_data(data):
    # Process the received data
    data_received = data['data']
    if data_received == 'misteklock':
        send_file()
        print('item sendingg....')
    else:
        print('Received data:', data_received)


# Initialize the index to 1
index = 1

# Create the GUI
start_button = tk.Button(window, text="Start", command=start)
start_button.pack()

stop_button = tk.Button(window, text="Stop", command=stop)
stop_button.pack()

# Connect to the Socket.IO server
sio.connect('http://10.0.2.150:8085')

# Handle the SIGINT signal
def signal_handler(signal, frame):
    print('Disconnecting from server...')
    sio.disconnect()
    window.destroy()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Run the Tkinter event loop
window.protocol("WM_DELETE_WINDOW", signal_handler)
window.mainloop()
