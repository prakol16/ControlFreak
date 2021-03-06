import sys
from twisted.web.static import File
from twisted.python import log
from twisted.web.server import Site
from twisted.internet import reactor
from twisted.internet.task import LoopingCall
from autobahn.twisted.websocket import WebSocketServerFactory, \
    WebSocketServerProtocol
from autobahn.twisted.resource import WebSocketResource
from turn_lights import Light

latest_coords = [0, 0]
class SomeServerProtocol(WebSocketServerProtocol):
    def onConnect(self, request):
        print("Connection {}".format(request))
    def onMessage(self, payload, isBinary):
        string = payload.decode('utf8')
        newPower = float(string.split(" ")[1])*100
        print("Power", newPower)
        latest_coords[0] = newPower
    def onOpen(self):
        print("something opened")
class MainServer:
  def __init__(self):
    self.latest_coords = latest_coords
  def runReactor(self):
    log.startLogging(sys.stdout)

    # static file server seving index.html as root
    root = File("./client")

    factory = WebSocketServerFactory(u"ws://127.0.0.1:9999")
    factory.protocol = SomeServerProtocol
    resource = WebSocketResource(factory)
    # websockets resource on "/ws" path
    root.putChild(b"ws", resource)

    site = Site(root)
    reactor.listenTCP(9999, site)
    #reactor.listenTCP(9999, factory)
    l = Light()
    LoopingCall(l.loop, latest_coords).start(0)
    reactor.run()
m = MainServer()
m.runReactor()
