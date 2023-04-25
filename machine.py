import threading
from flask import Flask, render_template, request, redirect, url_for, jsonify, json, session
from flask_socketio import SocketIO, emit
from datetime import datetime
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




app = Flask(__name__)
app.secret_key = 'mark'
socketio = SocketIO(app)
UPLOAD_FOLDER = 'uploads'


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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

    def load_programs(self):
        self.programs.clear()
        cur.execute('SELECT * FROM machine_tbl')
        for row in cur.fetchall():
            program = Program(row[0], row[1], row[2])
            self.programs.append(program)

    def add_program(self, name, path):
        cur.execute(
            'SELECT COUNT(*) FROM machine_tbl WHERE name = %s AND path = %s', (name, path))
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute(
                'INSERT INTO machine_tbl (name, path, status) VALUES (%s, %s, %s)', (name, path, 'stopped'))
            conn.commit()
            self.load_programs()
            return True
        else:
            return False

    def check_running_programs(self):
        for program in self.programs:
            if program.is_running():
                status = 'running'
                date_start = datetime.now()
                cur.execute('UPDATE machine_tbl SET status = %s, date_start = %s WHERE id = %s',
                            (status, date_start, program.id))
                conn.commit()

            else:
                status = 'stopped'
                date_stop = datetime.now()
                cur.execute('UPDATE machine_tbl SET status = %s, date_stop = %s WHERE id = %s',
                            (status, date_stop, program.id))
                conn.commit()

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

    def run(self):
        while True:
            self.load_programs()
            self.check_running_programs()
            
    def is_valid_ip_address(ip_address):
        # regular expression to match an IPv4 address
        ipv4_regex = r'^(\d{1,3}\.){3}\d{1,3}$'
        # regular expression to match an IPv6 address
        ipv6_regex = r'^([a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}$'
        if re.match(ipv4_regex, ip_address) or re.match(ipv6_regex, ip_address):
            return True
        else:
            return False

    def is_ip_address_working(ip_address):
        try:
            output = subprocess.check_output(['ping', '-c', '1', ip_address])
            return True
        except subprocess.CalledProcessError:
            return False

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


program_manager = ProgramManager()

# Run the program manager in a separate thread

t = threading.Thread(target=program_manager.run)
t.start()

# Define the route for the login page

def is_valid_ip_address(ip_address):
    # regular expression to match an IPv4 address
    ipv4_regex = r'^(\d{1,3}\.){3}\d{1,3}$'
    # regular expression to match an IPv6 address
    ipv6_regex = r'^([a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}$'
    if re.match(ipv4_regex, ip_address) or re.match(ipv6_regex, ip_address):
        return True
    else:
        return False

def is_ip_address_working(ip_address):
    try:
        output = subprocess.check_output(['ping', '-c', '1', ip_address])
        return True
    except subprocess.CalledProcessError:
        return False

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
                session['employee_position'] = user_data['employee_position']

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
                   current_path,
                   status,
                   to_char(start_time, 'Month dd,YYYY hh24:mi:ss') as start_time,
                   to_char(end_time, 'Month dd,YYYY hh24:mi:ss') as end_time,
                   to_char(pause_time, 'Month dd,YYYY hh24:mi:ss') as pause_time,
                   to_char(resume_time, 'Month dd,YYYY hh24:mi:ss') as resume_time,
                   to_char(idle_time, 'Month dd,YYYY hh24:mi:ss') as idle_time,
                   duration
                   FROM date_time_capture
                   ORDER BY id ASC
                    """)
    dataResult = cursor.fetchall()
    capturedDatas = []
    for data in dataResult:
        capturedData = {
            'id': data[0],
            'current_path': data[1],
            'status': data[2],
            'start_time': data[3],
            'idle_time': data[7],
            'pause_time': data[5],
            'resume_time': data[6],
            'end_time': data[4],
            'duration': data[8]
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
                   current_path,
                   status,
                   to_char(start_time, 'Month dd,YYYY hh24:mi:ss') as start_time,
                   to_char(end_time, 'Month dd,YYYY hh24:mi:ss') as end_time,
                   to_char(pause_time, 'Month dd,YYYY hh24:mi:ss') as pause_time,
                   to_char(resume_time, 'Month dd,YYYY hh24:mi:ss') as resume_time,
                   to_char(idle_time, 'Month dd,YYYY hh24:mi:ss') as idle_time,
                   duration
                   FROM date_time_capture
                   ORDER BY id ASC
                   """)
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'id': row[0],
            'current_path': row[1],
            'status': row[2],
            'start_time': row[3],
            'end_time': row[4],
            'pause_time': row[5],
            'resume_time': row[6],
            'idle_time': row[7],
            'duration': row[7]
        }
        cards.append(card)

    return jsonify(cards)


