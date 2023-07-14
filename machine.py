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
from datetime import datetime, time, date
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

                if photo_url == False or photo_url is None:
                    session['photo_url'] = """assets/compiled/jpg/1.jpg"""
                else:
                    hris = "http://hris.teamglac.com/"
                    session['photo_url'] = hris + user_data['photo_url']

        return redirect(url_for('index', success=True))

    else:
        # Display the login form
        return render_template('auth-login.html')


@app.route('/machines')
def get_machines():
    try:
        cursor = conn.cursor()
        cursor.execute("""
                    SELECT    
                        id, 
                        fetched_ip,  
                        controller_name
                    FROM
                        fetched_ip_tbl
                    WHERE
                        id IN (SELECT MAX(id) FROM
                        fetched_ip_tbl
                    GROUP BY controller_name )
                       """)
        rows = cursor.fetchall()
        machines = []
        for row in rows:
            machines.append({
                'id': row[0],
                'fetched_ip': row[1],
                'controller_name': row[2]
            })
        conn.commit()  # Commit the transaction before closing the cursor
        cursor.close()
        return jsonify({'data': machines})
    except Exception as e:
        conn.rollback()  # Rollback the transaction in case of an error
        cursor.close()
        print("Error executing query:", e)
        return jsonify({'error': 'An error occurred while fetching machines.'}), 500


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


@app.route('/get_name', methods=['GET', 'POST'])
def get_name():
    item_id = int(request.form['id'])  # Retrieve ID from the request form data

    # Perform a database query to fetch the fetched_ip based on the item ID
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(
        "SELECT fetched_ip FROM fetched_ip_tbl WHERE id = %s", (item_id,))
    result = cursor.fetchone()

    # Check if result is not empty
    if result:
        # Fetch the 'fetched_ip' value from the result dictionary
        ip = result['fetched_ip']
        # Perform another database query using the ip
        cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cursor.execute("""
                        SELECT    
                            id, 
                            fetched_ip, 
                            status, 
                            sid,
                            port,
                            machine_name,
                            area,
                            controller_name
                        FROM
                            fetched_ip_tbl
                        WHERE
                            id IN (SELECT MAX(id) FROM
                            fetched_ip_tbl
                        GROUP BY port)
                        ORDER BY 
                            id 
                        DESC LIMIT 5
                       """, (ip,))
        rows = cursor.fetchall()
        machines = []
        for row in rows:
            machines.append({
                'id': row[0],
                'fetched_ip': row[1],
                'status': row[2],
                'sid': row[3],
                'port': row[4],
                'machine_name': row[5],
                'area': row[6],
                'controller_name': row[7],
                })
        conn.commit()
        cursor.close()
        return jsonify({'data': machines})
    else:
        return jsonify(result=None)


