import sys
import grpc
import time
import drone_pb2
import drone_pb2_grpc

host = '0.0.0.0'
portstr= sys.argv[1]
port= int(portstr)
channel = grpc.insecure_channel('%s:%d' % (host, port))
clientId = ''
location = drone_pb2.Location()
location.x = -1
location.y = -1
location.z = -1


stub = drone_pb2_grpc.ClientConnectionStub(channel)

req = drone_pb2.ConnectionRequest()
#req.clientId = clientId
while True:
  req.clientId = clientId
  response = stub.connect(req)
  if(clientId == ''):
    clientId = response.clientId
    print("Client id [%s] connected to the server." % (response.clientId))
  if((response.location.x != location.x or response.location.y != location.y) or response.location.z != location.z):
    print("[received] moving to [%g, %g, %g]" % (response.location.x,response.location.y,response.location.z))
    location.x = response.location.x
    location.y = response.location.y
    location.z = response.location.z
    #print(" ")
    #print('awaiting further instructions from server')
    print(" ")
  time.sleep(0.1)