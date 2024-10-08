import socket
import pymongo
from datetime import datetime
import json

def start_socket_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5000))
    server_socket.listen(5)
    print('Socket server running on port 5000')
    
    client = pymongo.MongoClient('mongodb://mongo:27017/')
    db = client['messages_db']
    collection = db['messages']

    while True:
        client_socket, addr = server_socket.accept()
        data = client_socket.recv(1024).decode('utf-8')
        message_data = json.loads(data.replace("'", '"'))  
        message_data['date'] = str(datetime.now()) 
        collection.insert_one(message_data)
        print(f'Message saved to DB: {message_data}')
        client_socket.close()

if __name__ == "__main__":
    start_socket_server()