@app.route('/insert_machine_name', methods=['POST'])
def insert_machine_name():
    
    
    cursor = conn.cursor()
    form_id = request.form['id']
    machine_name = request.form['selectMachineName']
    area_var = request.form['selectArea']
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
    controller_name_var = request.form['controllerInput']
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
                    mdt.mo as MO,
                    mdt.emp_no as EMP_NO,
                    mdt.running_qty as RUNNING_QTY,
                    fit.start_date as START_TIME,
                    mdt.start_date as MACHINE_START_DATE,
                    mdt.class as MACHINE_NAME
                FROM
                        public.fetched_ip_tbl AS fit
                    LEFT JOIN 
                        public.machine_fetched_data_tbl AS mdt 
                    ON 
                        fit.port = mdt.class
                    """)
    dataResult = cursor.fetchall()
    capturedDatas = []
    for data in dataResult:
        capturedData = {
            'MO': row[0],
            'EMP_NO': row[1],
            'RUNNING_QTY': row[2],
            'START_TIME': row[3],
            'MACHINE_START_DATE': row[4],
            'MACHINE_NAME': row[5]        
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
    result = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    container = []
    for row in result:
        data = {
            'MO': row[0],
            'EMP_NO': row[1],
            'RUNNING_QTY': row[2],
            'START_TIME': row[3],
            'MACHINE_START_DATE': row[4],
            'MACHINE_NAME': row[5]        
        }
        container.append(data)

    return jsonify(container)


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
            fit.status as STATUS,
            mdt.mo as MO,
            mdt.emp_no as EMP_NO,
            mdt.running_qty as RUNNING_QTY,
            fit.start_time as START_TIME,
            fit.idle_time as IDLE_TIME,
            mdt.start_date as MACHINE_START_DATE,
            mdt.class as MACHINE_NAME
        FROM
            public.fetched_ip_tbl AS fit
        LEFT JOIN 
            public.machine_fetched_data_tbl AS mdt 
        ON 
            fit.port = mdt.class
        WHERE
            fit.area = 'Eol1' OR fit.area = 'EOL1'
    """)
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        machine_start_date = None
        if row[6] is not None:
            machine_start_date = datetime.strptime(row[6], '%Y-%m-%d %H:%M:%S.%f').time()
        card = {
            'STATUS': row[0],
            'MO': row[1],
            'EMP_NO': row[2],
            'RUNNING_QTY': row[3],
            'IDLE_TIME': row[4],
            'START_TIME': row[5].strftime('%H:%M:%S') if row[5] is not None else None,
            'MACHINE_START_DATE': machine_start_date.strftime('%H:%M:%S') if machine_start_date else None,
            'MACHINE_NAME': row[7]
        }
        cards.append(card)

    return jsonify(cards)



@app.route('/card_details_eol2')
def card_details_eol2():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                SELECT
                    mdt.mo as MO,
                    mdt.emp_no as EMP_NO,
                    mdt.running_qty as RUNNING_QTY,
                    fit.start_time as START_TIME,
                    mdt.start_date as MACHINE_START_DATE,
                    mdt.class as MACHINE_NAME
                FROM
                        public.fetched_ip_tbl AS fit
                    LEFT JOIN 
                        public.machine_fetched_data_tbl AS mdt 
                    ON 
                        fit.port = mdt.class
                WHERE
                    fit.area = 'Eol2' OR fit.area = 'eol2'
    """)
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'MO': row[0],
            'EMP_NO': row[1],
            'RUNNING_QTY': row[2],
            'START_TIME': row[3],
            'MACHINE_START_DATE': row[4],
            'MACHINE_NAME': row[5]        
        }
        cards.append(card)

    return jsonify(cards)


@app.route('/card_details_mold')
def card_details_mold():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                SELECT
                    mdt.mo as MO,
                    mdt.emp_no as EMP_NO,
                    mdt.running_qty as RUNNING_QTY,
                    fit.start_time as START_TIME,
                    mdt.start_date as MACHINE_START_DATE,
                    mdt.class as MACHINE_NAME
                FROM
                        public.fetched_ip_tbl AS fit
                    LEFT JOIN 
                        public.machine_fetched_data_tbl AS mdt 
                    ON 
                        fit.port = mdt.class
                WHERE
                    fit.area = 'Mold' OR fit.area = 'mold'
    """)
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'MO': row[0],
            'EMP_NO': row[1],
            'RUNNING_QTY': row[2],
            'START_TIME': row[3],
            'MACHINE_START_DATE': row[4],
            'MACHINE_NAME': row[5]        
        }
        cards.append(card)

    return jsonify(cards)


