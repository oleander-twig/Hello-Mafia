import Mafia_pb2_grpc
import Mafia_pb2
import grpc
import threading
import time


players = []

def MonitorePlayers(stub):
    global players

    response = stub.UpdatePlayers(Mafia_pb2.Request(message = name))
    while response:
        players = stub.UpdatePlayers(Mafia_pb2.Request(message = name)) 

def WritePlayers():
    global players

    while True:

        print("Current list of players:")

        for user in players:
                print(user.message)
        
        time.sleep(10)

name = input("Enter your Name, please:", )
host = input("Enter your Host, please:", )
port = input("Enter your Port, please:", )

channel = grpc.insecure_channel(host+':'+port)
stub = Mafia_pb2_grpc.GameStub(channel)

response = stub.JoinGame(Mafia_pb2.Request(message = name))

try:
    print("You are in the Game right now!")

    t1 = threading.Thread(target=MonitorePlayers, args=([stub]))
    t2 = threading.Thread(target=WritePlayers, args=())

    t1.start()
    t2.start()

    t1.join()
    t2.join()

except KeyboardInterrupt:
    response = stub.LeaveGame(Mafia_pb2.Request(message = name))
