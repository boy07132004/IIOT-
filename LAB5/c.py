#!/usr/bin/env python3
"""
@argv[1]: [server address]
@argv[2]: [server name]
"""

import signal
import sys
from bluetooth import *


# End read handler
def end_read(signal, frame):
    global read_on
    print('\n[INFO] Ctrl+C captured, to shutdown service please press [enter].')
    read_on = False


# Env init
A = sys.argv[1]
ADDRESS = A[1:len(A)-1]
N = sys.argv[2]
SERVER_NAME = N[1:len(N)-1]
UUID = '94f39d29-7d6d-437d-973b-fba39e49d4ee'
read_on = True


# Add terminator
signal.signal(signal.SIGINT, end_read)


# Search service
print('[INFO] Search service on %s' % ADDRESS)
service_matches = find_service(uuid=UUID, address=ADDRESS)

if len(service_matches) == 0:
    print('[INFO] No service found, exiting client =(')
    sys.exit(0)


# Get/show service info
first_match = service_matches[0]
port = first_match['port']
name = first_match['name']
host = first_match['host']

if name != SERVER_NAME:
    print('[INFO] Server name error, exiting client =(')
    sys.exit(0)

print('[INFO] Connecting to [%s]:%s' % (name, host))


# Create the client socket
sock = BluetoothSocket(RFCOMM)
sock.connect( (host, port) )

print('[INFO] Connected, enjoy.')


# Start reading
while read_on:
    data = input('[SEND] >> ')
    if len(data) == 0: break

    sock.send(data)
    print('[RECV] ' + sock.recv(1024).decode('ascii'))


# End reading
sock.close()
