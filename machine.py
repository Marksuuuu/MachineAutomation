import threading
from flask import Flask, render_template, request, redirect, url_for, jsonify, json, session
from flask_socketio import SocketIO, emit
from datetime import datetime
from tempfile import NamedTemporaryFile
import configparser
import psycopg2
import psycopg2.extras
import psutil
import subprocess
import time
# import datetime
import json
import hashlib
import requests
import re
import os
import paramiko
import ipaddress
import socketio





app = Flask(__name__)
app.secret_key = 'mark'
UPLOAD_FOLDER = 'static\\assets\\uploads'


clients = {}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

socketio = SocketIO(app)
global running_process
running_process = None

ALLOWED_EXTENSIONS = {'py'}

def allowed_file(filename):
    for extension in ALLOWED_EXTENSIONS:
        if '.' in filename and filename.rsplit('.', 1)[1].lower() == extension:
            return True
    else:
        return "<script>alert('Unsupported FIle type') </script>"


# Database configuration
db_host = 'localhost'
db_port = 5432
db_name = 'machine_automation_tbl'
db_user = 'flask_user'
db_password = '-clear1125'

# Programs configuration
programs = []

# Connect to the database
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)
cur = conn.cursor()


class Program:
    def __init__(self, id, name, path):
        self.id = id
        self.name = name
        self.path = path

    def is_running(self):
        for process in psutil.process_iter():
            try:
                if process.name() == 'python.exe' and self.path in process.cmdline():
                    return True
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
        return False

    def run(self):
        try:
            subprocess.check_call(['python', self.path])
        except subprocess.CalledProcessError as e:
            print(f"Error running {self.name}: {e}")


class ProgramManager:
    def __init__(self):
        self.programs = []

    # def load_programs(self):
    #     self.programs.clear()
    #     cur.execute('SELECT * FROM machine_tbl')
    #     for row in cur.fetchall():
    #         program = Program(row[0], row[1], row[2])
    #         self.programs.append(program)

    # def add_program(self, name, path):
    #     cur.execute(
    #         'SELECT COUNT(*) FROM machine_tbl WHERE name = %s AND path = %s', (name, path))
    #     count = cur.fetchone()[0]
    #     if count == 0:
    #         cur.execute(
    #             'INSERT INTO machine_tbl (name, path, status) VALUES (%s, %s, %s)', (name, path, 'stopped'))
    #         conn.commit()
    #         self.load_programs()
    #         return True
    #     else:
    #         return False

    # def check_running_programs(self):
    #     for program in self.programs:
    #         if program.is_running():
    #             status = 'running'
    #             date_start = datetime.now()
    #             cur.execute('UPDATE machine_tbl SET status = %s, date_start = %s WHERE id = %s',
    #                         (status, date_start, program.id))
    #             conn.commit()

    #         else:
    #             status = 'stopped'
    #             date_stop = datetime.now()
    #             cur.execute('UPDATE machine_tbl SET status = %s, date_stop = %s WHERE id = %s',
    #                         (status, date_stop, program.id))
    #             conn.commit()

    def count_total_machine(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            'SELECT count(name) as total_machines FROM machine_tbl WHERE name IN (SELECT MAX(name) FROM machine_tbl GROUP BY name)')
        total_count = cursor.fetchone()
        return total_count

    def count_total_machine_running(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            "SELECT count(status) FROM machine_tbl WHERE id IN (SELECT MAX(id) FROM machine_tbl GROUP BY name) and status = 'running'")
        total_count = cursor.fetchone()
        return total_count

    def count_total_machine_stopped(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            "SELECT count(status) FROM machine_tbl WHERE id IN (SELECT MAX(id) FROM machine_tbl GROUP BY name) and status = 'stopped'")
        total_count = cursor.fetchone()
        return total_count

    def view_table_func(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            "SELECT * FROM machine_tbl WHERE id IN (SELECT MAX(id) FROM machine_tbl GROUP BY name)")
        total_count = cursor.fetchall()
        return total_count

    # def run(self):
    #     while True:
            # self.load_programs()
            # self.check_running_programs()


program_manager = ProgramManager()

# Run the program manager in a separate thread

# t = threading.Thread(target=program_manager.run)
# t.start()


def handle_client(conn, addr):
    # Send a message to the client
    message = "Hello from the server!"
    conn.sendall(message.encode('utf-8'))

    # Receive data from the client endlessly
    while True:
        data = conn.recv(1024)
        if not data: # If no data is received, assume the client has disconnected
            print(f"Client at {addr} has disconnected")
            break
        print(f"Received {len(data)} bytes from client at {addr}: {data.decode('utf-8')}")

    # Close the connection
    conn.close()