@app.route('/card_details_die_prep')
def card_details_die_prep():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                SELECT
                    mdt.mo as MO,
                    mdt.emp_no as EMP_NO,
                    mdt.running_qty as RUNNING_QTY,
                    fit.start_time as START_TIME,
                    mdt.start_date as MACHINE_START_DATE,area_var
                    mdt.class as MACHINE_NAME
                FROM
                        public.fetched_ip_tbl AS fit
                    LEFT JOIN 
                        public.machine_fetched_data_tbl AS mdt 
                    ON 
                        fit.port = mdt.class
                WHERE
                    fit.area = 'Die Prep' OR fit.area = 'Die Prep'
    """)
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'MO': row[0],
            'EMP_NO': row[1],
            'RUNNING_QTY': row[2],
            'START_TIME': row[3],
            'MACHINE_START_DATE': row[4],
            'MACHINE_NAME': row[5]
        }
        cards.append(card)

    return jsonify(cards)


@app.route('/card_details_die_attached')
def card_details_die_attached():
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute("""
                SELECT
                    mdt.mo as MO,
                    mdt.emp_no as EMP_NO,
                    mdt.running_qty as RUNNING_QTY,
                    fit.start_time as START_TIME,
                    mdt.start_date as MACHINE_START_DATE,
                    mdt.class as MACHINE_NAME
                FROM
                        public.fetched_ip_tbl AS fit
                    LEFT JOIN 
                        public.machine_fetched_data_tbl AS mdt 
                    ON 
                        fit.port = mdt.class
                WHERE
                    fit.area = 'Eol1' OR fit.area = 'Die Attach'
    """)
    card_data = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    cards = []
    for row in card_data:
        card = {
            'MO': row[0],
            'EMP_NO': row[1],
            'RUNNING_QTY': row[2],
            'START_TIME': row[3],
            'MACHINE_START_DATE': row[4],
            'MACHINE_NAME': row[5]
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

@app.route('/showHistory', methods=['POST'])
def showHistory():
    port = request.json['name']
    print(port)
    today = date.today()
    print(today)
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(f"""
                SELECT 
                    id as ID,
                    port as PORT, 
                    fetched_ip as IP, 
                    status as STATUS, 
                    status_date_changed as STATUS_DATE_CHANGED
                FROM
                    fetched_ip_tbl 
                WHERE 
                    status_date_changed
                BETWEEN 
                    '{today} 06:00'::timestamp AND '{today} 18:00'::timestamp
                AND port = '{port}'
                ORDER BY id DESC
                    """ )
    result = cursor.fetchall()
    cursor.close()

    # Convert data to a list of dictionaries
    data = []
    for row in result:
        card = {
            'ID': row[0],
            'PORT': row[1],
            'IP': row[2],
            'STATUS': row[3],
            'STATUS_DATE_CHANGED': row[4]
        }
        data.append(card)

    return jsonify(data)



# @app.route('/update_ip_data', methods=['POST'])
# def update_ip_data():
#     status = request.json['message']
#     stop_date = request.json['stop_date']
#     sid = request.json['sid']
#     cur.execute(f"UPDATE public.fetched_ip_tbl SET status ='{status}', stop_time='{stop_date}' WHERE sid='{sid}'")
#     conn.commit()
#     return jsonify("Data updated successfully in the database")

@app.route('/stop_update', methods=['POST'])
def stop_update():
    try:
        machine_name = request.json["machine_name"]
        print(f"==>> machine_name: {machine_name}")
        remove_py = re.sub('.py', '', machine_name)
        client_ip = request.json["client_ip"]
        message = request.json["message"]
        sid = request.json["sid"]
        stop_date = request.json["stop_date"]
        fetchedGetDate = stop_date

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                'INSERT INTO public.fetched_ip_tbl (fetched_ip, status, sid, port, status_date_changed) VALUES (%s, %s, %s, %s, %s)',
                (client_ip, message, sid, remove_py, stop_date))
            conn.commit()
            return jsonify("Data inserted successfully into the database")
    except psycopg2.Error as e:
        error_message = "Error inserting data into the database: " + str(e)
        conn.rollback()
        return jsonify(error_message)



@app.route('/idle_update', methods=['POST'])
def function_idle_update():
    try:
        machine_name = request.json["machine_name"]
        print(f"==>> machine_name: {machine_name}")
        remove_py = re.sub('.py', '', machine_name)
        client_ip = request.json["client_ip"]
        status = request.json["status"]
        sid = request.json["sid"]
        idle_date = request.json['idle_date']
        
        
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                    'INSERT INTO public.fetched_ip_tbl (fetched_ip, status, sid, port, status_date_changed) VALUES (%s, %s, %s, %s, %s)',
                    (client_ip, status, sid, remove_py, idle_date))
            conn.commit()
            return jsonify("Data inserted successfully into the database")
    except Exception as e:
        return jsonify("Error updating data in the database: " + str(e))






# @app.route('/insert_ip_data', methods=['POST'])
# def insert_ip_data():
#     try:
#         machine_name = request.json["machine_name"]
#         remove_py = re.sub('.py', '', machine_name)
#         fetched_ip = request.json["fetched_ip"]
#         status = request.json["status"]
#         fetched_sid = request.json["fetched_sid"]
#         get_start_date = request.json["get_start_date"]

#         fetchedGetDate = get_start_date

#         # fetchedStartDate = get_card_details()

#         cur.execute(
#             "SELECT COUNT(port) FROM public.fetched_ip_tbl WHERE port = %s", (remove_py,))
#         count = cur.fetchone()[0]

#         if count > 0:
#             # data already exists, update
#             cur.execute("UPDATE public.fetched_ip_tbl SET status = %s, start_time = %s, port = %s WHERE  sid= %s",
#                         (status, fetchedGetDate, remove_py, fetched_sid))
#             conn.commit()  # commit the transaction
#             return jsonify("Data updated successfully in the database")
#         else:
#             # data doesn't exist, insert
#             cur.execute(
#                 "INSERT INTO public.fetched_ip_tbl (fetched_ip, status, sid, port, start_time) VALUES (%s, %s, %s, %s, %s)",
#                 (fetched_ip, status, fetched_sid, remove_py, fetchedGetDate))
#             conn.commit()  # commit the transaction
#             return jsonify("Data inserted successfully into the database")
#     except Exception as e:
#         conn.rollback()  # rollback the transaction if an error occurs
#         return jsonify("An error occurred while inserting/updating data")
    
@app.route('/insert_ip_data', methods=['POST'])
def insert_ip_data():
    try:
        # Fetch data from the request
        data = request.json
        machine_name = data["machine_name"]
        remove_py = re.sub('.py', '', machine_name)
        fetched_ip = data["fetched_ip"]
        status = data["status"]
        fetched_sid = data["fetched_sid"]
        get_start_date = data["get_start_date"]
        fetched_get_date = get_start_date

        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                "INSERT INTO public.fetched_ip_tbl (fetched_ip, status, sid, port, status_date_changed) VALUES (%s, %s, %s, %s, %s)",
                (fetched_ip, status, fetched_sid, remove_py, fetched_get_date))
            conn.commit()

        return jsonify("Data inserted successfully into the database")

    except psycopg2.Error as e:
        error_message = "Error inserting data into the database: " + str(e)
        conn.rollback()
        return jsonify(error_message)

    except Exception as e:
        error_message = "An error occurred: " + str(e)
        return jsonify(error_message)




@app.route('/request_data', methods=['POST'])
def request_data():
    data = request.get_json()
    socketio.emit('dataPassed', {'data': data})
    return jsonify(data=data)


@app.route('/getMachinesNamesApi')
def getMachinesNamesApi():
    url = 'http://cmms.teamglac.com/apimachine2.php'
    response = requests.get(url)
    data = json.loads(response.text)['data']
    
    classes = set()  # Create a set to store unique values
    
    for rec in data:
        classes.add(rec['CLASS']) 
    unique_classes = list(classes) 
    return jsonify(unique_classes)

@app.route('/insertController', methods=['POST'])
def insertController():
    controllerInput = request.form['controllerInput']
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                'INSERT INTO public.controllers_tbl (controller_name) VALUES (%s)',
                (controllerInput,))
            conn.commit()
            return jsonify("Data inserted successfully into the database")
    except psycopg2.Error as e:
        error_message = "Error inserting data into the database: " + str(e)
        conn.rollback()
        return jsonify(error_message)
    
@app.route('/insertMachinesToController')
def insertMachinesToController():
    cursor = conn.cursor()
    cursor.execute("""
                   SELECT
                    id,
                    fetched_ip,
                    status,
                    sid,
                    port,
                    machine_name,
                    area,
                    start_time,
                    stop_time
                   FROM public.fetched_ip_tbl ORDER BY id ASC 
                   """)
    rows = cursor.fetchall()
    machines = []
    for row in rows:
        start_date = row[7].strftime('%H:%M:%S') if row[7] is not None else None
        stop_date = row[8].strftime('%H:%M:%S') if row[8] is not None else None

        machines.append({
            'id': row[0],
            'fetched_ip': row[1], # Change 'machine_name' to 'text' for Select2 compatibility
            'status': row[2],
            'sid': row[3],
            'port': row[4],
            'machine_name': row[5],
            'area': row[6],
            'start_time': start_time,
            'stop_date': stop_date
        })
    cursor.close()
    return jsonify({'results': machines})  # Use 'results' instead of 'data' for Select2


@app.route('/processSelectedData', methods=['POST'])
def process_selected_data():
    selected_data = request.form.get('selectedDataArray')
    view_data = json.loads(selected_data)
    # print(f"==>> view_data: {view_data}")
    dataControllerID = int(request.form.get('dataControllerID').strip('"'))
    # print(f"==>> dataControllerID: {dataControllerID}")

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            for item in view_data:
                value1 = item['port']
                # print(f"==>> value1: {value1}")
                value2 = item['id']
                # print(f"==>> value2: {value2}")

                if not value1 or not value2:
                    # Either value1 or value2 is empty, skip this iteration
                    continue

                # Check if the combination of machine_id and controller_id already exists
                cur.execute(
                    "SELECT COUNT(*) FROM public.controller_with_machine_tbl WHERE machine_id = %s AND controller_id = %s",
                    (value2, dataControllerID))
                count = cur.fetchone()[0]

                if count > 0:
                    msg = 1
                    return jsonify({'data': msg})

                # Insert the data if it doesn't already exist
                cur.execute(
                    "INSERT INTO public.controller_with_machine_tbl (machine_id, controller_id) VALUES (%s, %s)",
                    (value2, dataControllerID))
                conn.commit()

            msg = 0
            return jsonify({'data': msg})

    except psycopg2.Error as e:
        error_message = "Error inserting data into the database: " + str(e)
        conn.rollback()
        return jsonify(error_message)

    
@app.route('/viewControllerResult', methods=['POST'])
def viewControllerResult():
    data_id = int(request.form.get('data_id').strip('"'))
    cursor = conn.cursor()
    cursor.execute("""
        SELECT
            a.id as ID,
            a.fetched_ip as FETCHED_IP,
            a.status as STATUS,
            a.sid as SID,
            a.port as PORT,
            a.machine_name as MACHINE_NAME,
            a.area as AREA,
            a.start_time as START_DATE,
            a.stop_time as STOP_DATE,
            b.remarks as REMARKS
        FROM (
            SELECT 
                a.id,
                a.status,
                a.start_time,
                a.stop_time,
                a.sid,
                a.fetched_ip,
                a.area,
                a.port,
                a.machine_name,
                b.controller_id
            FROM 
                public.fetched_ip_tbl a 
            LEFT JOIN 
                public.controller_with_machine_tbl b
            ON
                a.id = b.machine_id
        ) a
        LEFT JOIN 
            public.controllers_tbl b
        ON 
            b.id = a.controller_id
        WHERE 
            a.controller_id = %s
    """, (data_id,))
    rows = cursor.fetchall()
    result = []
    for row in rows:
        start_date = row[7].strftime('%H:%M:%S') if row[7] is not None else None
        stop_date = row[8].strftime('%H:%M:%S') if row[8] is not None else None
        
        result.append({
            'ID': row[0],
            'FETCHED_IP': row[1],
            'STATUS': row[2],
            'SID': row[3],
            'PORT': row[4],
            'MACHINE_NAME': row[5],
            'AREA': row[6],
            'START_DATE': start_date,
            'STOP_DATE': stop_date,
            'REMARKS': row[9]
        })
    cursor.close()
    return jsonify({'data': result})



@app.route('/controllersViewData')
def controllersViewData():
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, controller_name, remarks FROM controllers_tbl")
    rows = cursor.fetchall()
    machines = []
    for row in rows:
        machines.append({
            'id': row[0],
            'remarks': row[2],
            'controller_name': row[1]
        })
    cursor.close()
    return jsonify({'data': machines}) 


@app.route('/stop_update_data', methods=['POST'])
def stop_update_data():
    status = request.json['status']
    stop_date = request.json['stop_date']
    client_ip = request.json['client_ip']
    uid = request.json['uid']
    print(f"==>> uid: {uid}")
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(f"UPDATE public.machine_fetched_data_tbl SET machine_status= '{status}', stop_date= '{stop_date}' WHERE uid = {uid}")
            conn.commit()
            return jsonify("Data inserted successfully into the database")
    except Exception as e:
        conn.rollback()
        return jsonify("Error inserting data into the database: " + str(e))
    
@app.route('/pause_update_data', methods=['POST'])
def pause_update_data():
    status = request.json['status']
    get_pause_date = request.json['get_pause_date']
    client_ip = request.json['client_ip']
    uid = request.json['uid']
    print(f"==>> uid: {uid}")
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(f"UPDATE public.machine_fetched_data_tbl SET machine_status = '{status}', pause_date= '{get_pause_date}' WHERE uid = {uid}")
            conn.commit()
            return jsonify("Data inserted successfully into the database")
    except Exception as e:
        conn.rollback()
        return jsonify("Error inserting data into the database: " + str(e))
    
@app.route('/resume_update_data', methods=['POST'])
def resume_update_data():
    status = request.json['status']
    get_resume_date = request.json['get_resume_date']
    client_ip = request.json['client_ip']
    uid = request.json['uid']
    print(f"==>> uid: {uid}")
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            query = "UPDATE public.machine_fetched_data_tbl SET machine_status = %s, resume_idle = %s WHERE uid = %s"
            cur.execute(query, (status, get_resume_date, sid))
            conn.commit()
            return jsonify("Data inserted successfully into the database")
    except Exception as e:
        conn.rollback()
        return jsonify("Error inserting data into the database: " + str(e))
    

@app.route('/wakeup_update_data', methods=['POST'])
def wakeup_update_data():
    try:
        machine_name = request.json["machine_name"]
        print(f"==>> machine_name: {machine_name}")
        remove_py = re.sub('.py', '', machine_name)
        status = request.json['status']
        get_wakeup_date = request.json['get_wakeup_date']
        sid = request.json['sid']
        client_ip = request.json['client_ip']
        uid = request.json['uid']
        
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                    'INSERT INTO public.fetched_ip_tbl (fetched_ip, status, sid, port, status_date_changed) VALUES (%s, %s, %s, %s, %s)',
                    (client_ip, status, sid, remove_py, get_wakeup_date))
            conn.commit()
            return jsonify("Data inserted successfully into the database")
    except Exception as e:
        return jsonify("Error updating data in the database: " + str(e))



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


@socketio.on('custom_event')
def handle_custom_event(data):
    sid = data['sessionID']
    machine_name = data['machine_name_var']
    # Emitting a response back to the client
    socketio.emit('my_message', {'machine_name': machine_name}, to=sid)


@socketio.on('client_message')
def handle_client_message(data):
    message = data['message']
    filename_var = data['filename_var']
    socketio.emit('server_sample_response', {
        'message': message, 'filename_var': filename_var})


@socketio.on('client_connected')
def handle_client_connected(data):
    client_ip = request.remote_addr
    get_start_date = datetime.now()
    jsonStartDate = str(get_start_date)
    machine_name = data['machine_name']
    remove_py = re.sub('.py', '', machine_name)
    # Send a response event back to the client
    socketio.emit('server_response', {
        'message': 'CONNECTED', 'sid': request.sid, 'machine_name': remove_py, 'client_ip': client_ip, 'get_start_date': jsonStartDate})
    
@socketio.on('get_bandwidth')
def get_bandwidth():
    while True:
        # Retrieve the network statistics
        network_stats = psutil.net_io_counters(pernic=True)
        
        # Extract the relevant information for the graph
        graph_data = {
            'labels': list(network_stats.keys()),
            'data': [stats.bytes_sent for stats in network_stats.values()]
        }

        # Emit the graph data to the client
        emit('bandwidth', graph_data)

        # Delay between updates (e.g., 1 second)
        socketio.sleep(1)


@socketio.on('disconnect')
def handle_client_disconnected():
    # print(f"==>> filename: {filename}")
    # remove_py = re.sub('.py', '', filename)
    client_ip = request.remote_addr
    client_sid = request.sid
    get_stop_date = datetime.now()
    jsonStopDate = str(get_stop_date)
    # print(f"==>> jsonStopDate: {jsonStopDate}")
    # socketio.emit('server_response_dc', {
    #     'message': 'DISCONNECTED', 'sid': client_sid, 'client_ip': client_ip, 'stop_date': jsonStopDate})

# @socketio.on('message')
# def handle_message(message):
#     print('received message: ' + message)
#     socketio.emit('message','test')
    
@socketio.on('message')
def disconnect_event(data):
    machine_name = data['machine_name']
    client_ip = request.remote_addr
    client_sid = request.sid
    get_stop_date = datetime.now()
    jsonStopDate = str(get_stop_date)
    print(f"==>> jsonStopDate: {jsonStopDate}")
    socketio.emit('server_response_dc', {
        'message': 'DISCONNECTED', 'sid': client_sid,'machine_name': machine_name, 'client_ip': client_ip, 'stop_date': jsonStopDate})



@socketio.on('data')
def handle_data(data, stat_var, uID, result, get_start_date):
    # Assuming you have established a connection to the database and assigned it to the variable `conn`
    
    client_ip = request.remote_addr
    
    # Assuming there is only one nested dictionary inside `data`
    inner_data = next(iter(data.values()))
    
    EMP_NO = inner_data['EMP_NO']
    AREA_NAME = inner_data['AREA_NAME']
    CLASS = inner_data['CLASS']
    MACHINE_ID = inner_data['MACHINE_ID']
    MACHINE_NAME = inner_data['MACHINE_NAME']
    MO = inner_data['MO']
    RUNNING_QTY = inner_data['RUNNING_QTY']
    STATUS = inner_data['STATUS']
    SUB_OPT_NAME = inner_data['SUB_OPT_NAME']
    
    hris = f'http://hris.teamglac.com/api/users/emp-num?empno={EMP_NO}'
    
    response = requests.get(hris)
    data = json.loads(response.text)['result']
    
    if data == False:
        photo = "../static/assets/images/faces/pngegg.png"
    else:
        photo_url = data['photo_url']
        photo = f"http://hris.teamglac.com/{photo_url}"
        
    start_time = str(get_start_date)
    
    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(
                'SELECT * FROM machine_fetched_data_tbl WHERE emp_no = %s AND start_date = %s',
                (EMP_NO, start_time)
            )
            existing_data = cur.fetchone()

            if existing_data:
                # Update the existing record
                cur.execute(
                    'UPDATE machine_fetched_data_tbl SET area_name = %s, class = %s, machine_id = %s, machine_name = %s, mo = %s, running_qty = %s, status = %s, sub_opt_name = %s, photo = %s WHERE uid = %s',
                    (AREA_NAME, CLASS, MACHINE_ID, MACHINE_NAME, MO, RUNNING_QTY, STATUS, SUB_OPT_NAME, photo, uID)
                )
                conn.commit()
                return jsonify("Data updated successfully in the database")
            else:
                # Insert a new record
                cur.execute(
                    'INSERT INTO machine_fetched_data_tbl (area_name, class, emp_no, machine_id, machine_name, mo, running_qty, status, sub_opt_name, photo, start_date, uid, machine_status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (AREA_NAME, CLASS, EMP_NO, MACHINE_ID, MACHINE_NAME, MO, RUNNING_QTY, STATUS, SUB_OPT_NAME, photo, start_time, uID, stat_var)
                )
                conn.commit()
                return jsonify("Data inserted successfully into the database")
    except psycopg2.Error as e:
        error_message = "Error inserting/updating data in the database: " + str(e)
        conn.rollback()
        return jsonify(error_message)


@socketio.on('stop_data')
def handle_data(stat_var, uID, get_stop_date):
    print('uid', uID)
    client_ip = request.remote_addr
    stop_date = str(get_stop_date)
    socketio.emit('stop_date', {
        'status': 'STOP', 'uid':uID, 'client_ip': client_ip, 'stop_date':stop_date})
    
@socketio.on('pause_data')
def handle_pause_data(stat_var, uID, get_pause_date):
    print('uid', uID)
    client_ip = request.remote_addr
    get_pause_date = str(get_pause_date)
    socketio.emit('pause_date', {
        'status': 'PAUSE', 'uid':uID, 'client_ip': client_ip, 'get_pause_date':get_pause_date})
    
@socketio.on('resume_data')
def handle_resume_data(stat_var, uID, get_resume_date):
    print('uid', uID)
    client_ip = request.remote_addr
    get_resume_date = str(get_resume_date)
    socketio.emit('resume_date', {
        'status': 'RESUME', 'uid':uID, 'client_ip': client_ip, 'get_resume_date':get_resume_date})
    
@socketio.on('wakeup_data')
def handle_wakeup_data(stat_var, uID, get_wakeup_date, remove_py):
    print('uid', uID)
    client_ip = request.remote_addr
    get_wakeup_date = str(get_wakeup_date)
    socketio.emit('wakeup_date', {
        'status': 'STARTED', 'uid':uID, 'machine_name': remove_py, 'sid': request.sid, 'client_ip': client_ip, 'get_wakeup_date':get_wakeup_date})
    
@socketio.on('idle_data')
def handle_idle_data(data):
    machine_name = data['machine_name']
    client_ip = request.remote_addr
    client_sid = request.sid
    stat_var = data['stat_var']
    uID = data['uID']
    get_idle_date = data['get_idle_date']
    socketio.emit('client_idle', {
        'message': 'IDLE', 'uid': uID, 'machine_name': machine_name, 'sid': request.sid, 'client_ip': client_ip, 'idle_date':get_idle_date})



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
    return render_template('controllers-program.html')


@app.route('/all_device')
@login_required
def all_device():
    return render_template('controllers-area-view.html')


@app.route('/configuration')
@login_required
def configuration():
    return render_template('configuration-setup.html')

@app.route('/graph')
@login_required
def graph():
    return render_template('graph.html')


@app.route('/machine_uph')
@login_required
def machine_uph():
    return render_template('machine_uph.html')


@app.route('/captured_data')
@login_required
def captured_data():
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
    socketio.run(app, host='10.0.2.150', port=8095, debug=True)