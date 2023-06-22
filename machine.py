import hashlib
# import datetime
import json
import os
import psutil
import psycopg2
import psycopg2.extras
import re
import re
import requests
import socketio
import subprocess
import threading
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, jsonify, json, session
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, LoginManager, UserMixin
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.secret_key = 'mark'

clients = {}
photo = ''

socketio = SocketIO(app)
global running_process
running_process = None

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
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin):
    def __init__(self, id, firstname, lastname, username, fullname, employee_department, photo_url):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname
        self.username = username
        self.fullname = fullname
        self.employee_department = employee_department
        self.photo_url = photo_url

    def get_id(self):
        return str(self.id)

    def is_active(self):
        return True


@login_manager.user_loader
def load_user(user_id):
    firstname = session.get('firstname')
    lastname = session.get('lastname')
    username = session.get('username')
    fullname = session.get('fullname')
    employee_department = session.get('employee_department')
    photo_url = session.get('photo_url')

    return User(user_id, firstname, lastname, username, fullname, employee_department, photo_url)


def view_table_func(self):
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        "SELECT * FROM machine_tbl WHERE id IN (SELECT MAX(id) FROM machine_tbl GROUP BY name)")
    total_count = cursor.fetchall()
    return total_count


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
                return render_template('auth-login.html')
            else:
                user_data = response["result"]
                session['firstname'] = user_data['firstname']
                session['lastname'] = user_data['lastname']
                session['username'] = user_data['username']
                session['fullname'] = user_data['fullname']
                session['employee_department'] = user_data['employee_department']

                photo_url = session['photo_url'] = user_data['photo_url']

                user_id = user_data['user_id']
                user = User(user_id, user_data['firstname'], user_data['lastname'], user_data['username'],
                            user_data['fullname'], user_data['employee_department'], user_data['photo_url'])

                # Login the user
                login_user(user)

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


@app.route('/machines')
def get_machines():
    cursor = conn.cursor()
    cursor.execute(
        "SELECT MAX(id) AS id, fetched_ip, controller_name FROM fetched_ip_tbl GROUP BY fetched_ip, controller_name;")
    rows = cursor.fetchall()
    machines = []
    for row in rows:
        machines.append({
            'id': row[0],
            'fetched_ip': row[1],
            'controller_name': row[2]
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


@app.route('/get_name', methods=['POST'])
def get_name():
    item_id = int(request.form['id'])  # Retrieve ID from the request form data

    # Perform a database query to fetch the fetched_ip based on the item ID
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        "SELECT fetched_ip FROM fetched_ip_tbl WHERE id = %s", (item_id,))
    result = cursor.fetchone()
    cursor.close()

    # Check if result is not empty
    if result:
        # Fetch the 'fetched_ip' value from the result dictionary
        ip = result['fetched_ip']
        print(ip)
        # Perform another database query using the ip
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""SELECT 
                       id, 
                       fetched_ip, 
                       status, 
                       sid,
                       port,
                       machine_name,
                       area,
                       controller_name
                       FROM 
                       public.fetched_ip_tbl
                       WHERE
                       fetched_ip = %s
                       AND port !=''
                       ORDER BY id DESC LIMIT 5
                       """, (ip,))
        result2 = cursor.fetchall()
        cursor.close()

        # Return the second query result as JSON response
        return jsonify(result=result2)
    else:
        return jsonify(result=None)


@app.route('/insert_machine_name', methods=['POST'])
def insert_machine_name():
    cursor = conn.cursor()
    form_id = request.form['id']
    machine_name = request.form['machine_name_var']
    area_var = request.form['area_var']
    cursor.execute(f"""UPDATE 
                   public.fetched_ip_tbl
                   SET machine_name = '{machine_name}',
                   area = '{area_var}'
                   WHERE id = '{form_id}'""")
    conn.commit()
    cursor.close()
    data = {
        'form_id': form_id,
        'machine_name': machine_name,
        'area_var': area_var
    }
    return jsonify({'data': data})


@app.route('/insert_controller', methods=['POST'])
def insert_controller():
    cursor = conn.cursor()
    form_ip = request.form['ip']
    controller_name_var = request.form['controller_name_var']
    cursor.execute(f"""UPDATE 
                   public.fetched_ip_tbl
                   SET controller_name = '{controller_name_var}'
                   WHERE fetched_ip = '{form_ip}'""")
    conn.commit()
    cursor.close()
    data = {
        'form_ip': form_ip,
        'controller_name_var': controller_name_var,
    }
    return jsonify({'data': data})


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
                   area,
                   machine_name
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
            'area': data[7],
            'machine_name': data[8]
        }
        capturedDatas.append(capturedData)
    cursor.close()
    return jsonify({'data': capturedDatas})


@app.route('/delete_data', methods=['POST'])
def insert_data():
    cursor = conn.cursor()
    id = request.form['id']
    cursor.execute("DELETE FROM machine_data_tbl WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    return jsonify({'success': True})


@app.route('/card_details')
def get_card_details():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                    SELECT 
                        t1.id,
                        t1.device_id,
                        t1.status,
                        t1.operator,
                        t1.assigned_gl,
                        t1.operation_code,
                        t1.operation,
                        t1.area
                    FROM machine_data_tbl t1
                    INNER JOIN (
                    SELECT device_id, MAX(id) AS max_id
                    FROM machine_data_tbl
                    GROUP BY device_id
                    ) t2 ON t1.id = t2.max_id;
                   """)
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'id': row[0],
            'area': row[1],
            'port': row[2],
            'controller_name': row[3],
            'status': row[4],
            'operator': row[5],
            'assigned_gl': row[6],
            'operation_code': row[7],
            'operation': row[8],
            'machine_name': row[9],
            'machine': row[10]
        }
        cards.append(card)

    return jsonify(cards)


