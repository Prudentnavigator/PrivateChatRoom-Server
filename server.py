#!/bin/env python3

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
chat_server.py--a simple module implementation of a basic chat room
               server that allows multiple users to connect and communicate
               with each other using sockets.
               SET FIREWALL RULE TO ALLOW TRAFFIC ON YOUR CHOSEN PORT OVER TCP.
               Linux example: sudo ufw allow 5050/tcp
'''

import sys
import socket
import threading
import logging
from logging import handlers
import ipv4_addresses

# Get current logger instance with name of the module.
logger = logging.getLogger(__name__)

# Set log level to debug - higher than info.
logger.setLevel(logging.DEBUG)

# Create a formatter object with specified format for the logs.
formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                              "%Y-%m-%d %H:%M:%S")

# Create file handler to handle log files rotation and backup.
file_handler = handlers.RotatingFileHandler('.privateChat_server.log',
                                            maxBytes=60000, backupCount=3)
# Set formatter for the file handler object.
file_handler.setFormatter(formatter)

# Create stream handler to handle logs in console.
stream_handler = logging.StreamHandler()

# Set formatter for the stream handler object.
stream_handler.setFormatter(formatter)

# Add both file and stream handlers to logger instance.
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# Assigning Public and Private IP Addresses.
# Get the public IPv4 address of the machine.
PUPLIC_IP = ipv4_addresses.get_public()
# Get the private IPv4 address of the host machine.
HOST = ipv4_addresses.get_private()

# Encoding format for data being sent/received over the socket.
FORMAT = "utf-8"

client_list = []  # Initialize an empty list to store client objects.
alias_list = []  # Initialize an empty list to store aliases of clients.
SERVER_SOCKET = ""
PORT = ""


def read_port():
    ''' Get the port number from the .prc_port file. '''

    global PORT

    try:
        # Opening file to read its content (port number).
        with open(".pcr_port", "r", encoding="utf-8") as file:
            port = file.read()
            # Converting port number from string to integer and storing it
            #   in PORT variable.
            PORT = int(port)
            return PORT

    except (FileNotFoundError, ValueError):
        # If the file does not exist or an error during reading the file
        #   occurs, create a new file with the a default port number 5050.
        with open(".pcr_port", "w+", encoding="utf-8") as file:
            PORT = 5050
            file.write(str(PORT))
            return PORT


def broadcast(message):
    ''' Function to broadcast a message to all connected clients. '''

    for client in client_list:
        try:
            client.send(message)
        except BrokenPipeError:
            # Log the error, close the client's connection and
            #   continue with next client.
            logger.info("[MESSAGE]: message not delivered...")
            client.close()
        except OSError:
            pass


def handle_clients(client):
    ''' Threaded function to handle incoming messages from clients. '''

    while True:
        try:
            # Receive data from the client and print its alias.
            message = client.recv(2048)

            # Broadcast the received message to all the clients.
            broadcast(message)
            user_count(client_list)

        except OSError:
            # if the connection is reset or aborted by the client, remove it
            #   from both lists and close the connection.
            index = client_list.index(client)
            client.close()
            alias = alias_list[index]
            del client_list[index]
            msg = f"{alias.decode(FORMAT)}"
            logger.info("[DISCONNECTED]: client disconnected: %s", msg)
            user_count(client_list, True)
            broadcast(f"{msg} has left the chat...\n".encode(FORMAT))

            if alias in alias_list:
                del alias_list[index]

            break


def receive():
    ''' Function to receive incoming connections and start new
        threads for handling messages '''

    while True:
        try:
            # Accept a new connection and store its details in client and
            #   address variables.
            client, addr = SERVER_SOCKET.accept()
        except OSError:
            break

        except Exception as err:
            # Log the error.
            logger.error("[ACCEPT]: accepting has failed with error %s", err)
            break

        # Send the alias prompt to the client and receive their alias.
        client.send("ALIAS".encode(FORMAT))

        try:
            alias = client.recv(2048)
        except ConnectionResetError:
            continue

        # Add the client object and alias to respective lists
        #   for display purposes.
        client_list.append(client)
        alias_list.append(alias)

        # Decode bytes format to string and remove any
        #   leading/trailing white spaces.
        msg1 = f"{alias.decode(FORMAT).strip()}"
        msg2 = "Name of the client is"

        # Log a message indicating that a new connection was made,
        #   with the name and IP address of the user.
        logger.info("[NEW CONNECTION]: %s %s ip: %s", msg2, msg1, addr[0])
        cast = f"{msg1} joined the chat...\n".encode(FORMAT)
        user_count(client_list, True)

        # Send a message indicating that a new user has joined to
        #   all connected clients.
        broadcast(cast)

        try:
            # Create a new thread for handling incoming messages from
            #   the client.
            thread = threading.Thread(target=handle_clients, args=(client,))
            thread.start()
        except Exception as err:
            # Log the error.
            msg = f"starting a new thread has failed with error {err}"
            logger.error("[THREAD]: %s", msg)


def user_count(clients, new=False):
    ''' Function to log the number of connected clients to the server
        and also display in client.py '''

    devices = len(clients)

    if devices > 1:
        broadcast(f"{devices} people are online...\n".encode(FORMAT))
        if new:
            logger.info("[CONNECTIONS]: %s devices are connected...", devices)
    else:
        broadcast(f"{devices} person is online...\n".encode(FORMAT))
        if new:
            logger.info("[CONNECTIONS]: %s device is connected...", devices)


def start():
    ''' Function to start the server and create a TCP socket objects '''

    global SERVER_SOCKET
    read_port()

    try:
        SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logger.info(" socket succesfully created...")
    except socket.error as err:
        logger.critical("[SOCKET]: socket creation failed! %s", err)
        sys.exit()

    try:
        # Bind the socket to the host and port number.
        SERVER_SOCKET.bind((HOST, PORT))
        logger.info(" server is starting...")
    except OSError as error:
        logger.critical("[BIND]: binding has failed! %s", error)

        # Log a help message according to the error number.
        if error.errno == 98:
            msg = "close client apps, wait a minute and stop/start server!"
            logger.info("[HELP]: %s", msg)
        elif error.errno == 99:
            msg = " please connect to the internet!"
            logger.info("[HELP]: %s", msg)

    else:
        # Start listening for incoming connections on the server.
        try:
            SERVER_SOCKET.listen()
        except Exception as error:
            logger.critical("[LISTEN]: listening has failed with error %s",
                            error)
            sys.exit()

        msg = f" server is running and listening on ip:{HOST} port:{PORT}"
        logger.info(msg)

        receive()


def stop():
    ''' Function to stop the server.'''

    logger.info(" server is shutdown...")

    # Iterate through all clients and close their connections.
    for client in client_list:
        try:
            client.close()
        except OSError as err:
            msg = " closing connection has failed with error"
            logger.warning("[CLOSE]:%s %s", msg, err)

    # Shutdown the socket and close connections.
    try:
        SERVER_SOCKET.shutdown(socket.SHUT_RDWR)  # Shut down the socket.
        SERVER_SOCKET.close()  # Close the socket object.
    except (AttributeError, OSError):
        pass


if __name__ == "__main__":
    start()
