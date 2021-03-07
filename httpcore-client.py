import httpcore
import helloworld_pb2

headers = [
    (b"content-type", b"application/grpc+proto"),
    (b"grpc-message-type", b"helloworld.HelloRequest"),
    (b"grpc-encoding", b"identity"),
]

request = helloworld_pb2.HelloRequest(name="world")
serialized_request = request.SerializeToString()

with httpcore.SyncConnectionPool(http2=True) as http:
    status_code, headers, stream, ext = http.request(
        method=b"POST",
        url=(b"http", b"127.0.0.1", 50051, b"/helloworld.Greeter/SayHello"),
        headers=[(b"host", b"127.0.0.1"), *headers],
    )

    try:
        body = b"".join([chunk for chunk in stream])
    finally:
        stream.close()

    print(status_code, body)
