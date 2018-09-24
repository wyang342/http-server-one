# HTTP Server One

## What We're Building

For this challenge we are going to build an HTTP server using just Python. We'll use a lot of what we've learned so far, but some of the techniques we utilize to accomplish this will be entirely new. Don't worry. The point of this exercise is not to become an expert at building servers. There are many tools out there that already do what we are going to do and do it wayyyy better. This project is for our own learning. 

## Release 0 - Hello World

HTTP servers speak over the networking protocol TCP/IP. It turns out HTTP requests and responses aren't sent over the web as single blobs of text. Instead, they're transferred over as smaller packets and re-assembled at their final destination. TCP/IP is the protocol that makes this lower-level communication happen.

Lucky for us, we don't have to learn TCP/IP from scratch to write an HTTP server. Python ships with a TCP server library (`socket`) we can use, allowing us to focus on HTTP.

### TCP/IP Hello World

Let's start by creating a simple [TCP server in Python](https://docs.python.org/2/library/socket.html#socket.AF_INET), here's an example:

```Python
# server.py

import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9292))
print('Waiting For Connection...')
server.listen(1)

client_connection, client_address = server.accept()
print('New Connection received!')

client_connection.close()
```

Let's walk through the code here. First, we import the `socket` library. Next, we create a new instance of a socket object and save it to the variable `server`. We are passing our new socket two arguments, `AF_INET` is the address family we will be using and `SOCK_STREAM` is the type of socket we want to use. 

Next we bind our new socket to a host and port. We'll use `localhost` as our host. This is the address for our local machine. Then, we bind it to port `9292`. This is an arbitrary choice of port number. We could do anything. 

After that we tell the socket to start listening for a connection from a client. Then, we print "Waiting for connection..." to the terminal. 

Our program will pause here and wait until it receives a connection. After it receives one, it will print "New connection received". Then we need to remember to close the connection before the program exits. Run `server.py` in the terminal. 

```
http_server_one :> python3 server.py
Waiting for connection...

```

