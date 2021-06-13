# request.py
class Request:
    def __init__(self, request_text):
        self.parse_request(request_text.recv(
            4096).decode('utf-8').split('\r\n'))

    def parse_request(self, decoded_request_text):
        self.parsed_request = {}
        self.parsed_request['host'] = decoded_request_text[1].split(' ')[1]
        self.parsed_request['uri'] = decoded_request_text[0].split(' ')[1]
        self.parsed_request['user-agent'] = decoded_request_text[2].split(' ')[
            1]
        self.parsed_request['accept'] = decoded_request_text[3].split(' ')[1]
        return self.parsed_request
