#!/bin/env python3

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
        self.log_text = None
        self.start_button = None
        self.port_button = None
        self.stop_button = None
        self.image_label = None

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
        self.image_label.destroy()

        # Replace the image label with the log text.
        self.log_text.grid(row=0, columnspan=3, padx=40, pady=25)

        self.start_button.config(state="disabled",
                                 text="server started",
                                 bg="green",
                                 relief="sunken")

        self.stop_button.config(state="normal",
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

        self.stop_button.config(state="disabled",
                                text="server stopped",
                                bg="red",
                                relief="sunken")

        self.start_button.config(state="normal",
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
        self.log_text.config(state="normal")
        self.log_text.delete(1.3, "end")

        # Open the server log file in read mode and insert log into
        #   text widget.
        with open(".privateChat_server.log", "r", encoding="utf-8") as file:
            for line in file:
                self.log_text.insert("end", chars=line)

        # Scroll to the bottom of the widget to show the latest log.
        self.log_text.yview("end")
        self.log_text.config(state="disabled")

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
        self.window.title("PrivatChatRoom-Server v1.0.0")
        self.window.config(bg="lightgreen")
        self.window.geometry('1050x775')

        # Create a frame to add widgets to.
        frame = tk.Frame(self.window, bg="lightgreen")

        # Create a label that contains an image which is display at
        #   the startup of the app.
        image = ImageTk.PhotoImage(file="pcr_server.png")
        self.image_label = tk.Label(frame, image=image)

        # Add a scrolled text widget.
        self.log_text = tkinter.scrolledtext.ScrolledText(frame,
                                                          bg='lightgray',
                                                          font=("Times",
                                                                18))

        # Create a button for starting the server.
        self.start_button = Button(frame, text="start server",
                                   font=("Roman", 15),
                                   bd=8,
                                   highlightbackground="black",
                                   activeforeground="blue",
                                   activebackground="lightblue",
                                   disabledforeground="white",
                                   relief="raised",
                                   command=self.start_server_btn_clicked)

        # Create a button to change the port number.
        self.port_button = Button(frame,
                                  text="change port",
                                  font=("Roman", 15),
                                  bd=8,
                                  highlightbackground="black",
                                  activeforeground="blue",
                                  activebackground="lightblue",
                                  relief="raised",
                                  command=change_port)

        # Create a button for stopping the server.
        self.stop_button = Button(frame,
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

        # Place widgets on the frame.

        self.image_label.grid(row=0, columnspan=3, padx=15, pady=10)

        self.start_button.grid(row=1, column=0, pady=15)
        self.port_button.grid(row=1, column=1, pady=15)
        self.stop_button.grid(row=1, column=2, pady=15)

        frame.pack(expand=1)

        # Start the main loop of the GUI.
        self.window.mainloop()


def change_port():
    ''' Function that lets the user change the port number that the server
        is listening on. '''

    # Stop the server.
    GUIServer.stop_server(serve)

    msg = tkinter.Tk()  # Create a dialog window.
    msg.option_add('*Entry*background', 'lightgreen')
    msg.option_add('*font', 'Times')
    msg.withdraw()  # Hiding the window.

    # If the user does not enter an integer for the port, keep asking for
    #   input unless canceled.
    while True:
        # Getting a new port number from user.
        port = simpledialog.askstring("PrivateChatRoom-Server",
                                      "Please enter a port number",
                                      parent=msg)
        try:
            if not port.isdigit():
                continue
        except AttributeError:
            break
        else:
            break

    # If the user cancels changing the port, close the dialog window.
    if port is None:
        msg.destroy()

    else:
        # Write the changed port number to the .prc_port file.
        with open(".pcr_port", "w", encoding="utf-8") as file:
            file.write(port)
            # Close the dialog window.
            msg.destroy()

    server.read_port()


if __name__ == "__main__":
    serve = GUIServer()
    # Call the methode to create the GUI.
    GUIServer.create_gui(serve)
