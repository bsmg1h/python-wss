import wss
import asyncio
import sys
import time

loop = asyncio.get_event_loop()

server = wss.Server(port=8887, useSsl=True, sslCert="server.crt", 
                     sslKey="server.key")

def onTextMessage(server, msg, client):
    print("got message from client:", msg)

def onBinaryMessage(server, msg, client):
    print("got binary message")

server.onMessage = onTextMessage
server.onBinaryMessage = onBinaryMessage

n = 0

@asyncio.coroutine
def sendData():
    global n
    while True:
        try:
            n+=1
            print("trying to broadcast...")
            server.broadcast(str(time.time())+str(n))
            server.broadcast("{'hello' : 'world' }")
        except Exception as e:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)

        yield from (asyncio.sleep(1))

loop.create_task(sendData())

server.start()
loop.run_forever()