# Define the route for the login page


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_username = request.form['username']
        form_password = request.form['password']

        if form_username == '' and form_password == '':
            return """<script>
                            alert('Error')
                            </script>"""
        else:

            url = f"http://hris.teamglac.com/api/users/login?u={form_username}&p={form_password}"
            response = requests.get(url).json()

            if response['result'] == False:
                return """<script>
                            alert('Error')
                            </script>"""
            else:
                user_data = response["result"]
                session['firstname'] = user_data['firstname']
                session['lastname'] = user_data['lastname']
                session['username'] = user_data['username']
                session['fullname'] = user_data['fullname']
                session['employee_department'] = user_data['employee_position']

                photo_url = session['photo_url'] = user_data['photo_url']

                if photo_url == False:
                    session['photo_url'] = """assets/compiled/jpg/1.jpg"""
                else:
                    hris = "http://hris.teamglac.com/"
                    session['photo_url'] = hris + user_data['photo_url']

                print(session['username'])
        return redirect(url_for('index', success=True))

    else:
        # Display the login form
        return render_template('auth-login.html')


@app.route('/process', methods=['POST'])
def process():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    msg = ''
    machine_name = request.form['machine_name']
    program_path = request.form['program_path']
    status = 'stopped'
    cursor.execute("INSERT INTO machine_tbl (name, path, status) VALUES (%s,%s,%s)",
                   (machine_name, program_path, status))
    conn.commit()
    msg = 'success'
    return jsonify({'name': msg})


@app.route('/machines')
def get_machines():
    cursor = conn.cursor()
    cursor.execute(
        "SELECT MIN(id) AS id, name FROM machine_tbl GROUP BY name;")
    rows = cursor.fetchall()
    machines = []
    for row in rows:
        machines.append({
            'id': row[0],
            'name': row[1]
        })
    cursor.close()
    return jsonify({'data': machines})


@app.route('/category')
def get_category():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM category_uph_tbl;")
    rows = cursor.fetchall()
    category_data = []
    for row in rows:
        category_data.append({
            'id': row[0],
            'category': row[1],
            'uph': row[2]
        })
    cursor.close()
    return jsonify({'data': category_data})


@app.route('/programs')
def get_programs():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM machine_tbl;")
    rows = cursor.fetchall()
    programs = []
    for data in rows:
        program = {
            'id': data[0],
            'path': data[2],
            'status': data[3],
            'date_start': data[4],
            'date_stop': data[5]
        }
        programs.append(program)
        print(data)
    cursor.close()
    return jsonify({'data': programs})


