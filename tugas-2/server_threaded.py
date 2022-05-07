from email import message
import zen_utils
from threading import Thread

value = 0

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

def handle_connection(sock):
    global value
    len_msg = recvall(sock, 3)
    message = recvall(sock, int(len_msg))
    message = str(message, encoding="ascii")
    cmd, c_value = message.split()

    print(cmd, "=>", c_value)
    
    if cmd == 'ADD':
        value += int(c_value)
    elif cmd == 'DEC':
        value -= int(c_value)
    else:
        print("Wrong command")
    
    msg = "Value = : " + str(value)
    len_msg = b"%03d" % (len(msg), )

    msg = len_msg + bytes(msg, encoding="ascii")

    sock.sendall(msg)

def handle_thread(listener):
    while True:
        sock, address = listener.accept()
        print('Accepted connection from {}'.format(address))
        try:
            while True:
                handle_connection(sock)
        except EOFError:
            print('Client closed socket normally')
        finally :
            sock.close()

def start_threads(listener, workers=4):
    t = (listener,)
    for i in range(workers):
        Thread(target=handle_thread, args=t).start()

if __name__ == '__main__':
    address = zen_utils.parse_command_line('multi-threaded server')
    listener = zen_utils.create_srv_socket(address)
    start_threads(listener)
