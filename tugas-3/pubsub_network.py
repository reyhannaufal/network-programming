import random, threading, time, zmq
B = 32  # number of bits of precision in each random integer

def random_digits():
    return str(random.randint(0, 2))

def generator(zcontext, url):
    zsock = zcontext.socket(zmq.PUB)
    zsock.bind(url)
    while True:
        zsock.send_string(random_digits())
        print('Generated:', random_digits())
        time.sleep(0.2)

def executor_1(zcontext, in_url, out_url):
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    isock.setsockopt(zmq.SUBSCRIBE, b'00')
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    n1 = random.randint(1, 99000)
    n2 = random.randint(1, 1000) 
    data = str(n1) + ' ' + str(n2)
    while True:
        isock.recv_string()
        osock.send_string(data)

def executor_2(zcontext, in_url, out_url):
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    isock.setsockopt(zmq.SUBSCRIBE, b'00')
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    n1 = random.randint(1, 99000)
    n2 = random.randint(1, 1000) 
    data = str(n1) + ' ' + str(n2)
    while True:
        isock.recv_string()
        osock.send_string(data)

def executor_3(zcontext, in_url, out_url):
    isock = zcontext.socket(zmq.SUB)
    isock.connect(in_url)
    isock.setsockopt(zmq.SUBSCRIBE, b'00')
    osock = zcontext.socket(zmq.PUSH)
    osock.connect(out_url)
    n1 = random.randint(1, 99000)
    n2 = random.randint(1, 1000) 
    data = str(n1) + ' ' + str(n2)
    while True:
        isock.recv_string()
        osock.send_string(data)

def logger(zcontext, url):
    zsock = zcontext.socket(zmq.PULL)
    zsock.bind(url)
    while True:
        log = zsock.recv_string()
        print('Logger:', log)

def start_thread(function, *args):
    thread = threading.Thread(target=function, args=args)
    thread.daemon = True  # so you can easily Ctrl-C the whole program
    thread.start()

def main(zcontext):
    pubsub = 'tcp://127.0.0.1:6700'
    pushpull = 'tcp://127.0.0.1:6702'
    start_thread(generator, zcontext, pubsub)
    start_thread(executor_1, zcontext, pubsub, pushpull)
    # start_thread(executor_2, zcontext, pubsub, pushpull)
    # start_thread(executor_3, zcontext, pubsub, pushpull)
    start_thread(logger, zcontext, pushpull)
    time.sleep(5)

if __name__ == '__main__':
    main(zmq.Context())