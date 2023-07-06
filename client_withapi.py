import json
import os
import re
import signal
import sys
import tkinter as tk
import uuid
from datetime import datetime

import requests
import socketio

# Create a Tkinter window
window = tk.Tk()
window.title("Client")

# Create a Socket.IO client
sio = socketio.Client(reconnection=True, reconnection_attempts=5, reconnection_delay=1, reconnection_delay_max=5)
client_id = str(uuid.uuid4())
filename = os.path.basename(__file__)
remove_py = re.sub('.py', '', filename)
fileName = 'config_' + remove_py + '.json'
folder_path = 'downloadConfigs'
file_path = f'{folder_path}/{fileName}'

# Fetch data from the API
url = 'http://odoodev.teamglac.com:3001/data'
response = requests.get(url)
data = json.loads(response.text)['data']
print(data)

# Define the start and stop functions
@sio.event
def connect():
    print('Connected to server')
    sio.emit('client_connected', {'machine_name': filename})

@sio.event
def disconnect():
    print('Disconnected from server')

@sio.event
def reconnect():
    print('Reconnected to server')

@sio.event
def my_message(data):
    print('message received with', data['machine_name'])
    toPassData = data['machine_name']
    write_to_file_config(toPassData)
    sio.emit('my response', {'response': 'my response'})

def write_to_file_config(toPassData):
    remove_py = re.sub('.py', '', filename)
    fileNameWithIni = 'config_' + remove_py + '.json'
    folder_path = 'downloadConfigs'
    file_path = f'{folder_path}/{fileNameWithIni}'

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    with open(file_path, 'w') as file:
        data = {
            'filename': remove_py,
            'data': toPassData
        }
        json.dump(data, file)

@sio.event
def send_file():
    with open(fileName, 'rb') as file:
        # Read the file as binary data
        file_data = file.read()

    # Create a payload dictionary or tuple with the file data and filename
    payload = {'file_data': file_data, 'filename': filename}

    # Emit the 'file_event' with the payload
    sio.emit('file_event', payload)

def start():
    global index
    if index is None:
        print("No data found. Please add or set up data first.")
    else:
        with open(file_path, 'r') as file:
            file_data = json.load(file)
            data_result = file_data['data']
            print(data_result)

        if index < len(data):
            stat_var = 'STARTED'
            get_start_date = datetime.now()
            uID = str(client_id)
            machine = data[index]

            # Check if the machine's CLASS matches data_result
            if machine[str(index + 1)]['CLASS'] == data_result:
                data_to_send = machine, stat_var, uID,  data_result, str(get_start_date)

                sio.emit('data', data_to_send)
                print('Data emitted:', data_to_send)

            index += 1

            if index >= len(data):
                print("All indexes have been sent.")
                start_button.config(state=tk.NORMAL)
        else:
            print("All indexes have been sent.")

def stop():
    global index
    if index is None:
        print("No data found. Please add or set up data first.")
    else:
        stat_var = 'STOP'
        get_stop_date = datetime.now()
        uID = str(client_id)
        data_to_send = stat_var, uID, str(get_stop_date)
        sio.emit('stop_data', data_to_send)
        start_button.config(state=tk.NORMAL)

@sio.event
def receive_data(data):
    # Process the received data
    data_received = data['data']
    if data_received == 'misteklock':
        send_file()
        print('item sending....')
    else:
        print('Received data:', data_received)

# Initialize the index to None
index = 0

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