@app.route('/card_details_wirebond')
def card_details_wirebond():
    try:
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
                         SELECT
                            fit.id,
                            fit.area,
                            fit.port,
                            fit.controller_name,
                            fit.status,
                            mdt.mo,
                            mdt."totalProccessQty",
                            mdt.operation,
                            mdt.machine_name,
                            mdt.photo,
                            mdt."operatorIdNum",
                            fit.machine_name as machine,
                            mdt.status as mdt_status,
                            mdt.start_time,
                            mdt.stop_time,
                            CASE
                                WHEN stop_time IS NOT NULL THEN
                                    CONCAT(
                                        LPAD(EXTRACT(HOUR FROM (stop_time - start_time))::TEXT, 2, '0'), ':',
                                        LPAD(EXTRACT(MINUTE FROM (stop_time - start_time))::TEXT, 2, '0'), ':',
                                        LPAD(EXTRACT(SECOND FROM (stop_time - start_time))::TEXT, 2, '0')
                                    )
                                ELSE
                                    CONCAT(
                                        LPAD(EXTRACT(HOUR FROM (NOW() - start_time))::TEXT, 2, '0'), ':',
                                        LPAD(EXTRACT(MINUTE FROM (NOW() - start_time))::TEXT, 2, '0'), ':',
                                        LPAD(EXTRACT(SECOND FROM (NOW() - start_time))::TEXT, 2, '0')
                                    )
                            END AS total_running_time,
                            fit.start_date as fit_start_date,
                            fit.stop_date as fit_stop_date
                        FROM
                            public.fetched_ip_tbl AS fit
                            LEFT JOIN public.machine_data_tbl AS mdt ON fit.port = mdt.machine_name
                        WHERE
                            fit.area IN ('Wirebond', 'WIREBOND', 'wirebond')""")
        card_data = cursor.fetchall()
        cursor.close()

        # Convert data to a list of dictionaries
        cards = []
        for row in card_data:
            card = {
                'id': row[0],
                'area': row[1],
                'port': row[2],
                'controller_name': row[3],
                'status': row[4],
                'mo': row[5],
                'totalProccessQty': row[6],
                'operation': row[7],
                'machine_name': row[8],
                'photo': row[9],
                'operatorIdNum': row[10],
                'machine': row[11],
                'mdt_status': row[12],
                'start_time': row[13].strftime('%H:%M:%S') if row[13] is not None else None,
                'stop_time': row[14].strftime('%H:%M:%S') if row[14] is not None else None,
                'duration': str(row[15]) if row[15] is not None else None,
                'fit_start_date': row[16].strftime('%H:%M:%S') if row[16] is not None else None,
                'fit_stop_date': row[17].strftime('%H:%M:%S') if row[17] is not None else None
            }
            cards.append(card)

        return jsonify(cards)
    except psycopg2.Error as e:
        conn.rollback()  # Rollback the transaction in case of an error
        return "An error occurred while processing the request.", 500


@app.route('/card_details_eol1')
def card_details_eol1():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                    SELECT
     fit.id,
	fit.area,
	fit.port,
	fit.controller_name,
	fit.status,
	mdt.operator,
	mdt.assigned_gl,
	mdt.operation_code,
	mdt.operation,
	mdt.machine_name,
    fit.machine_name as machine
FROM
    public.fetched_ip_tbl AS fit
    LEFT JOIN public.machine_data_tbl AS mdt ON fit.port = mdt.machine_name
WHERE
    fit.area = 'Eol1' OR fit.area = 'eol1'""")
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'id': row[0],
            'area': row[1],
            'port': row[2],
            'controller_name': row[3],
            'status': row[4],
            'operator': row[5],
            'assigned_gl': row[6],
            'operation_code': row[7],
            'operation': row[8],
            'machine_name': row[9],
            'machine': row[10]
        }
        cards.append(card)

    return jsonify(cards)


