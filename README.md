# Drone-Dancing-Simulator
A drone dancing simulator in Python using GRPC as a communication protocol.

![](https://usatftw.files.wordpress.com/2018/02/drones.jpg)

The simulator has two components:
- Server
- Client

### Server

The server is the main orchestrator to guide directions for all drone in the network. The role of server are:
- Drone/client membership
- Getting user inputs for the whole drone cluster movement and sending new coordinate to each drone.

To start the server with a x-axis distance between each drone:

> python3 server.py {start_cooridnate} {peer_distance}

```sh
python3 server.py 0,0,0 10,0,0
```

Server log and waits for user input:

```sh
Server started at 3000.
Enter New Cooridnate[x, y, z] > 
```

#### 1. Membership

When a drone joins to the server, the server sends a response with an unique client/drone id and a coordinate to be moved.

> python3 client.py {server_port}

```sh
python3 client.py 3000 
```
Client log:

__First Drone Log__

```sh
Client id [xxxx] connected to the server.
[received] moving to [0, 0, 0]
```

__Second Drone Log__

```sh
Client id [xxxx] connected to the server.
[received] moving to [10, 0, 0]
```

#### 2. Getting user inputs and forwarding to drones

When user enters a new coordinate in the server window, the server forward new coordinates to all drones. Any number of drones can be supported. Then, each client window will be prompted with new coordinate.

### Client

Each drone acts as a client which is listening new coordinates from the server. The server to client communication is one-way (GRPC) streaming and the client never sends any messages back to the server.
