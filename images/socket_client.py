import socket, struct, time, pickle, io, subprocess
from PIL import Image

async def recieve_image(client_socket):
    size_data = client_socket.recv(8)
    print(len(size_data))
    img_size = struct.unpack('>Q', size_data)[0]

    received = b""
    while len(received) < img_size:
        chunk = client_socket.recv(4096)
        if not chunk: break
        received += chunk

    img = Image.open(io.BytesIO(received))
    return img

    '''with open("/dev/shm/image.png", 'wb') as f:
        f.write(received)'''

HOST = '192.168.4.88'
PORT = 2361
ping_packet = " ".encode()

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

num_pings = 20
send_time = time.time()
for i in range(num_pings):
    client_socket.sendall(ping_packet)
    client_socket.recv(1)

time_pigsies = pickle.loads(client_socket.recv(21))
ping = (time.time() - send_time) / (num_pings * 2)
time_offset = time_pigsies - time.time() + ping

while True:
    subprocess.run(["sudo", "waydroid", "shell", "input", "tap", "366", "109"])
    time.sleep(0.75)
    subprocess.run(["sudo", "waydroid", "shell", "input", "tap", "200", "350"])
    time.sleep(0.75)
    subprocess.run(["sudo", "waydroid", "shell", "input", "tap", "400", "460"])
    client_socket.sendall(ping_packet)
    client_socket.recv(1)
    time.sleep(8)


client_socket.close()
