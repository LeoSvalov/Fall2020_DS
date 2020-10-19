import socket
import tqdm
import os
import sys

SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096  # send 4096 bytes each time step


def get_params():
    if len(sys.argv) != 4:  # 1) script 2) file to transfer 3) ip 4) port
        print('Error! Invalid num of parameters!')
    else:
        return sys.argv[1], sys.argv[2], int(sys.argv[3])


filename, host, port = get_params()

filesize = os.path.getsize(filename)

# create the client socket
s = socket.socket()

print(f"[*] Connecting to {host}:{port}")
s.connect((host, port))
print("[*] Connected.")

# send the filename and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

# start sending the file
progress = tqdm.tqdm(range(filesize), f"[*] Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024,leave=False)

with open(filename, "rb") as f:
    for _ in progress:
        # read the bytes from the file
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
            # file transmitting is done
            break
        # we use sendall to assure transimission in
        # busy networks
        s.sendall(bytes_read)
        # update the progress bar
        progress.update(len(bytes_read))
# close the socket

print(f"[+] File {filename} was sent.")
s.close()
