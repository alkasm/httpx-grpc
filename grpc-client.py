import grpc
import helloworld_pb2, helloworld_pb2_grpc

channel = grpc.insecure_channel("[::]:50051")
stub = helloworld_pb2_grpc.GreeterStub(channel)
request = helloworld_pb2.HelloRequest(name="world")
response = stub.SayHello(request)
print(response.message)
