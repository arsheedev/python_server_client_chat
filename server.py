from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter


#Accept incoming connections
def accept_incoming_connections():
    msg_list.insert(tkinter.END, f'Server running on {host_string.get()}:{port_int.get()}')
    while True:
        client, client_address = SERVER.accept()
        client.send(bytes("Now send me your name!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_client, args=(client,)).start()

# Handle single client
def handle_client(client):
    try:
        name = client.recv(BUFSIZ).decode("utf8")
        msg_list.insert(tkinter.END, f'{name} has joined the chat!')
        welcome = 'Welcome %s! If you want to quit, type #quit to exit.' % name
        client.send(bytes(welcome, "utf8"))
        msg = "%s has joined the chat!" % name
        broadcast(bytes(msg, "utf8"))
        clients[client] = name
    except:
        temp = ''

    while True:
        try:
            msg = client.recv(BUFSIZ)
            temp_msg = msg.decode('utf8')
            if msg == bytes("#quit", "utf8"):
                client.close()
                del clients[client]
                msg_list.insert(tkinter.END, f'{name} has left the chat!')
                broadcast(bytes("%s has left the chat." % name, "utf8"))
                break
            else:
                msg_list.insert(tkinter.END, f'{name}: {temp_msg}')
                broadcast(msg, name+": ")
        except:
            client.close()
            del clients[client]
            msg_list.insert(tkinter.END, f'{name} has left the chat!')
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

# Broadcast messages to all client
def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

# Start server
def start_server():
    global disabled
    if disabled:
        return
    else:
        disabled = True
        HOST = host_string.get()
        PORT = int(port_int.get())
        ADDR = (HOST, PORT)
        SERVER.bind(ADDR)
        SERVER.listen(5)
        ACCEPT_THREAD.start()

# Handles sending of messages
def send(event=None):
    msg = my_msg.get()
    my_msg.set("")
    msg_list.insert(tkinter.END, f'Server: {msg}')
    msg = msg.encode()
    broadcast(msg, 'Server: ')

# Setup Server
SERVER = socket(AF_INET, SOCK_STREAM)
BUFSIZ = 1024
ACCEPT_THREAD = Thread(target=accept_incoming_connections)
clients = {}
addresses = {}
disabled = False

# Window manager form
top = tkinter.Tk()
top.title("Server")

# Connect form/field
host_label = tkinter.Label(top, text='Server IP')
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
connect_button = tkinter.Button(top, text='start', command=start_server)
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
