from flask import Flask, render_template, request, redirect, url_for, jsonify, json
import psycopg2
import psycopg2.extras
import psutil
import subprocess
import time


app = Flask(__name__)

# Database configuration
db_host = 'localhost'
db_port = 5432
db_name = 'machine_automation_database'
db_user = 'flask_user'
db_password = '-clear1125'

# Programs configuration
programs = [
    {'name': 'controller1', 'path': 'dummy.py'},
    {'name': 'test2', 'path': 'dummy2.py'},
    # {'name': 'program3', 'path': '/path/to/program3.py'},
]

# Connect to the database
conn = psycopg2.connect(
    host=db_host,
    port=db_port,
    dbname=db_name,
    user=db_user,
    password=db_password
)
cur = conn.cursor()

# Add the programs to the database
for program in programs:
    cur.execute('INSERT INTO programs (name, path, status) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING', (program['name'], program['path'], 'stopped'))



conn.commit()

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
        cur.execute('SELECT * FROM programs')
        for row in cur.fetchall():
            program = Program(row[0], row[1], row[2])
            self.programs.append(program)

    def add_program(self, name, path):
        cur.execute('SELECT COUNT(*) FROM programs WHERE name = %s AND path = %s', (name, path))
        count = cur.fetchone()[0]
        if count == 0:
            cur.execute('INSERT INTO programs (name, path, status) VALUES (%s, %s, %s)', (name, path, 'stopped'))
            conn.commit()
            self.load_programs()
            return True
        else:
            return False

    def remove_program(self, id):
        cur.execute('DELETE FROM programs WHERE id = %s', (id,))
        conn.commit()
        self.load_programs()

    def check_running_programs(self):
        for program in self.programs:
            if program.is_running():
                status = 'running'
            else:
                status = 'stopped'
                # program.run()
            cur.execute('UPDATE programs SET status = %s WHERE id = %s', (status, program.id))
            conn.commit()

    def count_total_machine(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute('SELECT count(name) as total_machines FROM programs WHERE id IN (SELECT MAX(id) FROM programs GROUP BY name)')
        total_count = cursor.fetchone()
        return total_count

    def count_total_machine_running(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT count(status) FROM programs WHERE id IN (SELECT MAX(id) FROM programs GROUP BY name) and status = 'running'")
        total_count = cursor.fetchone()
        return total_count

    def count_total_machine_stopped(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT count(status) FROM programs WHERE id IN (SELECT MAX(id) FROM programs GROUP BY name) and status = 'stopped'")
        total_count = cursor.fetchone()
        return total_count

    def view_table_func(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("SELECT * FROM programs WHERE id IN (SELECT MAX(id) FROM programs GROUP BY name)")
        total_count = cursor.fetchall()
        return total_count

    def run(self):
        while True:
            self.load_programs()
            self.check_running_programs()

# Instantiate the program manager
program_manager = ProgramManager()

# Run the program manager in a separate thread
import threading
t = threading.Thread(target=program_manager.run)
t.start()

# Flask routes
@app.route('/')
def log_in():
    if request.method == 'POST':
        _username = request.form('username')
        _password = request.form('password')
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        result = cursor.execute('SELECT * FROM user_details WHERE username = %s', [username])

        if result > 0:
            data = cursor.fetchone()
            password = data['password']
        else:
            error = 'NOT FOUND'
            return render_template('auth-login.html', error=error)


@app.route('/index')
def index():
    program_manager = ProgramManager()
    count_machines = program_manager.count_total_machine()
    count_machines_running = program_manager.count_total_machine_running()
    count_machines_stopped = program_manager.count_total_machine_stopped()
    # return render_template('index.html', count_machines=count_machines, count_machines_running=count_machines_running, count_machines_stopped=count_machines_stopped)
    return render_template('auth-login.html')
@app.route('/data_table')
def view_tables():
    program_manager = ProgramManager()
    view_all_machine_and_status = program_manager.view_table_func()
    return render_template('table-datatable-jquery.html', view_all_machine_and_status=view_all_machine_and_status)

@app.route("/ajaxfile",methods=["POST","GET"])
def ajaxfile():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        if request.method == 'POST':
            ## Fetch records
            cursor.execute('SELECT * FROM programs')
            programs = cursor.fetchall()
            print(programs)
            data = []
            for row in programs:
                data.append({
                    'name': row['name'],
                    'path': row['path'],
                    'status': row['status'],
                })
  
            response = {
                'dt_data'
            }
            return jsonify(response)    
    except Exception as e:
        print(e)
    finally:
        cursor.close() 

@app.route('/add', methods=['POST'])
def add_program():
    name = request.form['name']
    path = request.form['path']
    program_manager.add_program(name, path)
    return redirect(url_for('index'))

@app.route('/remove/<int:id>', methods=['POST'])
def remove_program(id):
    program_manager.remove_program(id)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="localhost", port=8082, debug=True)
    # app.static_folder = 'static'
