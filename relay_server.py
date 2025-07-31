import socket
import threading

host = '0.0.0.0'
port = 8000
clients = []

def forward(source, dest):
    try:
        while True:
            data = source.recv(4096)
            if not data:
                break
            dest.sendall(data)
    except:
        pass
    finally:
        source.close()
        dest.close()

def handle(conn):
    clients.append(conn)
    if len(clients) == 2:
        threading.Thread(target=forward, args=(clients[0], clients[1]), daemon=True).start()
        threading.Thread(target=forward, args=(clients[1], clients[0]), daemon=True).start()

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((host, port))
    s.listen(2)
    print(f'[*] Listening on {host}:{port}')
    while True:
        conn, addr = s.accept()
        print(f'[+] Connected: {addr}')
        threading.Thread(target=handle, args=(conn,), daemon=True).start()
