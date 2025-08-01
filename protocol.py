import socket
import struct

"""
message_type   - 1 byte
message_length - 3 bytes
reserved       - 4 bytes
field1         - 4 bytes
field2         - 4 bytes
mac_address    - 4 bytes
ip_address     - 4 bytes

Total of at least 24 bytes
MAC is usually 6 bytes but it strips first two bytes. 
11:22:33:44:55 -> 33:44:55
"""

class Proto:

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


    def parse(self, data, debug = False):

        message_type, message_length, reserved, field1, field2, mac_address, ip_address = struct.unpack_from("!B3s4s4s4s4s4s", data)

        self.message_type = message_type
        self.message_length = message_length
        self.reserved = reserved
        self.field1 = field1
        self.field2 = field2
        self.mac_address = mac_address
        self.ip_address = ip_address

        if debug:
            print(data)