@app.route('/execute', methods=['POST'])
def execute_program():
    global running_process  # Access the global running_process variable
    if running_process and running_process.poll() is None:
        # If there is a running process, and it has not terminated yet,
        # send a response indicating that a program is already running
        return jsonify(msg="A program is already running. Please stop it first.")
    else:
        id = int(request.form['id'])  # Retrieve ID from the request form data

        # Perform a database query to fetch the name based on the ID
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT path FROM machine_tbl WHERE id = %s", (id,))
        fetchedData = cursor.fetchone()
        print(fetchedData)
        cursor.close()

        # Check if result is not empty
        if fetchedData:
            # Fetch the 'path' value from the result dictionary
            item_path = fetchedData['path']
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Change the current working directory of the Python script to the script directory
            program_path = f"cd {script_dir}'\\static\\assets\\uploads' && python {item_path}"
            command = re.sub(r"'", "", program_path)

            # Build the command to execute
            print(command)
            # Perform another database query using the item_path
            running_process = subprocess.Popen(
                command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = running_process.communicate()

            print("Output:")
            print(stdout.decode('utf-8'))
            print("Error:")
            print(stderr.decode('utf-8'))

            if running_process.returncode == 0:
                msg = "Program executed successfully."
                print("Program executed successfully.")
            else:
                msg = "Program executed successfully."
                print(
                    f"Program execution failed with return code {running_process.returncode}.")

            # Return the second query result as JSON response
            return jsonify(msg=msg)
        else:
            return jsonify(result=None)


@app.route('/stop_execute', methods=['POST'])
def stop_execute_program():
    global running_process

    # Check if there is a running process
    if running_process:
        try:
            # Terminate the running process
            running_process.terminate()
            running_process = None  # Reset the global variable
            return jsonify(msg="Program execution stopped successfully.")
        except Exception as e:
            return jsonify(msg=f"Failed to stop program execution: {str(e)}"), 500
    else:
        # If no running process, return an response
        return jsonify(msg="No program is currently running."), 400


@app.route('/get_name', methods=['POST'])
def get_name():
    item_id = int(request.form['id'])  # Retrieve ID from the request form data

    # Perform a database query to fetch the item name based on the item ID
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("SELECT name FROM machine_tbl WHERE id = %s", (item_id,))
    result = cursor.fetchone()
    cursor.close()

    # Check if result is not empty
    if result:
        # Fetch the 'name' value from the result dictionary
        item_name = result['name']
        print(item_name)
        # Perform another database query using the item_name
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""SELECT a.path,b.*
                       FROM 
                       machine_tbl a,
                       date_time_capture b
                       WHERE a.path = b.current_path
                       AND a.name = %s""", (item_name,))
        result2 = cursor.fetchall()
        print(result2)
        cursor.close()

        # Return the second query result as JSON response
        return jsonify(result=result2)
    else:
        return jsonify(result=None)


@app.route('/save_pause', methods=['POST'])
def save_pause():
    data = json.loads(request.data)
    pauseTime = data['pauseTime']
    machineId = data['machineId']
    print('machine ID ', machineId)
    # establish connection to database
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

    # insert data into database
    cursor.execute(
        "INSERT INTO captured_dates (machine_id, pause_time) VALUES (%s, %s)", (machineId, pauseTime))
    # close connection to database
    conn.commit()

    return json.dumps({'success': True}), 200, {'ContentType': 'application/json'}


@app.route('/card_details_table')
def card_details_table():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                   SELECT
                   id,
                   device_id,
                   status,
                   operator,
                   assigned_gl,
                   operation_code,
                   operation,
                   area
                   FROM machine_data_tbl
                   ORDER BY id ASC
                    """)
    dataResult = cursor.fetchall()
    capturedDatas = []
    for data in dataResult:
        capturedData = {
            'id': data[0],
            'device_id': data[1],
            'status': data[2],
            'operator': data[3],
            'assigned_gl': data[4],
            'operation_code': data[5],
            'operation': data[6],
            'area': data[7]
        }
        capturedDatas.append(capturedData)
    cursor.close()
    return jsonify({'data': capturedDatas})


@app.route('/insert_data', methods=['POST'])
def insert_data():
    data = request.get_json()
    data_id = data['id']
    duration = data['duration']
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(f"""UPDATE date_time_capture
	SET duration= '{duration}'
	WHERE id = {data_id};""")
    conn.commit()
    response = {'status': 'success'}
    return jsonify(response)


