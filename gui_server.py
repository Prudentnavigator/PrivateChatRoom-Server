#!/bin/env python3
# -*- mode: python; coding: utf-8 -*-

# Script by Thomas Pirchmoser (tommy_software@mailfence.com) 2024

# This script was created for personal/educational purposes only and is not to
#   be used for commercial or profit purposes.

'''
gui_server.py--a grafical user interface (GUI) for the PrivateChatRoom-Server.
'''

import tkinter as tk
from tkinter import Button
import tkinter.scrolledtext
from tkinter import simpledialog
import threading
import time
from PIL import ImageTk
import server   # import the server module to start/stop the server.


class GUIServer():
    ''' A class to add a GUI to the server. '''

    # Set an after() id inorder to pass it to the after_cancel().
    keep_updating = None

    def __init__(self):
        self.window = None  # Initialize window to be assigned later.
        self.start_thread = None
        self.server_thread = None
        self.widget = {"log_text": None,
                       "image_label": None,
                       "start_button": None,
                       "port_button": None,
                       "stop_button": None,
                       "copy_label": None}

    def start_server(self):
        ''' Start a new thread which starts the server. '''

        # Create a new thread and target it to the server.start() method.
        self.start_thread = threading.Thread(target=server.start, daemon=True)
        self.start_thread.start()

        while True:
            # check if the server has stopped
            if not self.start_thread.is_alive():
                break
            time.sleep(1)  # wait for a second before checking again

    def start_server_btn_clicked(self):
        ''' Method that calls the start_server methode and alters
            the configuration of the start_button and stop_button. '''

        # Delete the label containing the image displayed upon startup.
        self.widget["image_label"].destroy()

        # Replace the image label with the log text.
        self.widget["log_text"].grid(row=0, columnspan=3, padx=40, pady=25)

        self.widget["start_button"].config(state="disabled",
                                           text="server started",
                                           bg="green",
                                           relief="sunken")

        self.widget["stop_button"].config(state="normal",
                                          text="  stop  server ",
                                          bg="lightgray",
                                          relief="raised")

        # Start a new thread for server.
        self.server_thread = threading.Thread(target=self.start_server,
                                              daemon=True)
        self.server_thread.start()

        # Update the log display by calling update_log().
        self.update_log()

    def stop_server(self):
        ''' Method to stop the server and alter
            the configuration of the stop_button and start_button. '''

        self.widget["stop_button"].config(state="disabled",
                                          text="server stopped",
                                          bg="red",
                                          relief="sunken")

        self.widget["start_button"].config(state="normal",
                                           text=" start server ",
                                           bg="lightgray",
                                           relief="raised")

        # Stop the server.
        server.stop()

        # Cancel updating of log display by passing a flag to update_log().
        self.update_log(cancel=True)

    def read_log(self):
        ''' Method to read and display the server's log-file. '''

        # Clear the previous text by deleting all of it.
        self.widget["log_text"].config(state="normal")
        self.widget["log_text"].delete(1.3, "end")

        # Open the server log file in read mode and insert log into
        #   text widget.
        with open(".privateChat_server.log", "r", encoding="utf-8") as file:
            for line in file:
                self.widget["log_text"].insert("end", chars=line)

        # Scroll to the bottom of the widget to show the latest log.
        self.widget["log_text"].yview("end")
        self.widget["log_text"].config(state="disabled")

    def update_log(self, cancel=False):
        ''' Method that reads the server log and updates the scrolledtext
            widget recursively according to the time value given in
            window.after() or stops updating when canceled. '''

        # Call the read_log methode.
        self.read_log()

        # If cancel is not True, call update_log() again
        #   after 100 milliseconds.
        if not cancel:
            GUIServer.keep_updating = self.window.after(100, self.update_log)
        else:
            # Cancel the next call to update_log().
            try:
                self.window.after_cancel(GUIServer.keep_updating)
            except ValueError:
                pass

    def create_gui(self):
        ''' Method to create a GUI for the server. '''

        # Create a new Tkinter window.
        self.window = tk.Tk()
        self.window.title("PrivatChatRoom-Server v1.1.4")
        self.window.config(bg="lightgreen")
        self.window.geometry('1050x775')

        # Create a frame to add widgets to.
        frame = tk.Frame(self.window, bg="lightgreen")

        # Create a label that contains an image which is display at
        #   the startup of the app.
        image = ImageTk.PhotoImage(file="pcr_server.png")
        self.widget["image_label"] = tk.Label(frame, image=image)

        # Add a scrolled text widget.
        self.widget["log_text"] = tkinter.scrolledtext.ScrolledText(
                                                                frame,
                                                                bg='lightgray',
                                                                font=("Times",
                                                                      18))

        # Create a button for starting the server.
        self.widget["start_button"] = Button(
                                        frame, text="start server",
                                        font=("Roman", 15),
                                        bd=8,
                                        highlightbackground="black",
                                        activeforeground="blue",
                                        activebackground="lightblue",
                                        disabledforeground="white",
                                        relief="raised",
                                        command=self.start_server_btn_clicked)

        # Create a button to change the port number.
        self.widget["port_button"] = Button(frame,
                                            text="set ip:port",
                                            font=("Roman", 15),
                                            bd=8,
                                            highlightbackground="black",
                                            activeforeground="blue",
                                            activebackground="lightblue",
                                            relief="raised",
                                            command=set_ip_port)

        # Create a button for stopping the server.
        self.widget["stop_button"] = Button(frame,
                                            text="server stopped",
                                            font=("Roman", 15),
                                            bd=8,
                                            bg="red",
                                            highlightbackground="black",
                                            activeforeground="blue",
                                            activebackground="lightblue",
                                            disabledforeground="white",
                                            state="disabled",
                                            relief="sunken",
                                            command=self.stop_server)

        # Create a label to display the copyright.
        label_text = "Copyright\xa92024 Thomas Pirchmoser"
        self.widget["copy_label"] = tkinter.Label(frame,
                                                  text=label_text,
                                                  font=("Times", 9),
                                                  bg="lightgreen")

        # Place widgets on the frame.
        self.widget["image_label"].grid(row=0, columnspan=3, padx=15, pady=10)
        self.widget["start_button"].grid(row=1, column=0, pady=15)
        self.widget["port_button"].grid(row=1, column=1, pady=15)
        self.widget["stop_button"].grid(row=1, column=2, pady=15)
        self.widget["copy_label"].grid(row=2, column=1, pady=10)

        frame.pack(expand=1)

        # Start the main loop of the GUI.
        self.window.mainloop()


