# Torchlight 2 Lan Game Server Tool

[![Version](https://img.shields.io/github/release/jhj0411jhj/torchlight2_lan_game_server_tool.svg)](https://github.com/jhj0411jhj/torchlight2_lan_game_server_tool/releases)

A message forwarding tool for Torchlight 2 lan game.

Only the game host needs to start this tool.

## Who Needs the Tool

If your friends cannot connect to you on Torchlight 2 official Internet server,
and you want to play the game together in LAN mode. 
You set up a VLAN, but you cannot see each other in game, because:
+ The game host broadcast messages are not sent to the correct interface.
+ Broadcast packets are filtered by your LAN/VLAN.

This tool forwards message that contains the server info directly to your friends, 
so they can see and join the room you created.


## Download

[Click here](https://github.com/jhj0411jhj/torchlight2_lan_game_server_tool/releases)
to open Github release page and **download EXE file**.


## Usage

1. [Set up a VLAN](#addition-set-up-a-vlan) or make sure all clients have direct IPs.
2. Host a LAN game and start this tool. Enter all client IPs.
   The tool will send room info to clients automatically.
3. After all clients are connected, you can choose to close this tool.


You can start the tool by either **opening the EXE file** or using command line:
```
python torchlight2_lan_server.py
```

The EXE file is packaged with `pyinstaller`:
```
pyinstaller -F torchlight2_lan_server.py
```


## Bug Report

If you encounter any bug, please [fill an issue](https://github.com/jhj0411jhj/torchlight2_lan_game_server_tool/issues).


## Addition: Set Up a VLAN

Here I recommend 2 free software to set up a VLAN on Internet 
(**WITHOUT ANY WARRANTY**):

+ ZeroTier: <https://www.zerotier.com/>
+ Pugongying (Free for 3 clients): <https://pgy.oray.com/>
