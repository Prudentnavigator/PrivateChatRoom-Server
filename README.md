PrivateChatRoom-Server v1.1.4

  Most chat applications connect to a server where all the messages between
users can potentially be stored and read (encrypted or not) by third parties.
This poses a risk to privacy, as private communications should be private.
PrivateChatRoom-Server allows you to be in control of your own server, so you
can communicate with your family or friends over the internet freely. 
It is designed to be used with the "PrivateChatRoom-App" but can be used
with ones own client application by connecting to the server via the
private IP (if devices are on the same network) or public IP (over the internet),
and the chosen port number (default port is 5050).
If python3 is installed on your device, this program can be used with any 
operating system, (Windows, Mac, Linux, etc.).

  Usage:
1. Option a:
   Set your router to allow port forwarding to the private IPv4/mac address
    of your device.
   
   Option b:
   You can also use VPN port forwarding (there are a number of VPN services
    that provide that feature), with the added benefit that you can use the
    server anywhere you can connect to the internet (public-wifi i.e. hotels,
    airport, trains, etc.) as you don't need access to the router of that
    network.
    Also, an extra layer of security is added by using port forwarding over a
    VPN.
    This option is highly recommended.
3.  Set your device's firewall to allow traffic on your chosen port over TCP.
4.  The server can also be used to communicated between devices on the same
    network (i.e in your home, hotel, office, etc..) without following step 1.
    However step 2 is still necessary.
5.  Run gui_server.py from the terminal which creates a GUI interface for the
    PrivateChatRoom-Server.
6.  Click on 'start server' button to start the server, which starts listening
    for incoming connections from clients and displays the server log.
7.  Users can set the ip address and port number by clicking on the 'set ip:port'
    button and stop the server by pressing the 'stop server' button.
8.  Click 'X' on top-right corner of the window to exit the program.

  Requirements:
- python3 or higher version is required.
- tkinter module should be installed on your system.
- also see requirements.txt.

  Note:
1. To get Public IPv4 and Mac Address, user needs to have an active internet
    connection.
2. Make sure that the server port number is not being used by any other
    application on your machine, else change it with the 'set ip:port' button
    or if you run the server.py as standalone server, in the '.pcr_ip_port.txt'
    file.
3. If VPN port forwarding is used, the VPN server that you connect to will
    assign a port number. This port number should be set with the 'set ip:port'
    for the 'PrivateChatRoom-Server' to listen on (also allow this port on your
    firewall). The listening ip should be 0.0.0.0.
4. The program reads/writes from/to a log file named ".privateChat_server.log"
    to store and display server messages, errors, and client connections.
    Log files are rotated (max 3 files). 
5. There are 2 different options to use the server:
    a) gui_server.py (on a desktop/laptop with a GUI)
    b) server.py (on a desktop/laptop if a GUI is not required)
6. The gui_server.py can also be packaged with pyinstaller or other packaging
    software to a standalone executable.
7. The Server logs info for troubleshooting and monitoring purposes only and 
    does not log any messages between clients.
8. Please note that this program does not encrypt the data being sent between
    clients! However, if VPN's are used with the server and the apps, the
    messages are encrypted.

  Features:
- Public IPv4 Address: This program reads the public IPv4 address of the
   device using an API and displays it in the GUI.
- Mac Address: It gets the MAC address of the device running the program,
   which helps to identify a unique client.
- Private IPv4 Address: The private IPv4 on the local network of the machine
   running the program is also displayed.

   *Caution: if the local ipv4 address is not matching your devices IP on your
   router, check your systems host addresses (Linux /etc/hosts).
- IPv4/Port: The IP address and the port number that the server is listening on
   are displayed.
- User Count: The number of connected clients are displayed.
- All server logs are displayed in real time in the GUI and are updated
   every 100 milliseconds.

If you have any questions/recommendations or want to report a bug you can reach
 me by email (tommy_software@mailfence.com).
