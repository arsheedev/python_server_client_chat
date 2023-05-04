from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


# Handles receiving of messages
def receive():
    while True:
        try:
            msg = client_socket.recv(BUFSIZ).decode("utf8")
            msg_list.insert(tkinter.END, msg)
        except OSError:
            break

# Handles sending of messages
def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    client_socket.send(bytes(msg, "utf8"))
    if msg == "#quit":
        client_socket.close()
        top.quit()

# This fucntion is called when window is closed
def on_closing(event=None):
    my_msg.set("#quit")
    send()

# Function for connecting client to server
def connect_server():
    HOST = host_string.get()
    PORT = int(port_int.get())

    ADDR = (HOST, PORT)
    client_socket.connect(ADDR)
    receive_thread.start()
    msg_list.insert(tkinter.END, f'Connection established with {HOST}:{PORT}')

# Setup socket
client_socket = socket(AF_INET, SOCK_STREAM)
receive_thread = Thread(target=receive)
BUFSIZ = 1024

# Window manager form
top = tkinter.Tk()
top.title("Client")

# Function to be executed when window manager form is closed
top.protocol("WM_DELETE_WINDOW", on_closing)

# Connect form/field
host_label = tkinter.Label(top, text='Host IP')
host_label.pack()
host_string = tkinter.StringVar()
host_string.set('127.0.0.1')
host_field = tkinter.Entry(top, textvariable=host_string)
host_field.pack()
port_label = tkinter.Label(top, text='PORT')
port_label.pack()
port_int = tkinter.IntVar()
port_int.set(33000)
port_field = tkinter.Entry(top, textvariable=port_int)
port_field.pack()
connect_button = tkinter.Button(top, text='connect', command=connect_server)
connect_button.pack()

# Message frame
messages_frame = tkinter.Frame(top)
messages_frame.pack()

# Message box for showing history message
scrollbar = tkinter.Scrollbar(messages_frame)
scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list = tkinter.Listbox(messages_frame, height=15, width=50, yscrollcommand=scrollbar.set)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()

# Message field to input message
my_msg = tkinter.StringVar()
entry_field = tkinter.Entry(top, textvariable=my_msg)
entry_field.bind("<Return>", send)
entry_field.pack()
send_button = tkinter.Button(top, text="Send", command=send)
send_button.pack()

# Start GUI application
tkinter.mainloop()
