import asyncio, zen_utils

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

@asyncio.coroutine
def handle_conversation(reader, writer):
    global value
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))
    while True:
        data = b''
        while not data:
            more_data = yield from reader.read(4096)
            if not more_data:
                if data:
                    print('Client {} sent {!r} but then closed'
                          .format(address, data))
                else:
                    print('Client {} closed socket normally'.format(address))
                return
            data += more_data
            
        len_msg = str(data[:3], encoding="ascii")
        message = str(data[3:], encoding="ascii")
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

        writer.write(msg)

if __name__ == '__main__':
    address = zen_utils.parse_command_line('asyncio server using coroutine')
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handle_conversation, *address)
    server = loop.run_until_complete(coro)
    print('Listening at {}'.format(address))
    try:
        loop.run_forever()
    finally:
        server.close()
        loop.close()