@app.route('/card_details_eol2')
def card_details_eol2():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                    SELECT
     fit.id,
	fit.area,
	fit.port,
	fit.controller_name,
	fit.status,
	mdt.operator,
	mdt.assigned_gl,
	mdt.operation_code,
	mdt.operation,
	mdt.machine_name,
    fit.machine_name as machine
FROM
    public.fetched_ip_tbl AS fit
    LEFT JOIN public.machine_data_tbl AS mdt ON fit.port = mdt.machine_name
WHERE
    fit.area = 'Eol2' OR fit.area = 'eol2'""")
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'id': row[0],
            'area': row[1],
            'port': row[2],
            'controller_name': row[3],
            'status': row[4],
            'operator': row[5],
            'assigned_gl': row[6],
            'operation_code': row[7],
            'operation': row[8],
            'machine_name': row[9],
            'machine': row[10]
        }
        cards.append(card)

    return jsonify(cards)


@app.route('/card_details_mold')
def card_details_mold():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                    SELECT
     fit.id,
	fit.area,
	fit.port,
	fit.controller_name,
	fit.status,
	mdt.operator,
	mdt.assigned_gl,
	mdt.operation_code,
	mdt.operation,
	mdt.machine_name,
    fit.machine_name as machine
FROM
    public.fetched_ip_tbl AS fit
    LEFT JOIN public.machine_data_tbl AS mdt ON fit.port = mdt.machine_name
WHERE
    fit.area = 'Mold' OR fit.area = 'mold'""")
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'id': row[0],
            'area': row[1],
            'port': row[2],
            'controller_name': row[3],
            'status': row[4],
            'operator': row[5],
            'assigned_gl': row[6],
            'operation_code': row[7],
            'operation': row[8],
            'machine_name': row[9],
            'machine': row[10]
        }
        cards.append(card)

    return jsonify(cards)


@app.route('/card_details_die_prep')
def card_details_die_prep():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                    SELECT
     fit.id,
	fit.area,
	fit.port,
	fit.controller_name,
	fit.status,
	mdt.operator,
	mdt.assigned_gl,
	mdt.operation_code,
	mdt.operation,
	mdt.machine_name,
    fit.machine_name as machine
FROM
    public.fetched_ip_tbl AS fit
    LEFT JOIN public.machine_data_tbl AS mdt ON fit.port = mdt.machine_name
WHERE
    fit.area = 'Die Prep' OR fit.area = 'die drep'""")
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'id': row[0],
            'area': row[1],
            'port': row[2],
            'controller_name': row[3],
            'status': row[4],
            'operator': row[5],
            'assigned_gl': row[6],
            'operation_code': row[7],
            'operation': row[8],
            'machine_name': row[9],
            'machine': row[10]

        }
        cards.append(card)

    return jsonify(cards)


@app.route('/card_details_die_attached')
def card_details_die_attached():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                    SELECT
     fit.id,
	fit.area,
	fit.port,
	fit.controller_name,
	fit.status,
	mdt.operator,
	mdt.assigned_gl,
	mdt.operation_code,
	mdt.operation,
	mdt.machine_name,
    fit.machine_name as machine
FROM
    public.fetched_ip_tbl AS fit
    LEFT JOIN public.machine_data_tbl AS mdt ON fit.port = mdt.machine_name
WHERE
    fit.area = 'Die Attached' OR fit.area = 'die attached'""")
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'id': row[0],
            'area': row[1],
            'port': row[2],
            'controller_name': row[3],
            'status': row[4],
            'operator': row[5],
            'assigned_gl': row[6],
            'operation_code': row[7],
            'operation': row[8],
            'machine_name': row[9],
            'machine': row[10]
        }
        cards.append(card)

    return jsonify(cards)


