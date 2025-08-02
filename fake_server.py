import socket

from protocol import Protocol

class Server:
    def __init__(self, host: str, port: int, protocolObj):
        
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

        self.protocol = protocolObj 
        self.message = protocolObj.message_server

    def send(self, message: bytes, addr, debug = False) -> None:

        self.sock.sendto(message, addr)
        if debug:
            print(f"-> {message}")

    def listen(self) -> None:
        
        while True:
            data, addr = self.sock.recvfrom(4096)
            print(f"<- {data}")
            parsed = self.protocol.parse_client(data)
            print(parsed)

            if self.protocol.message_type == 1 and self.protocol.message_length == 8:
                self.send(self.message(1), addr)

            if self.protocol.message_type == 1 and self.protocol.message_length == 20:
                self.send(self.message(2), addr)


def main() -> None:

    protocol = Protocol()
    server = Server("0.0.0.0", 4800, protocol)
    server.listen()

if __name__ == "__main__":
    main()
