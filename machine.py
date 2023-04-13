import threading
from flask import Flask, render_template, request, redirect, url_for, jsonify, json, session
from werkzeug.security import generate_password_hash, check_password_hash
import psycopg2
import psycopg2.extras
import psutil
import subprocess
import time
import datetime
import json
import hashlib
import requests

app = Flask(__name__)
app.secret_key = 'mark'

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

    def remove_program(self, id):
        cur.execute('DELETE FROM machine_tbl WHERE id = %s', (id,))
        conn.commit()
        self.load_programs()

    def check_running_programs(self):
        for program in self.programs:
            if program.is_running():
                status = 'running'
                date_start = datetime.datetime.now()
                cur.execute('UPDATE machine_tbl SET status = %s, date_start = %s WHERE id = %s',
                            (status, date_start, program.id))
                conn.commit()

            else:
                status = 'stopped'
                date_stop = datetime.datetime.now()
                cur.execute('UPDATE machine_tbl SET status = %s, date_stop = %s WHERE id = %s',
                            (status, date_stop, program.id))
                conn.commit()

    def count_total_machine(self):
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute(
            'SELECT count(name) as total_machines FROM machine_tbl WHERE id IN (SELECT MAX(id) FROM machine_tbl GROUP BY name)')
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


program_manager = ProgramManager()

# Run the program manager in a separate thread

t = threading.Thread(target=program_manager.run)
t.start()

# Load users from JSON file
with open('api.json') as f:
    users = json.load(f)

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
    return render_template('layout-vertical-navbar.html', username=username, success=success, count_machines=count_machines,
                           count_machines_running=count_machines_running, count_machines_stopped=count_machines_stopped)


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
    cursor.execute("SELECT * FROM machine_tbl")
    rows = cursor.fetchall()
    machines = []
    for row in rows:
        machines.append({
            'id': row[0],
            'name': row[1],
            'path': row[2],
            'status': row[3],
            'date_start': row[4],
            'date_stop': row[5],
        })
    cursor.close()
    return jsonify({'data': machines})


@app.route('/machines/update', methods=['POST'])
def update_machine():
    cursor = conn.cursor()
    id = request.form['id']
    name = request.form['edit_machine_name']
    path = request.form['edit_program_path']
    cursor.execute(
        "UPDATE machine_tbl SET name = %s, path = %s WHERE id = %s", (name, path, id))
    conn.commit()
    cursor.close()
    return jsonify({'success': True})


@app.route('/card_details')
def get_card_details():
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM machine_tbl')
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'id': row[0],
            'name': row[1],
            'path': row[2],
            'status': row[3],
            'date_start': str(row[4]),
            'date_stop': str(row[5])
        }
        cards.append(card)

    return jsonify(cards)


@app.route('/data_table')
def view_tables():
    program_manager = ProgramManager()
    view_all_machine_and_status = program_manager.view_table_func()
    return render_template('table-datatable-jquery.html', view_all_machine_and_status=view_all_machine_and_status)


@app.route('/machines/delete', methods=['POST'])
def delete_machine():
    cursor = conn.cursor()
    id = request.form['id']
    cursor.execute("DELETE FROM machine_tbl WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    return jsonify({'success': True})


@app.route('/all_device')
def all_device():
    print('Go to All Devices')
    return render_template('layout-vertical-1-column.html')


@app.route('/logout')
def logout():
    # Clear the session and redirect to the login page
    session.clear()
    return redirect(url_for('login', success=True))


if __name__ == '__main__':
    app.run(host="localhost", port=8083, debug=True)