@app.route('/machines/delete', methods=['POST'])
def delete_machine():
    cursor = conn.cursor()
    id = request.form['id']
    cursor.execute("DELETE FROM fetched_ip_tbl WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    return jsonify({'success': True})


@app.route('/insert_ip_data', methods=['POST'])
def insert_ip_data():
    try:
        machine_name = request.json["machine_name"]
        remove_py = re.sub('.py', '', machine_name)
        fetched_ip = request.json["fetched_ip"]
        status = request.json["status"]
        fetched_sid = request.json["fetched_sid"]
        get_start_date = request.json["get_start_date"]

        fetchedGetDate = str(get_start_date)

        # fetchedStartDate = get_card_details()

        cur.execute(
            "SELECT COUNT(port) FROM public.fetched_ip_tbl WHERE port = %s", (remove_py,))
        count = cur.fetchone()[0]

        if count > 0:
            # data already exists, update
            cur.execute("UPDATE public.fetched_ip_tbl SET status = %s, start_date = %s, sid = %s WHERE port = %s",
                        (status, fetchedGetDate, fetched_sid, remove_py))
            conn.commit()  # commit the transaction
            print("Data updated successfully in the database")
            return jsonify("Data updated successfully in the database")
        else:
            # data doesn't exist, insert
            cur.execute(
                "INSERT INTO public.fetched_ip_tbl (fetched_ip, status, sid, port, start_date) VALUES (%s, %s, %s, %s, %s)",
                (fetched_ip, status, fetched_sid, remove_py, fetchedGetDate))
            conn.commit()  # commit the transaction
            print("Data inserted successfully into the database")
            return jsonify("Data inserted successfully into the database")
    except Exception as e:
        conn.rollback()  # rollback the transaction if an error occurs
        print("An error occurred while inserting/updating data:", e)
        return jsonify("An error occurred while inserting/updating data")


@app.route('/request_data', methods=['POST'])
def request_data():
    data = request.get_json()
    print(data)
    socketio.emit('dataPassed', {'data': data})
    return jsonify(data=data)


## SOCKET IO CONNECTION ##
# Define the event handler for receiving files
@socketio.on('file_event')
def receive_file(payload):
    # Extract the file data and filename from the payload
    file_data = payload['file_data']
    filename = payload['filename']
    remove_py = re.sub('.py', '', filename)
    fileNameWithIni = 'config_' + remove_py + '.ini'

    # Generate a unique filename for each received file
    folder_path = 'downloadConfigs'
    file_path = f'{folder_path}/{fileNameWithIni}'

    # Process the received file data
    with open(file_path, 'wb') as file:
        file.write(file_data)

    # Send a response back to the client
    socketio.emit('result_response', {'fileNameWithIni': fileNameWithIni})
    return jsonify(data=fileNameWithIni)


@socketio.on('client_message')
def handle_client_message(data):
    message = data['message']
    filename_var = data['filename_var']
    print('Received message:', message)
    print('Received filename_var:', filename_var)
    socketio.emit('server_sample_response', {
        'message': message, 'filename_var': filename_var})


@socketio.on('client_connected')
def handle_client_connected(data):
    client_ip = request.remote_addr
    print('Client connected:', request.sid, client_ip)
    get_start_date = datetime.now()
    jsonStartDate = str(get_start_date)
    machine_name = data['machine_name']
    print(
        f"Client with SID {request.sid} connected with machine name {machine_name}")
    # Send a response event back to the client
    socketio.emit('server_response', {
        'message': 'CONNECTED', 'sid': request.sid, 'client_ip': client_ip, 'machine_name': machine_name,
        'get_start_date': jsonStartDate})


@socketio.on('disconnect')
def handle_disconnect():
    client_ip = request.remote_addr
    client_sid = request.sid
    get_stop_date = datetime.now()
    jsonStopDate = str(get_stop_date)

    print('Client disconnected:', client_ip, client_sid, jsonStopDate)
    cur.execute(
        f"UPDATE public.fetched_ip_tbl SET status='DISCONNECTED', stop_date='{jsonStopDate}' WHERE sid='{client_sid}'")
    conn.commit()
    socketio.emit('client_disconnected', {
        'message': 'DISCONNECTED', 'sid': request.sid, 'client_ip': client_ip})



@socketio.on('data')
def handle_data(data, stat_var, uID, result, get_start_date):
    client_ip = request.remote_addr
    print(f'Received data from {client_ip}: {data}')
    EMP_NO = data['EMP_NO']
    AREA_NAME = data['AREA_NAME']
    CLASS = data['CLASS']
    MACHINE_ID = data['MACHINE_ID']
    MACHINE_NAME = data['MACHINE_NAME']
    MO = data['MO']
    RUNNING_QTY = data['RUNNING_QTY']
    STATUS = data['STATUS']
    SUB_OPT_NAME = data['SUB_OPT_NAME']
    
    # hris = f'http://hris.teamglac.com/api/users/emp-num?empno={EMP_NO}'
    # response = requests.get(hris).json()
    
    # user_data = response.get("result", {})
    # photo_url = user_data.get('photo_url')

    start_date = str(get_start_date)

    # photo = "../static/assets/images/faces/pngegg.png" if photo_url is None else f"http://hris.teamglac.com/{photo_url}"
    # print(photo)

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                'INSERT INTO machine_fetched_data_tbl (area_name, class, emp_no, machine_id, machine_name, mo, running_qty, status, sub_opt_name, start_date, uid, machine_status) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                (AREA_NAME, CLASS, EMP_NO, MACHINE_ID, MACHINE_NAME, MO, RUNNING_QTY, STATUS, SUB_OPT_NAME, start_date, uID, stat_var))
            conn.commit()
            print("Data inserted successfully into the database")
            return jsonify("Data inserted successfully into the database")
    except psycopg2.Error as e:
        error_message = "Error inserting data into the database: " + str(e)
        print(error_message)
        conn.rollback()
        return jsonify(error_message)



@socketio.on('stop_data')
def handle_data(stat_var, uID, get_stop_date):
    client_ip = request.remote_addr
    print(f'Received data from {client_ip}')
    socketio.emit('response', f'Server received data from {client_ip}: ')
    stop_date = str(get_stop_date)
    print(stop_date)

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                "UPDATE public.machine_data_tbl SET stop_time=%s, status=%s WHERE device_id=%s",
                (stop_date, stat_var, uID)
            )
            conn.commit()
            print("Data inserted successfully into the database")
            return jsonify("Data inserted successfully into the database")
    except Exception as e:
        print("Error inserting data into the database:", e)
        conn.rollback()
        return jsonify("Error inserting data into the database: " + str(e))


