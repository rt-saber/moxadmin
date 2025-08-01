# Moxa NPort Administrator security research

I wanted to dig into this protocol to kinda understand how it works.
I reverse engineered the NPort Aministrator executable but I also wanted to dig into the networking part more actively.

This repo is messy because only meant to keep some notes

My idea was to make a server listening on UDP port 4800, then connect to it using NPort Administrator.

This way I could actively see messages sent from the client to devices, I could also send a similar packet to a legitimate device and see what it answers as well as sending it back to client.

## protocol

```
offset: |0|1-3|4-7|8-11|12-15|16-21|22-25
meaning |message_type|len|?|?|?|mac_address|ip
```


## packet order (msg_type)

client -> 1
device -> 129
client -> 22
device -> 150