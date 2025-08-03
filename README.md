# Moxa NPort Administrator security research

I wanted to dig into this protocol to kinda understand how it works.
I reverse engineered the NPort Aministrator executable but I also wanted to dig into the networking part more actively.

This repo is messy because only meant to keep some notes

My idea was to make a server listening on UDP port 4800, then connect to it using NPort Administrator.

This way I could actively see messages sent from the client to devices, I could also send a similar packet to a legitimate device and see what it answers as well as sending it back to client.

Using struct is not ideal way to handle packets here, the packet structure varies too much.
While for some packets MAC would 4 bytes (usually 6 bytes but first 2 bytes are ignored in this protocol) starting at offset 16 for some packets it would be at 22 for some others.

Instead we know that in some packets:

- First byte -> message type
- Second-to-third bytes -> Packet length
- Last 4 bytes -> IP address
- 4 bytes preceding the IP -> MAC address

the last 4 bytes is the IP address

---

`fake_client.py` -> This simulate the legitimate Moxa NPort Administrator client by sending similar packets to legitimate devices

`fake_server.py` -> This simulate a legitimate Moxa NPort device by sending back to client packets a real Moxa device would send

`protocol.py`    -> This is where most of the job is done

---

## Message type 144:

Device name at offset 20, remaining bytes should all be null?
Is length always 60?
Is device name always at offset 20?
What's the bytes between length and device name?

