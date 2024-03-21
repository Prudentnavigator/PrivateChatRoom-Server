# PrivateChatRoom-Server v1.0.0
Chat Server

GUI_Server.py--a GUI-based user interface (GUI) for the PrivateChatRoom-Server.
   The program allows users to start and stop the server, view log files,
    and monitor the number of connected clients in real time. It also displays
    private/public IPv4 addresses and mac address of the device running
    the program.
   It is designed to be used with the 'PrivateChatRoom-App' but can be used
    with ones's own client application by connecting to the server via the
    private IP (if devices are on the same network) or public IP
    (over the internet), and the choosen port number (default port is 5050).

Usage:
1. Set your router to allow port forwarding to the private IPv4/mac address
    of your device.
2. Set your device firewall to allow traffic on your chosen port over TCP.
    (Linux 'sudo ufw allow 5050/tcp')
3. The server can also be used to communicated between devices on the same
    network (i.e in your home, hotel, office, etc..) without following step 1.
    However step 2 is still necessary.
4. Run gui_server.py from the terminal which creates a GUI interface for the
    PrivateChatRoom-Server.
5. Click on 'start server' button to start the server, which starts listening
    for incoming connections from clients and displays the server log.
6. Users can change the port number by clicking on the 'change port' button
    and stop the server by pressing the 'stop server' button.
7. The log files are updated every 100 milliseconds and display information
    in the GUI, including public/private IPv4 address, mac address and port.

Requirements:
- python3 or higher version is required.
- tkinter module should be installed on your system.
- also see requirements.txt.

Note:
1. To get Public IPv4 and Mac Address, user needs to have an active internet
    connection.
2. Make sure that the server port number is not being used by any other
    application on your machine, else change it with the 'change port' button
    or if you run the server.py as standalone server, in the '.pcr_port' file.
3. The program reads/writes from/to a log file named ".privateChat_server.log"
    to store and display server messages, errors, and client connections.
4. There are 2 different options to use the server:
    a) gui_server.py (on a desktop/laptop with a GUI)
    b) server.py (on a desktop/laptop if a GUI is not required)
5. The gui_server.py can also be packaged with pyinstaller
    (included in the requirements.txt) to a standalone executable.
6. The Server logs info for troubleshooting and monitoring purposes only and 
    does not log any messages between clients.
7. Please note that this program does not encrypt the data being sent between
    clients!

Features:
- Public IPv4 Address: This program reads the public IPv4 address of the
   device using an API and displays it in the GUI.
- Mac Address: It gets the mac address of the device running the program,
   which helps to identify a unique client.
- Private IPv4 Address: The private IPv4 on the local network of the machine
   running the program is also displayed.
   Caution: if the local ipv4 address is not matching your devices ip on your
   router, check your systems host addresses (Linux /etc/hosts).
- Port: port number is displayed.
- User Count: The number of connected clients is displayed in real time on
   the GUI and updated every 100 milliseconds.
