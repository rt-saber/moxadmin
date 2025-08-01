# Moxa NPort Administrator security research

I wanted to dig into this protocol to kinda understand how it works.
I reverse engineered the NPort Aministrator executable but I also wanted to dig into the networking part more actively.

This repo is messy because only meant to keep some notes

My idea was to make a server listening on UDP port 4800, then connect to it using NPort Administrator.

This way I could actively see messages sent from the client to devices, I could also send a similar packet to a legitimate device and see what it answers as well as sending it back to client.

Client: b'\x01\x00\x00\x08\x00\x00\x00\x00'
Device: b'\x81\x00\x00\x18\x00\x00\x00\x00\x10Q\x00\x80\x10Q\x00\x90\xe8,\xa8Y\xc0\xa8\x00\x07'
Client: b'\x01\x00\x00\x14\x00\x00\x00\x00\x10Q\x00\x80\x10Q\x00\x90\xe8,\xa8Y'

```
offset: |0|1-3|4-7|8-11|12-15|16-21|22-25
meaning |message_type|len|?|?|?|mac_address|ip
```
