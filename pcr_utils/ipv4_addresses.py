#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
public_ip.py--a module that utilizes the ipinfo API to get your public
IP address and print it out. If there are any issues with the HTTP requests
(like no internet connection), it will catch these errors and print them out,
instead of crashing the program.
'''


import socket
import requests
from pcr_utils import getmac
from pcr_utils.server_logging import server_log

logger = server_log(__name__)


def get_public():
    ''' Function that gets the public IPv4 address of a device. '''
    try:
        endpoint = "https://ipinfo.io/json"  # Set up the API endpoint.

        # Send an HTTP request to the API and store the result.
        response = requests.get(endpoint, verify=True, timeout=3)

        # If the status code is not 200 (request was unsuccessful),
        #   log the status code.
        if response.status_code != 200:
            logger.error("Status: %s.",  response.status_code)
            return None

        data = response.json()  # Load the JSON data from the HTTP response.

        # Log the received IP
        logger.info(" your public IPv4 address: %s", data['ip'])

        with open(".pcr_addresses.txt", 'w+', encoding="utf-8") as file:
            file.write(f"public_ipv4: {data['ip']}\n")

        get_mac()

        return data['ip']  # Return the public IPv4 address.

    except requests.exceptions.RequestException:
        # If any error occurs during the request,
        #   log a message and return None.

        with open(".pcr_addresses.txt", 'w+', encoding="utf-8") as file:
            file.write("Public_ip4: check internet connection!\n")

        logger.warning(" check internet connection!")
        return None


def get_private():
    ''' Function that gets the private IPv4 address. '''
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    logger.info(" your private IPv4 address: %s", ip_addr)

    with open(".pcr_addresses.txt", 'a+', encoding="utf-8") as file:
        file.write(f"private_ipv4: {ip_addr}\n")

    return ip_addr   # Return private IPv4 address.


def get_mac():
    ''' Function to log mac address. '''
    mac = getmac.get_mac_address()
    logger.info(" your mac address: %s", mac)

    with open(".pcr_addresses.txt", 'a+', encoding="utf-8") as file:
        file.write(f"device_mac: {mac}\n")

    return mac


if __name__ == "__main__":
    get_public()
    get_private()
