#!/bin/env python3
 
# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024
  
# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
public_ip.py--a module that utilizes the ipinfo API to get your public
IP address and print it out. If there are any issues with the HTTP requests
(like no internet connection), it will catch these errors and print them out,
instead of crashing the program.
'''


import logging
from logging import handlers
import socket
import requests
import getmac

# Create a logger
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

# Add file handler to logger instance.
logger.addHandler(file_handler)

# Create stream handler to handle logs in console.
stream_handler = logging.StreamHandler()

# Set formatter for the stream handler object.
stream_handler.setFormatter(formatter)

# Add stream handler to logger instance.
logger.addHandler(stream_handler)


def get_public():
    ''' Function that gets the public IPv4 address of a device. '''
    try:
        endpoint = "https://ipinfo.io/json"  # Set up the API endpoint.

        # Send an HTTP request to the API and store the result.
        response = requests.get(endpoint, verify=True)

        # If the status code is not 200 (request was unsuccessful),
        #   log the status code.
        if response.status_code != 200:
            logger.error("Status: %s.",  response.status_code)
            return None

        data = response.json()  # Load the JSON data from the HTTP response.

        # Log the received IP
        logger.info(" your public IPv4 address: %s", data['ip'])

        with open(".pcr_addresses", 'w+', encoding="utf-8") as file:
            file.write(f"public_ipv4: {data['ip']}\n")

        get_mac()

        return data['ip']  # Return the public IPv4 address.

    except requests.exceptions.RequestException:
        # If any error occurs during the request,
        #   log a message and return None.

        with open(".pcr_addresses", 'w+', encoding="utf-8") as file:
            file.write("Public_ip4: check internet connection!\n")

        logger.warning("[PUBLIC-IP]: check internet connection!")
        return None


def get_private():
    ''' Function that gets the private IPv4 address. '''
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    logger.info(" your private IPv4 address: %s", ip_addr)

    with open(".pcr_addresses", 'a+', encoding="utf-8") as file:
        file.write(f"private_ipv4: {ip_addr}\n")

    return ip_addr   # Return private IPv4 address.


def get_mac():
    ''' Function to log mac address. '''
    mac = getmac.get_mac_address()
    logger.info(" your mac address: %s", mac)

    with open(".pcr_addresses", 'a+', encoding="utf-8") as file:
        file.write(f"device_mac: {mac}\n")

    return mac


if __name__ == "__main__":
    get_public()
    get_private()
