import socket
import threading
import time
import sys

# Define the server address and port
HOST = '127.0.0.1' 
defaultPort = 80

portChange = defaultPort # Localhost
# Port to listen on



def handle_connection(client_socket, client_address):
    global portChange
    with client_socket:
        buffer = b''
        print(f"Connected by {client_address}")
        while True:
            # Receive data from the client
            data = client_socket.recv(1024)
            buffer+=data
            print(buffer)
            
            if b'\r\n' in buffer:
                newBuffer = buffer.split(b'\r\n')
                print(newBuffer)
                if b'-p' in buffer:
                    port_part = buffer.split(b'-p')[1].strip()
                    print(port_part)
                    new_port = int(port_part.decode())
                    if new_port != portChange:
                        portChange = new_port
                        print("i am port change: ", portChange)
                        restartServer()
        
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
   print("startserver90: ", portChange)
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