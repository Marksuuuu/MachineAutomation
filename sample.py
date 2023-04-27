from flask import Flask, jsonify
import configparser
import paramiko

app = Flask(__name__)

# @app.route("/establish-ssh-connection")
# def establish_ssh_connection():
#     config = configparser.ConfigParser()
#     config.read("connection_config.ini")

#     connection_name = "192.168.1.36" # replace with the actual connection name
#     remote_ip_address = config.get(connection_name, "remote_ip_address")
#     username = config.get(connection_name, "username")
#     password = config.get(connection_name, "password")
#     port = config.getint(connection_name, "port")

#     try:
#         client = paramiko.SSHClient()
#         client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#         client.connect(hostname=remote_ip_address, port=port, username=username, password=password)
#         # do something with the client
#         print('SSH connection established successfully')
#         client.close()
#         return "<span>SSH connection established successfully.</span>"
#     except paramiko.AuthenticationException:
#         print('Authentication failed')
#         return  "<span>Authentication failed</span>"
#     except paramiko.SSHException as e:
#         print(f'Unable to establish SSH connection: {e}')
#         return f"</span>Unable to establish SSH connection: {e}</span>"

@app.route('/config')
def get_config():
    config = configparser.ConfigParser()
    config.read('connection_config.ini')

    data = []
    for section in config.sections():
        if config.has_option(section, 'username') and config.has_option(section, 'password') and config.has_option(section, 'port'):
            username = config.get(section, 'username')
            password = config.get(section, 'password')
            port = config.get(section, 'port')
            data.append({'Ip Address': section, 'username': username, 'password': password, 'Port': port})

    return jsonify(data)
    
if __name__ == '__main__':
    app.run(host="localhost", port=8083, debug=True)
    
#     remote_ip_address
# username
# password
# port