import socket
import base64

class Proto:
    def __init__(self, host: str, port: int):
        
        self.host = host
        self.port = port

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.host, self.port))

    def receive(self) -> None:
        
        while True:
            data, addr = self.sock.recvfrom(4096)
            print(f"{addr[0]}:{addr[1]} -> {data}")
            if data == b'\x01\x00\x00\x08\x00\x00\x00\x00':
                message = b'\x81\x00\x00\x18\x00\x00\x00\x00\x10Q\x00\x80\x10Q\x00\x90\xe8,\xa8Y\xc0\xa8\x00\x07'
                self.sock.sendto(message, addr)

def main() -> None:

    proto = Proto("0.0.0.0", 4800)
    proto.receive()

if __name__ == "__main__":
    main()