@app.route("/addMachines", methods=["POST"])
def addMachines():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    machinesData = request.files.getlist("addMachine[]")
    controllersData = request.form["controllerInput"]
    ip_address = request.form["controllerIp"]

    # validate the IP address
    try:
        ip_address = ipaddress.ip_address(ip_address)
    except ValueError:
        return jsonify("Invalid IP address")

    # create a new SSH client
    client = paramiko.SSHClient()

    # automatically add the remote server's host key
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    # connect to the remote server
    try:
        client.connect(hostname=str(ip_address), port=22, username='mis', password='mis')
    except paramiko.AuthenticationException:
        return jsonify("Authentication failed")
    except paramiko.SSHException:
        return jsonify("Unable to establish SSH connection")

    # create the directory on the remote server
    directory = 'UPLOADS'
    sftp = client.open_sftp()
    try:
        sftp.mkdir(f'/home/mis/{directory}')
    except:
        pass

    # upload the file to the remote server
    for machine in machinesData:
        remote_path = f'/home/mis/{directory}/{machine.filename}'
        sftp.put(machine, remote_path)

    # close the SFTP and SSH clients
    sftp.close()
    client.close()

    return jsonify("File uploaded successfully")

    

    # for value in machinesData:
    #     filename = os.path.basename(value.filename)
    #     folder_path = os.path.join(os.sep, UPLOAD_FOLDER)
    #     folder_path_with_ip = os.path.join(os.sep, ip_address, folder_path.lstrip(os.sep).replace(os.sep, os.sep + os.sep))
    #     filepath = os.path.join("", UPLOAD_FOLDER, ip_address, filename)

    #     cur.execute("INSERT INTO machine_tbl (path, name, ip_address) VALUES (%s, %s, %s)",
    #                 (value.filename, controllersData, ip_address))
    #     conn.commit()

    #     print(folder_path)
    #     print(folder_path_with_ip)
    #     print(filepath)
    #     if not os.path.exists(folder_path_with_ip):
    #         os.makedirs(folder_path_with_ip)

    #     if os.path.exists(filepath):
    #         os.remove(filepath)

    #     value.save(filepath)

    #     # Transfer the file to the remote server
    #     remote_filepath = os.path.join(UPLOAD_FOLDER, ip_address, filename)
    #     sftp = ssh.open_sftp()
    #     sftp.put(filepath, remote_filepath)
    #     sftp.close()


@app.route('/machines/delete', methods=['POST'])
def delete_machine():
    cursor = conn.cursor()
    id = request.form['id']
    cursor.execute("DELETE FROM machine_tbl WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    return jsonify({'success': True})


## ROUTES REDIRECT ONLY TO SPECIFIC PAGES##


@app.route('/index', methods=['GET'])
def index():
    print('Go to Index')
    program_manager = ProgramManager()
    count_machines = program_manager.count_total_machine()
    count_machines_running = program_manager.count_total_machine_running()
    count_machines_stopped = program_manager.count_total_machine_stopped()
    return render_template('home.html', count_machines=count_machines,
                           count_machines_running=count_machines_running, count_machines_stopped=count_machines_stopped)


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


@app.route('/machine_uph')
def machine_uph():
    print('Go to machine uph')
    return render_template('machine_uph.html')


@app.route('/captured_time')
def captured_time():
    print('Go to machine uph')
    return render_template('captured_time.html')


@app.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect(url_for('login', success=True))


if __name__ == '__main__':
    app.run(host="localhost", port=8083, debug=True)
