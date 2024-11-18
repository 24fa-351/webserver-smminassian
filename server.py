import socket
import threading
import time
import sys

# Define the server address and port
HOST = '127.0.0.1' 
defaultPort = 80

portChange = defaultPort # Localhost
# Port to listen on
tot_requests = 0
tot_bytes_received = 0
tot_bytes_sent = 0


http_format = """
                        -------------------
                        HTTP/1.1 200 OK
                        Date: Wed, 06 Nov 2024 20:22:58 GMT
                        Server: Apache
                        Last-Modified: Thu, 05 Nov 2018 04:53:39 GMT
                        Etag: "ec-523c3e9170d07
                        Accept-Ranges: bytes
                        Content-Length: 
                        Vary: Accept-Encoding
                        Content-Type: text/html


"""

def handle_connection(client_socket, client_address):
    global portChange, tot_requests, tot_bytes_received, tot_bytes_sent
    with client_socket:
        buffer = b''
        print(f"Connected by {client_address}")
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            buffer+=data
            tot_requests += 1
            tot_bytes_received += len(buffer)
            print(buffer)
            if b'GET' in buffer:
                if b'\r\n' in buffer:
                    newBuffer = buffer.split(b'\r\n')
                    print(newBuffer)
                    if b'/calc/' in buffer:
                        queryString = buffer.split(b'/calc/')[1].strip()
                        print("I am ", queryString)
                        queryString = str(queryString)
                        queryNum1 = queryString[2]
                        queryNum2 = queryString[4]
                        queryNum1 = int(queryNum1)
                        queryNum2 = int(queryNum2)
                        print("num1", queryNum1)
                        print("num2", queryNum2)

                        sum = queryNum1 + queryNum2

                        sumToString = str(sum)

                        sumInBytes = sumToString.encode()

                        client_socket.sendall(sumInBytes)
                    if b'-p' in buffer:
                        port_part = buffer.split(b'-p')[1].strip()
                        print(port_part)
                        new_port = int(port_part.decode())
                        if new_port != portChange:
                            portChange = new_port
                            print("i am port change: ", portChange)
                            restartServer()
                    if b'/stat' in buffer:
                        response = f"""
                        {http_format}
                        <html>
                        <head>Server Stats</title></head>
                        <body>
                            <h1>Server Stats</h1>
                            <p>Total Requests: {tot_requests}</p>
                            <p>Total bytes Received: {tot_bytes_received}</p>
                            <p>Total Bytes Sent: {tot_bytes_sent}
                            
                        </body>
                        </html>
                        """
                        responseInBytes = response.encode()
                        tot_bytes_sent += len(responseInBytes)
                        client_socket.sendall(responseInBytes)
                for actualMessage in newBuffer[:-1]:
                    print("Received: ", actualMessage)
                    client_socket.sendall(actualMessage)
                        
            
                buffer = newBuffer[-1]

def restartServer():
    global echo_server, portChange
    echo_server.close()
    print("Restarting Server")
    print(portChange)

    time.sleep(2)

    
    start_server()





def start_server():
   global echo_server, portChange
   print("startserver on ", portChange)
   echo_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
   try:
        
        echo_server.bind((HOST, portChange))

        echo_server.listen()

        print(f"Server is listening on {HOST}:{portChange}")

        while True:
        # Accept a client connection
            client_socket, client_address = echo_server.accept()
        # Create a new thread for each client connection
            client_thread = threading.Thread(target=handle_connection, args=(client_socket, client_address))
            client_thread.start()
   except OSError as e:
       print(portChange)
       print("Error binding to the port", portChange, {e})
       sys.exit(1)


if __name__ == "__main__":
    start_server()


# done - Create a server that listens on a port (default: 80, changeable with a "-p" option).

# Accept HTTP/1.1. One message at a time, no pipelining. 

# Implement "/static" which allows the requester to specify the name of a file in a "/static" directory. Ex: "/static/images/rex.png", returns the binary file that is there accessible to your server.

# Implement "/stats" which returns a properly formatted HTML doc that lists the number of requests received so far, and the total of received bytes and sent bytes.

# Implement "/calc" which returns text or HTML, summing the value of two query params in the request named "a" and "b" (both numeric).

# done -Make it multithreaded!

# Submit: GHC repo link after you accept: https://classroom.github.com/a/2GNAdIbSLinks to an external site. 