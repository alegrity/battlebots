#-------------------------------------------- Imports ----------------------------------------------------------------

import socket
from start import  turn_on_led1, turn_off_led1, turn_on_led2, turn_off_led2, slider, joystick
from RobotInteractions import *

#-------------------------------------------- Server -----------------------------------------------------------------

def serve_file(file_path, content_type):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        response = f"HTTP/1.1 200 OK\r\nContent-Type: {content_type}\r\n\r\n{content}"
    except OSError:
        response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found"
    return response

def parse_get_data(query_string):
    parsed_data = {}
    if query_string:
        pairs = query_string.split('&')
        for pair in pairs:
            key, value = pair.split('=', 1)
            parsed_data[key] = value
    return parsed_data

def start_web_server():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.bind(addr)
    s.listen(1)
    print('Listening on', addr)

    running = True

    while running:
        cl, addr = s.accept()
        print('Client connected from', addr)
        
        request = cl.recv(1024)
        request_str = request.decode('utf-8')
        print(request_str)

        if 'POST' in request_str:
            parsed_data = parse_get_data(request)
            if '/vector' in request_str:
                x = parsed_data.get('x', 'not received')
                y = parsed_data.get('y', 'not received')
                print(f'Vector data - x: {x}, y: {y}')
            elif '/slider' in request_str:
                value = parsed_data.get('value', 'not received')
                print(f'Slider data - value: {value}')
            elif '/button1' in request_str:
                turn_on_led1()
                print('Button 1 pressed - LED 1 ON')
            elif '/button2' in request_str:
                turn_off_led1()
                print('Button 2 pressed - LED 1 OFF')
            elif '/button3' in request_str:
                turn_on_led2()
                print('Button 3 pressed - LED 2 ON')
            elif '/button4' in request_str:
                turn_off_led2()
                print('Button 4 pressed - LED 2 OFF')

        elif 'GET' in request_str:
            request_line = request_str.split('\r\n')[0]
            method, path, _ = request_line.split()
            query_string = path.split('?')[1] if '?' in path else ''

            parsed_data = parse_get_data(query_string)

            if '/vector' in path:
                x = parsed_data.get('x', 'not received')
                y = parsed_data.get('y', 'not received')
                joystick(x, y)
                moveXY(x,y)
            elif '/slider' in path:
                value = parsed_data.get('value', 'not received')
                slider(value)
            elif '/button1' in path:
                turn_on_led1()
                print('Button 1 pressed - LED 1 ON')
            elif '/button2' in path:
                turn_off_led1()
                print('Button 2 pressed - LED 1 OFF')
            elif '/button3' in path:
                turn_on_led2()
                print('Button 3 pressed - LED 2 ON')
            elif '/button4' in path:
                turn_off_led2()
                print('Button 4 pressed - LED 2 OFF')
            elif '/button5' in path:
                running = False
                cl.close()
                
                break
            if 'GET /style.css' in request_str:
                response = serve_file('style.css', 'text/css')
            elif 'GET /script.js' in request_str:
                response = serve_file('script.js', 'application/javascript')
            elif 'GET /' in request_str or 'GET /index.html' in request_str:
                response = serve_file('index.html', 'text/html')
            else:
                response = "HTTP/1.1 404 Not Found\r\n\r\nFile not found"

            cl.send(response)

        cl.close()
