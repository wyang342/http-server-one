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
server.listen()

client_connection, _client_address = server.accept()
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
As the client we want to be able to make a request to our server, which is our machine listening on local host 9292. We have many choices here. We can make a request via chrome or any other browser, we can use [Postman](https://www.getpostman.com), or we can use [Curl](https://curl.haxx.se/) to make a request from the command line.

Let's start with Curl. Open a separate command line window and run `curl http://localhost:9292`. `curl http://localhost:9292` will make a `GET` request to `http://localhost:9292`. The important thing to note here is the port number at the end. Because we opened our server on port `9292`, we need to make sure that we make our request to the same port. 

After you run the code, the server should accept the connection, print "New connection received", and then exit. Not very exciting, but it's important to note that this first step is what every web service is based on. A server listens for a connection, when a connection is made, it does some stuff. Right now the 'stuff' we're doing is printing 'new connection received' and closing the port and exiting the program. Let's refactor to do some more interesting 'stuff'. For now, we'll respond to every request with `Hello World!`. The `connection` has methods like `send` and `recv` we can use to communicate with the client.

`client_connection` is our direct line to the client. This is how we will be able to send and receive data.  

Take a look at the [docs for socket](https://docs.python.org/3/library/socket.html). What method can you use to send some data back to the client? Where will this code need to go? Modify the code in `server.py` so that each time the client makes an HTTP `GET` request to our server, they get `Hello World!` as a response. 

```
  http_server_one :> curl http://localhost:9292
  curl: (56) Recv failure: Connection reset by peer
  Hello World!
``` 

You've successfully completed your first request/response cycle! This cycle is what the whole internet is built on. It can be hard to grasp at first, since we are running both the server AND the client on our own computer, but this same concept is what allows a server in California to respond to an HTTP request sent from a browser in NYC. 

Everything we do from here will build out from this simple concept. Our client (for now that will be `curl`. Later if will be the Postman) makes a request to our server and our server responds. 

### Keeping Our Server Running. 
Right now our server quits after sending a response. But we want to keep the server running so it can handle multiple requests. 

One thing we can do right now is to use a `while` loop to keep the server running. Modify the your code in `server.py` so that after the server responds, it starts listening again for new requests. 

Try making a couple of requests with curl. Your server should respond each time and shouldn't stop running until you press `ctrl + c`. Great. We'll still have to stop and start our server when we make changes to the code, but at least we can make multiple requests without the program exiting. For now, that'll work. 

## Release 1 - HTTP Protocol. 

Right now we are responding with a simple string. Let's modify our code to respond with a standard HTTP response. [This article](https://code.tutsplus.com/tutorials/http-the-protocol-every-web-developer-must-know-part-1--net-31177) is a great resource if you're not already familiar with HTTP. 

It's important that we format our response correctly. According to the HTTP protocol, chrome requires the following headers:
* HTTP protocol (`HTTP/1.1 STATUS_CODE REASON_PHRASE`)
* Content-Type (what type of content you are sending back.)
* Content-Length 
* A blank new line
* The body of the response. (In this case, the HTML)
Between everything you need a carraige return `\r\n`. 
The last thing we return is the body of our response. This is our main content. Instead of responding with `Hello World!`, add some basic `HTML`. 

After you've modified `server.py`, start the server again and make another request with `curl`. You should get something like this: 

```
http_server_one :> curl http://localhost:9292
<html><body><p>Hello World!</p></body></html>
```
`curl` doesn't parse HTML so we should just get the string back. Once the output from `curl` looks correct, try connecting with a browser. Did the browser display your response as HTML?

Our server is just barely an HTTP server, but it's a start! We're able to make requests and receive a valid HTTP response.

## Release 2 - Request Parsing
So far we are completely ignoring the request. We want our server to be able to respond in different ways depending on what kind of request the client sends. Start by checking the [docs](https://docs.python.org/3/library/socket.html) for a method that will allow you to receive data from the client. 

**NOTE: 
Sockets in Python receive data as bytes. You may have to use `.decode('utf-8')` to convert those bytes to strings. `print()`data as it comes in to test it.**

Once you figure out how to receive data, print it to the terminal. You should have something like this:  
```
Waiting for connection...
GET / HTTP/1.1
Host: localhost:8888
User-Agent: curl/7.60.0
Accept: */*

```
Based off of the URN (after the HTTP method) we want to be able to route the user to different pages. Your job is to parse the request, get the URN and respond with 'Hello World' if it is `/` and return the current time if the request is `/time`. 

Ok. So we can get access to our request. Now we want to start making decisions based on the requested `path`. Modify your code in `server.py` so that a request to `/hello` responds with our `<html><body><h1>Hello World!</h1></body></html>`, but a request to `/time` returns the current time. 


## Release 3 - Making Our Code Single Responsibility 

At this point we are not doing a great job of separating our concerns. Our server should just be in charge of getting a request and serving up a response. Let's create a `Request` class to handle parsing our request to make it easier to handle. First, let's create a new file `request.py` and build out our class. Here's some code to get you started, but the class is incomplete. Take some time to figure out what each line is doing. You'll have to write your own `parse_headers()` method. It should return a dictionary containing all headers from the HTTP request. `{'host': 'localhost:8888', 'user-agent': 'curl/7.60.0', 'accept': '*/*'}` 

```Python 
# request.py 
class Request: 
  
  class Request:
    def __init__(self, request_text):
      self.parse_request(request_text.recv(1024).decode('utf-8').split('\r\n'))

```


Now we can update our `server.py` file to use our new `Request` class. 

```Python
# server.py 
# ............this is not the complete file. You'll have code above and below what is shown here. 
import socket
import datetime
from request import Request

def build_html_response(text_body):
  html_body = f'<html><head><title>An Example Page</title></head><body>{text_body}</body></html>'
  return f"HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-Length:{len(html_body)}\r\n\r\n{html_body}"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('localhost', 9291))

while True:
    server.listen()
    client_connection, _client_address = server.accept()
    client_request = Request(client_connection)
    if client_request.parsed_request['urn'] == '/':
        client_connection.send(build_html_response('Hello World').encode())
    elif client_request.parsed_request['urn'] == '/time':
        # Your code here
        
```
Be sure to import our new file. Then we create a new instance of `Request` and pass it our `request_text` variable. Our program should run as before. 