Open a separate command line window and run `curl http://localhost:9292`. [Curl](https://curl.haxx.se/) is a tool that allows us to make `http` requests from the command line. `curl http://localhost:9292` will make a `GET` request to `http://localhost:9292`. The important thing to note here is the port number at the end. Because we opened our server on port `9292`, we need to make sure that we make our request to the same port. 

After you run the code, the server should accept the connection, print "New connection received", and then exit. Not very exciting, but it's important to note that this first step is what every web service is based on. A server listens for a connection, when it makes one, it does some stuff. Right now the 'stuff' we're doing is closing the port and exiting the program. Let's refactor to do some more interesting 'stuff'. 

We'll set up our server to send back a response. For now, we'll respond to every request with `Hello World!`. The `connection` has methods like `puts` and `gets` we can use to communicate with the client.

Notice that above we set two variables we haven't used yet. `client_connection` and `client_address`. Let's think of `client_connection` as our direct line to the client. This is how we will be able to send and receive data.  

Take a look at the [docs for socket](https://docs.python.org/2/library/socket.html#socket.AF_INET). What method can you use to send some data back to the client? Where will this code need to go? 

Modify the code in `server.py` so that each time the client makes an HTTP `GET` request to 
our server, they get `Hello World!` as a response. 

```
  http_server_one :> curl http://localhost:9292
  curl: (56) Recv failure: Connection reset by peer
  Hello World!
```
You may or may not see the second line. Either way, we'll ignore it for now. The important thing is that somewhere you see `Hello World!` appear. 

You've successfully completed your first request/response cycle! This cycle is what the whole internet is built on. It can be hard to grasp at first, since we are running both the server AND the client on our own computer, but this same concept is what allows a server in California to respond to an HTTP request sent from a browser in NYC. 

Everything we do from here will build out from this simple concept. Our client (for now that will be `curl`. Later if will be the browser) makes a request to our server and our server responds. 

### Keeping Our Server Running. 
Right now our server quits after sending a response. But we want to keep the server running so it can handle multiple requests. 

One thing we can do right now is to use a `while` loop to keep the server running. Modify the your code in `server.py` so that after the server responds, it starts listening again for new requests. 

Try making a couple of requests with curl. Your server should respond each time and shouldn't stop running until you press `ctrl + c`. Great. We'll still have to stop and start our server when we make changes to the code, but at least we can make multiple requests without the program exiting. For now, that'll work. 

## Release 1 - HTTP Protocol. 

Right now we are responding with a simple string. Let's modify our code to respond with a standard HTTP response. [This article](https://code.tutsplus.com/tutorials/http-the-protocol-every-web-developer-must-know-part-1--net-31177) is a great resource if you're not already familiar with HTTP. 

It's important that we format our response correctly. According to the HTTP protocol, the first thing we send should be our protocol, in this case `HTTP/1.1`, followed by a carriage return (`\r\n`). Next, we can provide any number of headers. Which headers should we include? The last thing we return is the body of our response. This is our main content. Instead of responding with `Hello World!`, add some basic `HTML`. 

After you've modified `server.py`, start the server again and make another request with `curl`. You should get something like this: 

```
http_server_one :> curl http://localhost:9292
<html><body><p>Hello World!</p></body></html>
```
`curl` doesn't parse HTML so we should just get the string back. Once the output from `curl` looks correct, try connecting with a browser. Did the browser display your response as HTML?

Our server is just barely an HTTP server, but it's a start! We're able to make requests and receive a valid HTTP response.

## Release 2 - Request Parsing
So far we are completely ignoring the request. We want our server to be able to respond in different ways depending on what kind of request the client sends. Start by checking the docs for a method that will allow you to recv data from the client. 

##### NOTE: 
Sockets in Python receive data as bytes. You may have to use `.decode('utf-8')` to convert those bytes to strings. `Print()`data as it comes in to test it. 

Once you figure out how to receive data, print it to the terminal. You should have something like this:  
```
Waiting for connection...
GET / HTTP/1.1
Host: localhost:8888
User-Agent: curl/7.60.0
Accept: */*

```
Right now we are just going to focus on the first line, `GET / HTTP/1.1`.  We know from rigorous study of the HTTP protocol that this request line tells us the `method` followed by the `path` followed by the `protocol`. We can use this information to decide how to respond.

Ok. So we can get access to our request. Now we want to start making decisions based on the requested `path`. Modify your code in `server.py` so that a request to `/` responds with our `<html><body><h1>Hello World!</h1></body></html>`, but a request to `/time` returns the current time. 


## Release 3 - Request Parsing

At this point we are not doing a great job of separating our concerns. Our server should just be in charge of getting a request and serving up a response. Let's create a `Request` class to handle parsing our request to make it easier to handle. First, let's create a new file `request.py` and build out our class. Here's some code to get you started, but the class incomplete. Take some time to figure out what each line is doing. You'll have to write your own `parse_headers()` method. It should return a dictionary containing all headers from the HTTP request. `{'host': 'localhost:8888', 'user-agent': 'curl/7.60.0', 'accept': '*/*'}` 

```Python 
# request.py 
class Request: 
  
  def __init__(self, request_text):
    self.request      = request_text.split('\r\n')
    self.request_line = self.request.pop(0).split(' ')
    self.headers      = self.parse_headers()
    self.method       = self.request_line[0]
    self.path         = self.request_line[1]
    self.url          = self.headers['host']

```


Now we can update our `server.py` file to use our new `Request` class. 

```Python
# server.py 
# ............this is not the complete file. You'll have code above and below what is shown here. 
while True:
  
    client_connection, client_address = listen_socket.accept()
    # we listen for a request. Then we need to convert it from bytes to a string with decode. 
    request_text = client_connection.recv(1024).decode('utf-8')
    request = Request(request_text) # create a request object. 

    if request.path == '/':
        protocol = 'HTTP/1.1 200 OK\r\n'
        body_response = '<html><body><h1>Hello World!</h1></body></html>'
        content_type = 'Content Type: text/html\r\n'
        content_length = f'Content Length: {len(body_response)}\r\n'
        
        client_connection.send(protocol.encode())
        client_connection.send(content_type.encode())
        client_connection.send(content_length.encode())
        client_connection.send('\r\n'.encode())
        client_connection.send(body_response.encode())
        
```
Be sure to import our new file. Then we create a new instance of `Request` and pass it our `request_text` variable. Our program should run as before. 