def set_ip_port():
    ''' Function that lets the user set the ip/port number that the server
        is listening on. '''

    # Stop the server.
    GUIServer.stop_server(serve)

    msg = tkinter.Tk()  # Create a dialog window.
    msg.option_add('*Entry*background', 'lightgreen')
    msg.option_add('*font', 'Times')
    msg.withdraw()  # Hiding the window.

    while True:
        # Getting a new ip/port number from user.
        listening_on = simpledialog.askstring(
                                      "PrivateChatRoom-Server",
                                      "Please enter listening ip:port  "
                                      "i.e (192.168.0.10:5050)",
                                      parent=msg)

        # If the user cancels changing the port, close the dialog window.
        if listening_on is None:
            msg.destroy()
            break

        try:
            ip_port = listening_on.split(":")
            ip_add = ip_port[0]
            port = ip_port[1]

            # If the user does not enter an integer for the port, keep asking
            #  for input.
            if not port.isdigit():
                continue

            # Write the changed ip/port to the .prc_ip_port.txt file.
            with open(".pcr_ip_port.txt", "w", encoding="utf-8") as file:
                info_txt = f"{ip_add}:{port}"
                file.write(info_txt)
                # Close the dialog window.
                msg.destroy()

                break

        except IndexError:
            continue

    server.read_port()


if __name__ == "__main__":
    serve = GUIServer()
    # Call the methode to create the GUI.
    GUIServer.create_gui(serve)
