#! /usr/bin/env python3
# serialize communications with Zero motorcycle over Bluetooth
# the bike can handle only one connection at a time, so we queue up requests for data

import atexit
import logging
import os
import pickle
import socket
import time
import zerobt

port=4000
header_size=10

# debugging messages (comment to turn off messages)
#logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(message)s')
#logging.basicConfig(filename='/tmp/outputlog.txt', level=logging.DEBUG, format='%(asctime)s - %(message)s')

# clean up nicely
def cleanup():
   logging.debug('exiting')
   socket_server.close()
   if socket_bike:
      socket_bike.close()
   if socket_client:
      socket_client.close()

# format client packet with size header
def client_packet(data):
   msg=pickle.dumps(data)
   msg=bytes(f'{len(msg):<{header_size}}', 'ascii')+msg
   return msg

# function for clients
def read(cmd, host=socket.gethostname()):
   logging.debug('sending command')
   sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
      sock.connect((host, port))
   except ConnectionRefusedError:
      # server is down, try to start it
      log='/tmp/'+os.path.splitext(os.path.basename(__file__))[0]+'.txt'
      os.system('python3 '+__file__+' &> '+log+' &')
      time.sleep(5)
      sock.connect((host, port))
   sock.send(bytes(cmd, 'ascii'))
   packet=b''
   header=True
   while True:
      logging.debug('reading')
      data=sock.recv(1024)
      if header:
         packet_length=int(data[:header_size])
         header=False
         logging.debug('packet size: %d', packet_length)
      packet+=data
      if len(packet)-header_size == packet_length:
         logging.debug('packet received')
         sock.close()
         return pickle.loads(packet[header_size:])

def server():
   global socket_server, socket_bike, socket_client

   # create server socket
   socket_server=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   socket_server.bind(('', port))
   socket_server.settimeout(120)
   socket_server.listen(64)

   socket_client=None
   socket_bike=None
   atexit.register(cleanup)
   while True:
      logging.debug('looping')
      try:
         # wait for connection from client until timeout
         socket_client, address=socket_server.accept()

         # we got a command, set timeout so client doesn't DDOS us
         logging.debug('connection from %s', address)
         socket_client.settimeout(30)
         cmd=socket_client.recv(1024).decode('ascii').strip()
         logging.debug('command:', cmd)
         if cmd not in zerobt.cmd_packets.keys():
            # not a valid command
            logging.debug('invalid command')
            socket_client.send(client_packet('invalid command'))
         else:
            # echo command to bike
            if not socket_bike:
               logging.debug('connecting to bike')
               socket_bike=zerobt.connect_to_bike()
            # read and decode packet from bike
            logging.debug('reading packet')
            packet=zerobt.read_packet(socket_bike, cmd)
            # send results to client
            logging.debug('sending results')
            socket_client.send(client_packet(packet))
         logging.debug('done')
         socket_client.close()
         socket_client=None
      except socket.timeout:
         # a socket timed out, but we don't know which one
         logging.debug('socket timeout')
         if socket_client:
            logging.debug('closing client')
            socket_client.close()
            socket_client=None
         elif socket_bike:
            logging.debug('closing bike')
            socket_bike.close()
            socket_bike=None
      except zerobt.NoServices:
         logging.debug('unable to connect to bike')
         socket_client.send(client_packet('unable to connect to bike'))
         socket_client.close()
         socket_client=None
         if socket_bike:
            socket_bike.close()
            socket_bike=None
      except zerobt.NoData:
         logging.debug('no data from bike')
         socket_client.send(client_packet('no data from bike'))
         socket_client.close()
         socket_client=None
         if socket_bike:
            socket_bike.close()
            socket_bike=None

if __name__ == "__main__":
   server()
