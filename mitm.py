import socket
import threading

class Proxy:
    def __init__(self, listen_host: str, listen_port: int, server_host: str, server_port: int):
        self.listen_host = listen_host
        self.listen_port = listen_port
        self.server_host = server_host
        self.server_port = server_port

        self.listener_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.listener_sock.bind((self.listen_host, self.listen_port))

        self.server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.client_addr = None

    def listen_from_client(self):
        while True:
            data, addr = self.listener_sock.recvfrom(4096)
            self.client_addr = addr
            print(f"[CLIENT -> SERVER] {addr}: {data.hex()}")

            self.server_sock.sendto(data, (self.server_host, self.server_port))

    def listen_from_server(self):
        while True:
            data, _ = self.server_sock.recvfrom(4096)
            print(f"[SERVER -> CLIENT]: {data.hex()}")
            if self.client_addr:
                self.listener_sock.sendto(data, self.client_addr)

    def run(self):
        threading.Thread(target=self.listen_from_client, daemon=True).start()
        threading.Thread(target=self.listen_from_server, daemon=True).start()
        print(f"[*] Proxy listening on {self.listen_host}:{self.listen_port}")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            print("\n[!] Exiting...")


def main():
    proxy = Proxy(listen_host="0.0.0.0", listen_port=4800,
                      server_host="37.10.191.194", server_port=4800)
    proxy.run()

if __name__ == "__main__":
    main()