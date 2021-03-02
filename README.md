# HTTP Server One

## What We're Building
For this challenge we are going to build an HTTP server using  Python. We'll use a lot of what we've learned so far, but some of the techniques we utilize to accomplish this will be entirely new. Don't worry. The point of this exercise is not to become an expert at building servers; there are many tools out there that already do what we are going to do and do it wayyyy better. This project is to learn about separation of concerns (i.e., single responsibility code), reinforce OOP / OOP principles, and learn about HTTP concepts.

## Release 0 - Hello World
HTTP servers speak over the networking protocol TCP/IP. It turns out HTTP requests and responses aren't sent over the web as single blobs of text. Instead, they're transferred over as smaller packets and re-assembled at their final destination. TCP/IP is the protocol that makes this lower-level communication happen.

Lucky for us, we don't have to learn TCP/IP from scratch to write an HTTP server. Python ships with a TCP server library called [socket](https://docs.python.org/3/library/socket.html) that we can use, allowing us to focus on HTTP.

#### Hello World Server
Inside of `server.py`, you will see the following code:

```python
import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # so you don't have to change ports when restarting
server.bind(('localhost', 9292))
print('Waiting For Connection...')
server.listen()

client_connection, _client_address = server.accept()
print('New Connection received!')

client_connection.close()
```

Let's walk through the code here. First, we import the `socket` library built into Python. Next, we create a new socket instance and save it to the variable `server`. We are passing our new socket two arguments:
1. `AF_INET` - this is to define the address family we will be using
2. `SOCK_STREAM` - this is the type of socket we want to use

Next we bind our new socket to a host and port. We'll use `localhost` as our host - this is the address for our local machine. Then, we bind it to port `9292` (this is an arbitrary port number - we could put any 4-digit number in here). 

After that, we tell the socket to start listening for a connection from a client. Then, we print "Waiting for connection..." to the terminal.

Our program will pause here and wait until it receives a connection. After it receives one, it will print "New connection received". `client_connection.close()` will close the connection. 

To get started, run `server.py` in the terminal.

```
http_server_one :> python server.py
Waiting for connection...
```

As the client, we want to be able to make a request to the server listening on port 9292. We have many choices in how we make requests to the server:
- Chrome or any other browser
- [Postman](https://www.getpostman.com) - a GUI request maker
- [Curl](https://curl.haxx.se/) - a non GUI request maker

Let's start with Curl. __Open a separate command line window and run:__

```sh
$ curl http://localhost:9292
```

This will make a `GET` request to `http://localhost:9292`. After you run the code, the server should accept the connection, print "New connection received", and then exit. Not very exciting, but it's important to note that this first step is what every web service is based on. A server listens for a connection, a connection is made, the server does some stuff, and returns a response. In our case, the 'stuff' we're doing is printing "new connection received", closing the port, and exiting the program.

Let's refactor to do something more interesting - let's respond to every request with `Hello World!` To do this, we will use the `client_connection` variable to send/receive data. `client_connection` is a [socket object](https://docs.python.org/3/library/socket.html). Read through the documentation to find some methods that can `send` data. Then, modify the code in `server.py` so that each time the client makes an HTTP `GET` request to our server, they get `Hello World!` as a response:

```sh
http_server_one :> curl http://localhost:9292
Hello World!
``` 

You've successfully completed your first request/response cycle! This cycle is what the whole internet is built on. It can be hard to grasp at first, since we are running both the server AND the client on our own computer, but this same concept is what allows a server in California to respond to an HTTP request sent from a browser in NYC. Everything we do from here will build out from this simple concept.

#### Keeping Our Server Running
Right now, our server quits after sending a response. We want to keep the server running so that it can handle multiple requests.

We can solve this issue by having a `while` loop to keep the server running. Modify your code in `server.py` so that after the server responds, it starts listening again for new requests.

Try making a couple of requests with Curl. Your server should respond each time and shouldn't stop running until you press `ctrl c`. 

## Release 1 - HTTP Protocol
Right now, we are responding with a simple string. Let's modify our code to respond with a standard [HTTP response](https://code.tutsplus.com/tutorials/http-the-protocol-every-web-developer-must-know-part-1--net-31177).

In order for our response to show up in Chrome, have to format it to include at least the following:
* HTTP protocol (i.e., `HTTP/1.1 STATUS_CODE REASON_PHRASE`)
* Content-Type (i.e., what type of content you are sending back?)
* Content-Length  (i.e., how long is the response?)
* A blank new line (`\r\n`)
* The body of the response (i.e., in our case, it's an HTML string)
    * Let's replace our "Hello World" string with `<html><body><p>Hello World!</p></body></html>`

You need a carriage return (`\r\n`) between every line.

<details>
<summary>HTTP Hint</summary>
<br>
The below is a string representation of the HTTP Protocol.
   
"HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-Length:len(html_text)\r\n\r\n{html_text}"

</details>

After you've modified `server.py`, start the server again and make another request with `curl`. You should get something like this:

```bash
http_server_one :> curl http://localhost:9292
<html><body><p>Hello World!</p></body></html>
```

Once the output from `curl` looks correct, try making a request with a browser. Ensure that the browser displays "Hello World" before moving forward.

## Release 2 - Parsing our Request
We are currently ignoring the request. We want our server to be able to respond in different ways depending on what kind of request the client sends. Start by checking the [socket documentation](https://docs.python.org/3/library/socket.html) to find a method that will allow you to `recv` data from the client.

__Sockets in Python receive data as `bytes`. You will have to use `.decode('utf-8')` to convert those bytes to strings.__

Once you figure out how to receive data, print the request to the terminal. You should have something like this:  

```bash
Waiting for connection...
GET / HTTP/1.1
Host: localhost:8888
User-Agent: curl/7.60.0
Accept: */*
```

Based off of the URI, we want to be respond differently:
- If the URI is `/`, respond with 'Hello World'
- If the URI is `/time`, respond with the `The current time is INSERT_TIME_HERE`

## Release 3 - Single Responsibility Principle
At this point, we are not doing a great job of separating our concerns (i.e., following the single responsibility principle) because our server does more than it should - it's receiving a request, parsing the request, and sending a response.

Let's make our code follow the Single Responsibility (i.e., every piece of code should do one thing) a bit better by creating a `Request` class that parses the request that comes in. 

First, let's create a new file `request.py` and build out our class:

```Python 
# request.py 
class Request:
    def __init__(self, request_text):
        self.parse_request(request_text.recv(4096).decode('utf-8').split('\r\n'))
    
    def parse_request(self, decoded_request_text):
        self.parsed_request = {}
```

Take some time to figure out what's going on and finish fleshing out the `parse_request()` method. In the end, you want this method to return a dictionary that contains all the headers from the HTTP request: 

```python
{'host': 'localhost:9292', 'uri': '/', 'user-agent': 'curl/7.60.0', 'accept': '*/*', }
```

After that's done, we can update our `server.py` file to use our new `Request` class: 

```Python
import socket
import datetime
from request import Request

def build_html_response(text_body):
  html_body = f'<html><head><title>An Example Page</title></head><body>{text_body}</body></html>'
  return f"HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-Length:{len(html_body)}\r\n\r\n{html_body}"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # so you don't have to change ports when restarting
server.bind(('localhost', 9292))

while True:
    server.listen()
    client_connection, _client_address = server.accept()
    client_request = Request(client_connection)
    if client_request.parsed_request['uri'] == '/':
        client_connection.send(build_html_response('Hello World').encode())
    elif client_request.parsed_request['uri'] == '/time':
        # Your code here
```
