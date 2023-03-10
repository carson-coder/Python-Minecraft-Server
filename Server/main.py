import threading
import socket
import logging
import json

from .classes import *

info = {
    "enforcesSecureChat":True,
    "description":{
        "text":"A Minecraft Server",
        "color": "red"
    },
    "players":{
            "max":20,
            "online":0
    },
    "version":{
        "name":"The world is totally on fire",
        "protocol":760
    }
}

def func(conn, addr, conn_data: Connection):
    running = True
    packets_sent = 1
    logging.info(f"Connection from {addr[0]}:{addr[1]}")
    while running:
        #try:
        data = conn.recv(1024)
        #except:
            #running = False
            #break
        if data.__len__() != 0:
            logging.debug(f"Receved Data: {data}")
            packets = conn_data.parse_packets(data)
            for i in packets:
                logging.debug(f"Packet {packets_sent}: {i.id}, {i.data}")
                packets_sent += 1
                
                send_data = b""
                
                if i.id == 0 and i.data.__len__() == 0:
                    packet = Packet()
                    packet.create_packet(bytes(1), [String(json.dumps(info))])
                    send_data += packet.raw_data
                elif i.id == 1:
                    logging.debug(f"Receved ping with long {Long(i.data)}")
                    send_data += i.raw_data
                logging.debug(f"Sending; {send_data}")
                size = len(send_data)
                swap = False
                if swap:
                    send_data = int.from_bytes(send_data, 'big')
                    send_data = send_data.to_bytes(size, "little")
                conn.send(send_data)
    conn.close()

server = Connection("Server", 25565)
server.Start(func)