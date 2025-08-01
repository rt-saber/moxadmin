import time
import socket
import struct

class Proto:
    def __init__(self, host: str, port: int):
        
        self.host = host
        self.port = port
        self.peer = (host, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.message = {
            "1": b"\x01\x00\x00\x08\x00\x00\x00\x00",
            "2": b"\x16\x00\x00\x14\x00\x00\x00\x00\x10\x51\x00\x80\x10\x51\x00\x90\xe8\xc8\x73\xb0",
            "3": b"\x10\x00\x00\x14\x00\x00\x00\x00\x10Q\x00\x80\x10Q\x00\x90\xe8\xc8s\xb0"
        }

    def parser(self, message: bytes, debug=False) -> None|str:

        msg_type, length_bytes_raw, reserved, field1, field2, mac_raw, ip_raw = struct.unpack_from("!B3s4s4s4s4s4s", message)
        length_bytes = int.from_bytes(length_bytes_raw, "big")
        mac = ':'.join(f"{b:02x}" for b in mac_raw)
        ip = '.'.join(str(b) for b in ip_raw)

        if debug:
            return f"|{msg_type}|{length_bytes}|"


    def send(self, message: bytes) -> None:

        self.sock.sendto(message, self.peer)
        print(f"<- {message}")

    def receive(self) -> int:

        data, addr = self.sock.recvfrom(4096)
        msg_type, length_bytes_raw, reserved, field1, field2, mac_raw, ip_raw = struct.unpack_from("!B3s4s4s4s4s4s", data)

        parsed = self.parser(data, debug=True)

        length_bytes = int.from_bytes(length_bytes_raw, "big")
        mac = ':'.join(f"{b:02x}" for b in mac_raw)
        ip = '.'.join(str(b) for b in ip_raw)

        print(f"-> {data}")
        if parsed:
            print(parsed)
        #print(f"↳ {msg_type}|{length_bytes}|?|?|?|{mac}|{ip}\n")

        return msg_type

def main() -> None:

    proto = Proto("37.10.191.194", 4800)

    
    proto.send(proto.message["1"])
    data = proto.receive()

    if data == 129:
        proto.send(proto.message["2"])
    
    data = proto.receive()

    if data == 150:
        proto.send(proto.message["3"])
    
    data = proto.receive()

if __name__ == "__main__":
    main()
