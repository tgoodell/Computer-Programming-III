                                                                                                                                                                     

import socket               # Import socket module

import random

s = socket.socket()         # Create a socket object
host = "localhost" # Get local machine name
port = 50000                # Reserve a port for your service.

print('Server started!')
print('Waiting for clients...')

s.bind((host, port))        # Bind to the port
s.listen()                 # Now wait for client connection.
conn1,addr1=s.accept()
conn2,addr2=s.accept()
word=b"_____"
guesses=b""
while True:
    conn1.sendall(b"%s [%s]"%(word,guesses))
    guess = conn1.recv(1024)
    print(b"%s [%s,%s]"%(word,guesses,guess))
    conn2.sendall(b"%s [%s,%s]"%(word,guesses,guess))
    word = conn2.recv(1024)
    guesses+=guess
    if b"_" not in word:
        word=b"_"*random.randint(2,12)
        guesses=b""
    
    print(b"%s [%s]"%(word,guesses))
    

s.close()
