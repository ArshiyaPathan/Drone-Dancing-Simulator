import grpc
import sys
from concurrent import futures
import time
import drone_pb2
import drone_pb2_grpc

clientIdIterator = 0
clients = []
initialLocation = drone_pb2.Location()
initialLocation.x = 0
initialLocation.y = 0
initialLocation.z = 0

offset = drone_pb2.Location()
offset.x = 0
offset.y = 0
offset.z = 0
clientConnected = False

class ClientConnectionServicer(drone_pb2_grpc.ClientConnectionServicer):

  def connect(self,request,context):
    global clientIdIterator
    global initialLocation
    global clientConnected
    global offset
    response = drone_pb2.ConnectionResponse()
    if(request.clientId == ''):
      response.clientId = "190" + str(clientIdIterator)
      clientIdIterator+=1
      clients.append({"number" : clientIdIterator, "clientId" : response.clientId})
    else:
      response.clientId = request.clientId
    #response.clientId = "drone#" + str(clientIdIterator)
    #clientIdIterator+=1
    for elem in clients:
      if(elem["clientId"]== response.clientId):
        response.location.x = initialLocation.x + ((elem["number"] - 1) * offset.x)
        response.location.y = initialLocation.y + ((elem["number"] - 1) * offset.y)
        response.location.z = initialLocation.z + ((elem["number"] - 1) * offset.z)
    clientConnected = True
    #print(offset)
    return response

def run(host,port):
  global clientConnected
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  drone_pb2_grpc.add_ClientConnectionServicer_to_server(ClientConnectionServicer(),server)
  server.add_insecure_port('%s:%d' % (host, port))
  server.start()
  print('Server connected at %d' % port)
  _ONE_DAY_IN_SECONDS = 60 * 60 * 24
  print("awaiting client connection...")
  try:
    while True:
      if(clientConnected):
        newLocation = input("Enter new Coordinate [x,y,z] > ")
        #print(newLocation)
        a,b,c = newLocation.split(",")
        initialLocation.x = float(a)
        initialLocation.y = float(b)
        initialLocation.z = float(c)
      else:
        time.sleep(1)
      
  except KeyboardInterrupt:
    server.stop(0)



if __name__ == '__main__':
  #global initialLocation
  port= sys.argv[1]
  initialState = sys.argv[2]
  a,b,c = initialState.split(",")
  initialLocation.x=float(a)
  initialLocation.y=float(b)
  initialLocation.z=float(c)
  offsetstr = sys.argv[3]
  d,e,f = offsetstr.split(",")
  offset.x=float(d)
  offset.y=float(e)
  offset.z=float(f) 
  run('0.0.0.0', int(port))
else:
  print('hello')

