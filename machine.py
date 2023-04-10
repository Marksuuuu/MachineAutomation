from flask import Flask, render_template, request, redirect, url_for, jsonify, json, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
import psutil
import subprocess
import time
import datetime

app = Flask(__name__)
app.secret_key = 'mark'

# Database configuration
db_host = 'localhost'
db_port = 5432
db_name = 'machine_automation_controller'
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
        cur.execute('SELECT * FROM program_tbl')
        for row in cur.fetchall():
            program = Program(row[0], row[1], row[2])
            self.programs.append(program)

    def add_program(self, name, path):
        cur.execute('SELECT COUNT(*) FROM program_tbl WHERE name = %s AND path = %s', (name, path))
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute('INSERT INTO program_tbl (name, path, status) VALUES (%s, %s, %s)', (name, path, 'stopped'))
            conn.commit()
            self.load_programs()
            return True
        else:
            return False

    def remove_program(self, id):
        cur.execute('DELETE FROM program_tbl WHERE id = %s', (id,))
        conn.commit()
        self.load_programs()

    def check_running_programs(self):
        for program in self.programs:
            if program.is_running():
                status = 'running'
                date_start = datetime.datetime.now()
                cur.execute('UPDATE program_tbl SET status = %s, date_start = %s WHERE id = %s', (status, date_start, program.id))
                conn.commit()

            else:
                status = 'stopped'
                date_stop = datetime.datetime.now()
                cur.execute('UPDATE program_tbl SET status = %s, date_stop = %s WHERE id = %s', (status, date_stop, program.id))
                conn.commit()

    def count_total_machine(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            'SELECT count(name) as total_machines FROM program_tbl WHERE id IN (SELECT MAX(id) FROM program_tbl GROUP BY name)')
        total_count = cursor.fetchone()
        return total_count

    def count_total_machine_running(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            "SELECT count(status) FROM program_tbl WHERE id IN (SELECT MAX(id) FROM program_tbl GROUP BY name) and status = 'running'")
        total_count = cursor.fetchone()
        return total_count

    def count_total_machine_stopped(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            "SELECT count(status) FROM program_tbl WHERE id IN (SELECT MAX(id) FROM program_tbl GROUP BY name) and status = 'stopped'")
        total_count = cursor.fetchone()
        return total_count

    def view_table_func(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM program_tbl WHERE id IN (SELECT MAX(id) FROM program_tbl GROUP BY name)")
        total_count = cursor.fetchall()
        return total_count

    def run(self):
        while True:
            self.load_programs()
            self.check_running_programs()

program_manager = ProgramManager()

# Run the program manager in a separate thread
import threading

t = threading.Thread(target=program_manager.run)
t.start()

# Load users from JSON file
with open('api.json') as f:
    users = json.load(f)

# Define the route for the login page
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Check if the entered username and password are valid
        username = request.json['username']
        password = request.json['password']
        if username in users and users[username] == password:
            # Redirect to the index page with a success message
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index', success=True))
        else:
            # Return an error message as JSON
            return jsonify({'error': 'Invalid username or password'})
    else:
        # Display the login form
        return render_template('auth-login.html')

# Define the route for the index page
@app.route('/index', methods=['GET'])
def index():
    # Get the success parameter from the URL
    program_manager = ProgramManager()
    count_machines = program_manager.count_total_machine()
    count_machines_running = program_manager.count_total_machine_running()
    count_machines_stopped = program_manager.count_total_machine_stopped()
    success = request.args.get('success')
    username = session.get('username')
    return render_template('index.html', username=username, success=success, count_machines=count_machines,
                           count_machines_running=count_machines_running, count_machines_stopped=count_machines_stopped)

@app.route('/process', methods=['POST'])
def process():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
 
    msg = ''
    machine_name = request.form['machine_name']
    program_path = request.form['program_path']
    status = 'stopped'
    cursor.execute("INSERT INTO program_tbl (name, path, status) VALUES (%s,%s,%s)", (machine_name, program_path, status))
    conn.commit()
    msg = 'success'
    return jsonify({'name' : msg})

@app.route("/datatable", methods=["POST"])
def datatable():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    draw = request.form['draw']
    row = int(request.form['start'])
    rowperpage = int(request.form['length'])
    searchValue = request.form["search[value]"]
    likeString = "{}%".format(searchValue)

    cursor.execute("SELECT count(*) as allcount from program_tbl WHERE name LIKE %s", (likeString,))
    rsallcount = cursor.fetchone()
    totalRecordwithFilter = rsallcount['allcount']
    print(totalRecordwithFilter)

    # Total number of records without filtering
    cursor.execute("select count(*) as allcount from program_tbl")
    rsallcount = cursor.fetchone()
    totalRecords = rsallcount['allcount']
    print(totalRecords)

    if searchValue == '':
        cursor.execute('SELECT * FROM program_tbl LIMIT {limit} OFFSET {offset}'.format(limit=rowperpage, offset=row))
        programlist = cursor.fetchall()
    else:
        cursor.execute("SELECT * FROM program_tbl WHERE name LIKE %s LIMIT %s OFFSET %s;", (likeString, rowperpage, row,))
        programlist = cursor.fetchall()

    data = []
    for row in programlist:
       
        data.append({
            'name': row['name'],
            'path': row['path'],
            'status': row['status'],
            'date_start': row['date_start'],
            'date_stop': row['date_stop'],
        })

    response = {
        'draw': draw,
        'recordsTotal': totalRecords,
        'recordsFiltered': totalRecordwithFilter,
        'data': data,
    }

    return jsonify(response)

@app.route('/data_table')
def view_tables():
    program_manager = ProgramManager()
    view_all_machine_and_status = program_manager.view_table_func()
    return render_template('table-datatable-jquery.html', view_all_machine_and_status=view_all_machine_and_status)

@app.route('/program/<int:id>', methods=['DELETE'])
def delete_program(id):
    program_manager = ProgramManager()
    program_manager.delete_program(id)
    return jsonify({'success': True})

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    # redirect to the login page
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(host="localhost", port=8082, debug=True)
