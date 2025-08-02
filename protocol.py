import socket
import struct

"""
message_type   - 1 byte
message_length - 3 bytes
???
mac_address    - -8 bytes
ip_address     - -4 bytes

Total of at least 24 bytes
MAC is usually 6 bytes but first two bytes are not used. 
11:22:33:44:55 -> 33:44:55

At the moment I am not sure what ip_address is used for, client does not seem to rely on it to display device's IP address.
"""

class Protocol:

    def __init__(self):
        
        self.fields = [
            "message_type",
            "message_length",
            "reserved",
            "field1",
            "field2",
            "mac_address",
            "ip_address"
        ]

        self.message_type = None
        self.message_length = None
        self.reserved = None
        self.field1 = None
        self.field2 = None
        self.mac_address = None
        self.ip_address = None

        self.messages = {
            1: b"\x01\x00\x00\x08\x00\x00\x00\x00",
            2: b"\x16\x00\x00\x14\x00\x00\x00\x00\x10\x51\x00\x80\x10\x51\x00\x90\xe8\xc8\x73\xb0",
            3: b"\x10\x00\x00\x14\x00\x00\x00\x00\x10Q\x00\x80\x10Q\x00\x90\xe8\xc8s\xb0",
            4: b"NOT_IMPLEMENTED"
        }


    def parse(self, data, debug = False) -> None:

        """
        message_type, message_length_raw, reserved, field1, field2, mac_address, ip_address = struct.unpack_from("!B3s4s4s4s4s4s", data)

        self.message_type = message_type
        self.message_length = message_length_raw
        self.reserved = reserved
        self.field1 = field1
        self.field2 = field2
        self.mac_address = mac_address
        self.ip_address = ip_address
        """

        self.message_type = data[0]

        if self.message_type == 129:

            self.message_length = data[1:4]
            self.mac_address_raw = data[-8:-4]
            self.ip_address_raw = data[-4:]

            self.message_length = int.from_bytes(self.message_length, "big")

            self.mac_address = ":".join(f"{b:02x}" for b in self.mac_address_raw)
            self.ip_address = ".".join(str(b) for b in self.ip_address_raw)

            self.unknown = data[4:-8]

            message = f"Type -> {self.message_type}\n"
            message += f"Length -> {self.message_length}\n"
            message += f"Unknown -> {self.unknown.hex()}\n"
            message += f"MAC -> {self.mac_address}\n"
            message += f"IP -> {self.ip_address}\n"

            return message

        elif self.message_type == 150:
            
            self.message_length = data[1:4]
            self.message_length = int.from_bytes(self.message_length, "big")

            self.unknown1 = data[4:16]

            self.mac_address_raw = data[16:20]
            self.mac_address = ":".join(f"{b:02x}" for b in self.mac_address_raw)

            self.unknown2 = data[20:]

            message = f"Type -> {self.message_type}\n"
            message += f"Length -> {self.message_length}\n"
            message += f"Unknown1 -> {self.unknown1.hex()}\n"
            message += f"MAC -> {self.mac_address}\n"
            message += f"Unknown2 -> {self.unknown2.hex()}\n"

            return message
        
        elif self.message_type == 144:

            self.message_length = data[1:4]
            self.message_length = int.from_bytes(self.message_length, "big")

            self.unknown1 = data[4:16]

            self.mac_address_raw = data[16:20]
            self.mac_address = ":".join(f"{b:02x}" for b in self.mac_address_raw)

            self.device_name = data[20:]
            self.device_name = data[20:].split(b"\x00")[0]
            self.padding = b"\x00".join(data[20:].split(b"\x00")[1:])

            message = f"Type -> {self.message_type}\n"
            message += f"Length -> {self.message_length}\n"
            message += f"Unknown1 -> {self.unknown1.hex()}\n"
            message += f"MAC -> {self.mac_address}\n"
            message += f"Device name -> {self.device_name}\n"
            message += f"Padding -> {self.padding.hex()}\n"

            return message

        else:

            self.message_length = data[1:4]
            self.message_length = int.from_bytes(self.message_length, "big")

            message = f"Type -> {self.message_type}\n"
            message += f"Length -> {self.message_length}\n"

            return message

    
    def message(self, id: int) -> bytes:

        return self.messages[id]