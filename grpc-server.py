from concurrent.futures import ThreadPoolExecutor
import grpc
import helloworld_pb2, helloworld_pb2_grpc


class GreeterServicer(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message="Hello " + request.name)


executor = ThreadPoolExecutor(max_workers=1)
server = grpc.server(executor)

servicer = GreeterServicer()
helloworld_pb2_grpc.add_GreeterServicer_to_server(servicer, server)

server.add_insecure_port("127.0.0.1:50051")

server.start()
server.wait_for_termination()
