import argparse, random, socket, zen_utils
import sys, random, multiprocessing

HOST = "127.0.0.1"
PORT = 1060
NUMJOBS = 6

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

def worker(address, i, data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(address)

    message = ""
    for ii in data:
        ii = ii.strip()
        len_msg = b"%03d" % (len(ii),) 
        msg = len_msg + bytes(ii, encoding="ascii")
        sock.sendall(msg)
        len_msg = recvall(sock, 3)
        message = recvall(sock, int(len_msg))
        message = str(message, encoding="ascii")
    print('klien: ', i, '->', message)
    sock.close()

if __name__ == '__main__':
    f = open("input.txt")
    data = f.readlines()
    f.close()

    address = (HOST, PORT)
    jobs = []
    for i in range(NUMJOBS):
        p = multiprocessing.Process(target=worker, args=(address, i, data))
        jobs.append(p)
    print("JOBS:", len(jobs))

    for p in jobs:
        p.start()

    for p in jobs:
        p.join()

# vim:sw=4:ai
