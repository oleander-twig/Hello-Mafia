import Mafia_pb2_grpc
import Mafia_pb2
import grpc
from concurrent import futures
from threading import Lock


class Game(Mafia_pb2_grpc.GameServicer):

    players = []
    lock = Lock()
    number_of_players = 0

    def UpdatePlayers(self, request, context):
        for player in self.players:
            yield Mafia_pb2.Info(message=player)

    def JoinGame(self, request, context):
        self.players.append(request.message)

        print(request.message+' has joined')

        self.UpdatePlayers(request.message, '')
        
        return Mafia_pb2.Answer(emptyMessage='')
    
    def LeaveGame(self, request, context):

        self.lock.acquire()
        self.players.remove(request.message)
        self.lock.release()

        print(request.message+' has left')

        self.UpdatePlayers(request.message, '')

        return Mafia_pb2.Answer(emptyMessage='')


def serve():
  server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
  Mafia_pb2_grpc.add_GameServicer_to_server(
      Game(), server)
  server.add_insecure_port('[::]:50051')
  server.start()
  server.wait_for_termination()

serve()
