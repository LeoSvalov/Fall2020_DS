import socket
import tqdm
import os
from threading import Thread


# device's IP address
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8080

# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"


class Listener(Thread):
    def __init__(self, sock, addr):
        super().__init__(daemon=True)
        self.sock = sock
        self.addr = addr

    def already_exist(self, filename):
        return os.path.isfile(f"{filename}")

    def make_copy(self, filename, n):
        components = filename.split(".")
        if(len(components) == 1):
            return f"{filename}_copy{n}"
        head, *tail = components
        tail = ".".join(tail)
        return f"{head}_copy{n}.{tail}"

    # to validate that the file alerady was sent --> make 'copy' suffix
    def _get_valid_filename(self, filename):
        if(not self.already_exist(filename)):
            return filename
        n = 1
        while self.already_exist(self.make_copy(filename, n)):
            n += 1

        return self.make_copy(filename, n)

    def run(self):
        received = self.sock.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        filename = os.path.basename(filename)
        filename = self._get_valid_filename(filename)

        file_path = f"{filename}"
        filesize = int(filesize)

        # start receiving the file from the socket and writing to the file stream
        progress = tqdm.tqdm(range(filesize), f"[*] Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024, leave=False)
        with open(file_path, "wb") as f:
            for _ in progress:
                # read from the socket
                bytes_read = self.sock.recv(BUFFER_SIZE)
                if not bytes_read:
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                # update the progress bar
                progress.update(len(bytes_read))

            print(f"[+] File received: {filename}")
            self._close()

    def _close(self):
        self.sock.close()
        print(f"[+] {self.addr[0]}:{self.addr[1]} is disconnected.")


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((SERVER_HOST, SERVER_PORT))
    sock.listen()

    print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

    while True:
        con, addr = sock.accept()
        print(f"[+] {addr[0]}:{addr[1]} is connected.")
        Listener(con, addr).start()


if __name__ == "__main__":
    main()