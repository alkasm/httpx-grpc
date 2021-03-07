import httpx
import helloworld_pb2

headers = {
    "content-type": "application/grpc+proto",
    "grpc-message-type": "helloworld.HelloRequest",
    "grpc-encoding": "identity",
}
host = "http://127.0.0.1:50051"
route = "/helloworld.Greeter/SayHello"


request = helloworld_pb2.HelloRequest(name="world")
serialized_request = request.SerializeToString()
with httpx.Client(base_url=host, http2=True) as client:
    response = client.post(route, content=serialized_request, headers=headers)

print(response)
print(response.text)