## ROUTES REDIRECT ONLY TO SPECIFIC PAGES##


@app.route('/index', methods=['GET'])
@login_required
def index():
    user_id = current_user.id
    firstname = current_user.firstname
    lastname = current_user.lastname
    username = current_user.username
    fullname = current_user.fullname
    employee_department = current_user.employee_department
    photo_url = current_user.photo_url
    return render_template('home.html', user_id=user_id, firstname=firstname, lastname=lastname,
                           username=username, fullname=fullname, employee_department=employee_department,
                           photo_url=photo_url)


@app.route('/data_table')
@login_required
def view_tables():
    return render_template('controller-status.html')


@app.route('/controller_program')
@login_required
def view_programs():
    print('Go to controller program')
    return render_template('controllers-program.html')


@app.route('/all_device')
@login_required
def all_device():
    print('Go to All Devices')
    return render_template('controllers-area-view.html')


@app.route('/configuration')
@login_required
def configuration():
    print('Go to Config')
    return render_template('configuration-setup.html')


@app.route('/machine_uph')
@login_required
def machine_uph():
    print('Go to machine uph')
    return render_template('machine_uph.html')


@app.route('/captured_data')
@login_required
def captured_data():
    print('Go to Capture Data')
    return render_template('captured_time.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login', success=True))


# ROUTE TO AREAS#


@app.route('/mold')
def mold():
    return render_template('areas/controllers-area-view-mold.html')


@app.route('/wirebond')
def wirebond():
    return render_template('areas/controllers-area-view-wirebond.html')


@app.route('/die-prep')
def die_prep():
    return render_template('areas/controllers-area-view-die-prep.html')


@app.route('/die-attached')
def die_attached():
    return render_template('areas/controllers-area-view-die-attached.html')


@app.route('/eol1')
def eol1():
    return render_template('areas/controllers-area-view-eol1.html')


@app.route('/eol2')
def eol2():
    return render_template('areas/controllers-area-view-eol2.html')


if __name__ == '__main__':
    # app.run(host='localhost', port=8090, debug=True)
    socketio.run(app, host='10.0.2.150', port=8085, debug=True)
