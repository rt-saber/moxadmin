import time
import socket
import struct

from protocol import Protocol

class Client:

    def __init__(self, host, port, protocolObj):
        self.packet_stack = []
        self.host = host
        self.port = port
        self.peer = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.protocol = protocolObj 
        self.message = protocolObj.message_client


    def send(self, message: bytes, debug = False) -> None:

        self.sock.sendto(message, self.peer)
        if debug:
            print(f"-> {message}")


    def connect(self) -> None:
        
        self.send(self.message(1))

        while True:
            data, addr = self.sock.recvfrom(4096)
            print(f"<- {data}")
            parsed = self.protocol.parse_server(data)
            print(parsed)

            if self.protocol.message_type == 129:
                self.send(self.message(2))

            if self.protocol.message_type == 150:
                self.send(self.message(3))

            if self.protocol.message_type == 144:
                self.send(self.message(4))


def main() -> None:

    protocol = Protocol()
    client = Client("37.10.191.194", 4800, protocol)
    client.connect()

if __name__ == "__main__":
    main()