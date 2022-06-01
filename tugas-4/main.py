
   
import argparse, socket
import os

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

def server(interface, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((interface, port))
    sock.listen(1)
    print('Listening at', sock.getsockname())
    while True:
        print('Waiting to accept a new connection')
        sc, sockname = sock.accept()
        print('We have accepted a connection from', sockname)
        print('Socket name:', sc.getsockname())
        print('Socket peer:', sc.getpeername())
        len_msg = recvall(sc, 3)
        message = recvall(sc, int(len_msg))
        print('Message len:', repr(len_msg))
        print('Incoming message:', repr(message))
        cmd = message.split()
        if cmd[0].decode('utf-8') == "ping":
            messages = ""
            for message in cmd[1:]:
                messages += message.decode('utf-8')
                messages += " "
            send_msg = "terima: " + messages
            len_msg = b"%03d" % (len(send_msg),)
            send_msg = len_msg + bytes(send_msg, 'utf-8')
            sc.sendall(send_msg)
            sc.close()
        elif cmd[0].decode('utf-8') == "quit":
            send_msg = "Server shutdown..."
            len_msg = b"%03d" % (len(send_msg),)
            send_msg = len_msg + bytes(send_msg, 'utf-8')
            sc.sendall(send_msg)
            sc.close()
            break
        elif cmd[0].decode('utf-8') == "ls":
            if len(cmd) == 1:
                # cur dir
                current_directory = os.getcwd()
                # list dir
                list_dir = os.listdir(current_directory)
                # send list dir
                send_msg = ""
                for call_dir in list_dir:
                    send_msg += call_dir
                    send_msg += " "
                len_msg = b"%03d" % (len(send_msg),)
                send_msg = len_msg + bytes(send_msg, 'utf-8')
                sc.sendall(send_msg)
                sc.close()
            else:
                # global dir with workaround with star
                global_dir = os.path.join("/", cmd[1].decode('utf-8').split("*")[0])
                # list dir
                list_dir = os.listdir(global_dir)
                # send list dir
                send_msg = ""
                for call_dir in list_dir:
                    send_msg += call_dir
                    send_msg += "\n"
                len_msg = b"%03d" % (len(send_msg),)
                send_msg = len_msg + bytes(send_msg, 'utf-8')
                sc.sendall(send_msg)
                sc.close()
        elif cmd[0].decode('utf-8') == "get":
            dir = os.path.join("/", cmd[1].decode('utf-8'))
            if os.path.isfile(dir):
                count = 0
                with open(dir, "rb") as f:
                    for _ in f:
                        count += 1
                send_msg = "get: " + dir + " " + "size: " + str(count) + " " + "lokal: " + cmd[2].decode('utf-8')
                len_msg = b"%03d" % (len(send_msg),)
                send_msg = len_msg + bytes(send_msg, 'utf-8')
                sc.sendall(send_msg)
                sc.close()
            else:
                send_msg = "File not found"
                len_msg = b"%03d" % (len(send_msg),)
                send_msg = len_msg + bytes(send_msg, 'utf-8')
                sc.sendall(send_msg)
                sc.close()
            


def client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned socket name', sock.getsockname())
    msg = input('>')
    len_msg = b"%03d" % (len(msg),)
    cmd = msg.split()
    sock.sendall(len_msg + bytes(msg, 'utf-8'))

    if cmd[0] == "quit":
        print("Client shutdown...")

    rcv_len = recvall(sock, 3)
    rcv_message = recvall(sock, int(rcv_len))
    print(rcv_message.decode('utf-8'))
    sock.close()


if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)