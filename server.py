import socket
from datetime import datetime
from request import Request


def build_html_response(text_body):
    html_body = f'<html><head><title>An Example Page</title></head><body>{text_body}</body></html>'
    return f"HTTP/1.1 200 OK\r\nContent-Type:text/html\r\nContent-Length:{len(html_body)}\r\n\r\n{html_body}"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# so you don't have to change ports when restarting
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('localhost', 9292))

while True:
    server.listen()
    client_connection, _client_address = server.accept()
    client_request = Request(client_connection)
    if client_request.parsed_request['uri'] == '/':
        client_connection.send(build_html_response('Hello World').encode())
    elif client_request.parsed_request['uri'] == '/time':
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        client_connection.send(build_html_response(
            "Current time is : " + current_time).encode())
