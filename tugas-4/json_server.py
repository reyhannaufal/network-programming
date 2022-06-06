import argparse, socket
import sys
import time, os, glob
from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer

def ngelist1():
    print("Ngelist...")
    daftar=glob.glob("./*")
    isi=" "
    for i in daftar:
        isi += i + "\n"
    print("Udah ngelistnya yeay")
    return isi

def ngelist2(String):
    print("Ngelist...")
    daftar=glob.glob(String)
    isi=" "
    for i in daftar:
        isi += i + "\n"
    print("Udah ngelistnya yeay")
    return isi

def ngitung(String):
    print("Ngitung...")
    daftar=glob.glob(String)
    count=0
    for i in daftar:
        count+=1
    print("Udah ngitungnya yeay")
    return count

def ngambil(String):
    print('Ngambil...')
    msg=String.split()
    tempat= ' '.join(msg[:-1])
    tempat2=[tempat, msg[-1]]
    msg2 = '/'.join(tempat2)
    f=open(msg2, "rb")
    b=f.read()
    tulis= "fetch: " + tempat + "\nsize: " + str(len(b)) + "\nlokal: " + msg[-1]
    print("Udah ngambilnya yeay")
    return tulis

def bikin(String):
    print('Bikin...')
    msg=String.split()
    tempat= ' '.join(msg[1:])
    tempat2=[tempat, msg[0]]
    msg2 = '/'.join(tempat2)
    f=open(msg2, "x")
    f.close()
    tulis= "put: " + tempat + "\nlokal: " + msg[0]
    print("Udah bikinnya yeay")
    return tulis

def tutup():
    print("Shuting down...")
    sys.exit(0)

def main():
    server = SimpleJSONRPCServer(('localhost', 7002))
    server.register_function(ngelist1)
    server.register_function(ngelist2)
    server.register_function(ngambil)
    server.register_function(ngitung)
    server.register_function(bikin)
    server.register_function(tutup)
    print("Starting server")
    server.serve_forever()
    sys.exit(0)

if __name__ == '__main__':
    main()