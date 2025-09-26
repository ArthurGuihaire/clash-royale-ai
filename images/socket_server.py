import socket, struct, time, pickle, subprocess, threading

def send_image(connection):
    with open("/dev/shm/screen.png", 'rb') as f:
        img_data = f.read()

    connection.sendall(struct.pack('>Q', len(img_data)))
    connection.sendall(img_data)

HOST = '0.0.0.0'
PORT = 2361
PING_PACKET = " ".encode()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()
print("server started")

conn, addr = server.accept()
with conn:
    for i in range(20):
        conn.recv(1)
        conn.sendall(PING_PACKET)

    conn.sendall(pickle.dumps(time.time()))

    while True:
        subprocess.run(["adb", "shell", "input", "tap", "366", "109"])
        conn.recv(1)
        time.sleep(1)
        subprocess.run(["adb", "shell", "input", "tap", "366", "109"])
        conn.sendall(PING_PACKET)

        while True:
            time_to_send = pickle.loads(conn.recv(21))
            if not time_to_send: break
            time.sleep(time_to_send - time.time())
            subprocess.run(["bash", "android-screenshot.sh"])
            threading.Thread(target=send_image, args=(conn,)).start()
