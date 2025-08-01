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
            "2": b""
        }

    def send(self, message: bytes) -> None:

        self.sock.sendto(message, self.peer)
        print(f"Sent: {message} to {self.peer}")

    def receive(self) -> int:

        data, addr = self.sock.recvfrom(4096)
        msg_type, length_bytes_raw, reserved, field1, field2, mac_raw, ip_raw = struct.unpack_from("!B3s4s4s4s4s4s", data)

        length_bytes = int.from_bytes(length_bytes_raw, "big")
        mac = ':'.join(f"{b:02x}" for b in mac_raw)
        ip = '.'.join(str(b) for b in ip_raw)

        print(f"\n{addr[0]}:{addr[1]} -> {data}")
        print(f"↳ {msg_type}|{length_bytes}|?|?|?|{mac}|{ip}\n")

        if msg_type == 129:

            message_type = (1).to_bytes(1, "big")
            length = (20).to_bytes(3, "big")
            reserved = (0).to_bytes(4, "big")
            field1 = field1
            field2 = field2
            mac_raw = mac_raw

            self.message["2"] = message_type + length + reserved + field1 + field2 + mac_raw

        return msg_type

def main() -> None:

    proto = Proto("37.10.191.194", 4800)

    
    proto.send(proto.message["1"])
    data = proto.receive()

    if data == 129:
        for loop in range(4):
            proto.send(proto.message["2"])
            data = proto.receive()

if __name__ == "__main__":
    main()
