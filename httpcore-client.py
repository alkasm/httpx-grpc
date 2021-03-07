import httpcore
import helloworld_pb2

headers = [
    (b"content-type", b"application/grpc+proto"),
    (b"grpc-message-type", b"helloworld.HelloRequest"),
    (b"grpc-encoding", b"identity"),
]

request = helloworld_pb2.HelloRequest(name="world")
serialized_request = request.SerializeToString()
content_length = len(serialized_request)
req_stream = httpcore.PlainByteStream(serialized_request)

with httpcore.SyncConnectionPool(http2=True) as http:
    status_code, headers, stream, ext = http.request(
        method=b"POST",
        url=(b"http", b"127.0.0.1", 50051, b"/helloworld.Greeter/SayHello"),
        headers=[
            (b"host", b"127.0.0.1"),
            (b"content-length", str(content_length).encode()),
            *headers,
        ],
        stream=req_stream,
    )

    try:
        body = b"".join([chunk for chunk in stream])
    finally:
        stream.close()

    print(status_code, body)