@app.route('/card_details')
def get_card_details():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                   SELECT
                   id,
                   device_id,
                   status,
                   operator,
                   assigned_gl,
                   operation_code,
                   operation,
                   area
                   FROM machine_data_tbl
                   ORDER BY id ASC
                   """)
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'id': row[0],
            'device_id': row[1],
            'status': row[2],
            'operator': row[3],
            'assigned_gl': row[4],
            'operation_code': row[5],
            'operation': row[6],
            'area': row[7]
        }
        cards.append(card)

    return jsonify(cards)


@app.route("/addMachines", methods=["POST"])
def addMachines():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    config = configparser.ConfigParser()
    config.read("connection_config.ini")
    
    machinesData = request.files.getlist("addMachine[]")
    controllersData = request.form["controllerInput"]
    ip_address = request.form["controllerIp"]

    for value in machinesData:
        filename = os.path.basename(value.filename)
        cur.execute("INSERT INTO machine_tbl (path, name, ip_address) VALUES (%s, %s, %s)",
                    (value.filename, controllersData, ip_address))
        conn.commit()
    # validate the IP address
    try:
        ip_address = ipaddress.ip_address(ip_address)
    except ValueError:
        return jsonify("Invalid IP address")
    
    
    connection_name = str(ip_address)
    remote_ip_address = config.get(connection_name, "remote_ip_address")
    username = config.get(connection_name, "username")
    password = config.get(connection_name, "password")
    port = config.getint(connection_name, "port")

    # create a new SSH client
    client = paramiko.SSHClient()

    # automatically add the remote server's host key
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect to the remote server
    try:
        client.connect(hostname=remote_ip_address, port=port, username=username, password=password)
        print('SUCCESS')
    except paramiko.AuthenticationException:
        return jsonify("Authentication failed")
    except paramiko.SSHException as e:
        return jsonify(f"Unable to establish SSH connection: {e}")

    # create the directory on the remote server
    directory = 'UPLOADS'
    sftp = client.open_sftp()
    try:
        sftp.mkdir(f'/home/mis/{directory}')
    except:
        pass

    # upload the file to the server
    for machine in machinesData:
        # save the uploaded file to a temporary location
        with NamedTemporaryFile(delete=False) as temp_file:
            machine.save(temp_file.name)

            # upload the file to the remote server
            remote_path = f'/home/mis/{directory}/{machine.filename}'
            try:
                sftp.put(temp_file.name, remote_path)
            except Exception as e:
                return jsonify(f"Failed to upload file: {e}")

        # move the uploaded file into the created folder
        # try:
        #     sftp.rename(
        #         remote_path, f'/home/mis/{directory}/{machine.filename}')
        # except Exception as e:
        #     return jsonify(f"Failed to move file: {e}")

    # close the SFTP and SSH clients
    sftp.close()
    client.close()
    msg = '"File uploaded successfully"'
    return jsonify(msg=msg)


@app.route('/machines/delete', methods=['POST'])
def delete_machine():
    cursor = conn.cursor()
    id = request.form['id']
    cursor.execute("DELETE FROM machine_tbl WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    return jsonify({'success': True})


@app.route("/check-ip", methods=['POST'])
def check_ip():
    remote_ip_address = request.json["remote_ip_address"]
    print(remote_ip_address)
    msg = remote_ip_address

    result = subprocess.run(["ping ", remote_ip_address],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # check if the ping command succeeded (return code is 0)
    print(result)
    if not result:
        msg = f'This {remote_ip_address} are Valid!.'
        checking = 'FALSE'
        return jsonify(checking=checking)
    elif result.returncode == 0:
        msg = f'This {remote_ip_address} are Invalid!.'
        checking = 'TRUE'
        return jsonify(checking=checking)
    elif result.returncode == '':
        msg = f'This {remote_ip_address} are Invalid!.'
        checking = 'FALSE'
        return jsonify(checking=checking)
    else:
        msg = f'This {remote_ip_address} are Invalid!.'
        checking = 'FALSE'
        return jsonify(checking=checking)
    return jsonify('success')


@app.route("/check-ip-addcontroller", methods=['POST', 'GET'])
def check_up_add_controller():
    config = configparser.ConfigParser()
    config.read("connection_config.ini")
    # check if JSON data is valid
    remote_ip_address = request.form["controllerIp"]

    connection_name = str(remote_ip_address)
    remote_ip_address = config.get(connection_name, "remote_ip_address")
    username = config.get(connection_name, "username")
    password = config.get(connection_name, "password")
    port = config.getint(connection_name, "port")
    max_inputs = config.getint(connection_name, "max_inputs")

    # create a new SSH client
    client = paramiko.SSHClient()

    # automatically add the remote server's host key
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect to the remote server
    try:
        client.connect(hostname=remote_ip_address, port=port,
                       username=username, password=password)
        print('SUCCESS')
    except paramiko.AuthenticationException:
        return jsonify("Authentication failed")
    except paramiko.SSHException as e:
        return jsonify(f"Unable to establish SSH connection: {e}")

    directory_path = f'/home/mis/UPLOADS/'

    sftp = client.open_sftp()
    files = sftp.listdir(directory_path)

    # Print the list of files
    # print('\nFiles in directory:')
    data = []
    # for file in files:
    #     print(file)
    data.append({'max_inputs': max_inputs})
    print(data)

    msg = 'SUCCESS'
    ip = remote_ip_address
    return jsonify(data=data)


@app.route("/save-connection", methods=["POST"])
def save_connection():
    # Get the connection parameters from the request data
    connection_name = request.json["connection_name"]
    remote_ip_address = request.json["remote_ip_address"]
    username = request.json["username"]
    password = request.json["password"]
    port = request.json["port"]
    max_inputs = request.json["max_inputs"]

    # Save the connection parameters to a configuration file
    config = configparser.ConfigParser()
    config[connection_name] = {
        "remote_ip_address": remote_ip_address,
        "username": username,
        "password": password,
        "port": port,
        "max_inputs": max_inputs
    }
    with open("connection_config.ini", "a") as config_file:
        config.write(config_file)
    # Return a JSON response with the status message
    msg = 'Connection configuration saved successfully.'
    return jsonify(msg=msg)


@app.route('/config-datatable', methods=['GET', 'POST'])
def get_config():
    config = configparser.ConfigParser()
    config.read('connection_config.ini')

    data = []
    for section in config.sections():
        if config.has_option(section, 'remote_ip_address') and config.has_option(section, 'username') and config.has_option(section, 'password') and config.has_option(section, 'port'):
            remote_ip_address = config.get(section, 'remote_ip_address')
            username = config.get(section, 'username')
            password = config.get(section, 'password')
            port = config.get(section, 'port')
            data.append({'remote_ip_address': remote_ip_address,
                        'username': username, 'password': password, 'port': port})
    print(data)
    return jsonify(data=data)


@app.route('/get-max-inputs', methods=['POST'])
def get_max_inputs():
    config = configparser.ConfigParser()
    config.read('connection_config.ini')

    data = []
    for section in config.sections():
        if config.has_option(section, 'max_inputs') and (section, 'remote_ip_address'):
            max_inputs = config.get(section, 'max_inputs')
            remote_ip_address = config.get(section, 'remote_ip_address')
            data.append({'max_inputs': max_inputs,
                        'remote_ip_address': remote_ip_address})
    print(data)
    return jsonify(data=data)

@socketio.on('connect')
def handle_connect():
    client_ip = request.remote_addr
    status = 'CONNECTED'
    clients[request.sid] = client_ip
    emit('client_connected', {'ip': client_ip,  'status': status}, broadcast=True)
    print('Client connected', client_ip)

@socketio.on('disconnect')
def handle_disconnect():
    ip = clients.pop(request.sid, None)
    if ip:
        emit('client_disconnected', {'ip': ip}, broadcast=True)
    print('Client disconnected', ip)

@socketio.on('message')
def handle_message(message):
    client_ip = request.remote_addr
    print(message)
    print(f'Received message from {client_ip}: {message}')
    emit('response', f'Server received message from {client_ip}: ' + message)

@socketio.on('data')
def handle_data(data, stat_var, uID):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    client_ip = request.remote_addr
    print(f'Received data from {client_ip}: {data}')
    emit('response', f'Server received data from {client_ip}: ' + str(data))
    
    print(data['operator'])
    print(data['assigned_gl'])
    print(data['operation_code'])
    print(data['operation'])
    print(data['area'])
    print(stat_var)
    print(uID)
    
    try:
        cur.execute("INSERT INTO machine_data_tbl (device_id, status, operator, assigned_gl, operation_code, operation, area) VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (uID, stat_var, data['operator'],data['assigned_gl'],data['operation_code'],data['operation'],data['area']))
        conn.commit()
        print("Data inserted successfully into the database")
        return jsonify("Data inserted successfully into the database")
    except Exception as e:
        print("Error inserting data into the database:", e)
        conn.rollback()
        return jsonify("Error inserting data into the database:", e)
    finally:
        cur.close()
    
@socketio.on('stop_data')
def handle_data(stat_var, uID):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    client_ip = request.remote_addr
    print(f'Received data from {client_ip}')
    emit('response', f'Server received data from {client_ip}: ')
    
    print(stat_var)
    
    try:
        cur.execute(f"UPDATE public.machine_data_tbl SET status='{stat_var}' WHERE device_id='{uID}'")
        conn.commit()
        print("Data inserted successfully into the database")
        return jsonify("Data inserted successfully into the database")
    except Exception as e:
        print("Error inserting data into the database:", e)
        conn.rollback()
        return jsonify("Error inserting data into the database:", e)
    finally:
        cur.close()
        

## ROUTES REDIRECT ONLY TO SPECIFIC PAGES##


@app.route('/index', methods=['GET'])
def index():
    print('Go to Index')
    program_manager = ProgramManager()
    count_machines = program_manager.count_total_machine()
    count_machines_running = program_manager.count_total_machine_running()
    count_machines_stopped = program_manager.count_total_machine_stopped()
    return render_template('home.html', count_machines=count_machines,
                           count_machines_running=count_machines_running, count_machines_stopped=count_machines_stopped, clients=clients)


@app.route('/data_table')
def view_tables():
    program_manager = ProgramManager()
    view_all_machine_and_status = program_manager.view_table_func()
    return render_template('controller-status.html', view_all_machine_and_status=view_all_machine_and_status)


@app.route('/controller_program')
def view_programs():
    print('Go to controller program')
    return render_template('controllers-program.html')


@app.route('/all_device')
def all_device():
    print('Go to All Devices')
    return render_template('layout-vertical-1-column.html')

@app.route('/configuration')
def configuration():
    print('Go to Config')
    return render_template('configuration-setup.html')


@app.route('/machine_uph')
def machine_uph():
    print('Go to machine uph')
    return render_template('machine_uph.html')


@app.route('/captured_time')
def captured_time():
    print('Go to Capture Time')
    return render_template('captured_time.html')


@app.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect(url_for('login', success=True))


if __name__ == '__main__':
    # app.run(host='localhost', port=8090, debug=True)
    socketio.run(app, host='10.0.2.150', port=8090, debug=True)
