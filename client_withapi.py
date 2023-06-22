import json
import socketio
import uuid
import os
import re
import signal
import sys
import requests
from datetime import datetime


sio = socketio.Client()
client_id = str(uuid.uuid4())
filename = os.path.basename(__file__)
file_path = 'rfid_config.ini'

# Fetch data from the API
url = 'http://odoodev.teamglac.com:3001/data'
response = requests.get(url)
data = response.json()['data']


@sio.event
def connect():
    print('Connected to server')
    sio.emit('client_connected', {'machine_name': filename})
    sio.on('dataPassed', receive_data)


@sio.event
def disconnect():
    print('Disconnected from server')
    sio.emit('putang_ina', {'machine_name': filename})
    sio.disconnect()
    sys.exit(0)


@sio.event
def send_file():
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(4096), b''):
            # Emit the chunk of file data
            sio.emit('file_event', {'file_data': chunk, 'filename': filename})


def start():
    global index
    if not index:
        print("No data found. Please add or set up data first.")
    else:
        if index <= len(data):
            stat_var = 'STARTED'
            machine_name = filename
            get_start_date = datetime.now()
            result = os.path.splitext(machine_name)[0]
            uID = str(client_id)
            machine = data[f'index{index}']
            if machine['CLASS'] == result:
                data_to_send = machine, stat_var, uID, result, str(get_start_date)
                sio.emit('data', data_to_send)
                print('Data emitted:', data_to_send)
            
            index += 1
            
            if index > len(data):
                print("All indexes have been sent.")
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

# Connect to the Socket.IO server
sio.connect('http://10.0.2.150:8085')

# Handle the SIGINT signal
def signal_handler(signal, frame):
    print('Disconnecting from server...')
    sio.disconnect()
    sys.exit(0)

# Register the signal handler
signal.signal(signal.SIGINT, signal_handler)

# Run the event loop
while True:
    user_input = input("Enter a command (start/stop/disconnect): ")
    if user_input == "start":
        start()
    elif user_input == "stop":
        stop()
    elif user_input == "disconnect":
        disconnect()
        break
    else:
        print("Invalid command. Please try again.")
