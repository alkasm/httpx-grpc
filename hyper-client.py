import hyper

headers = dict(
    [
        ("te", "trailers"),
        ("content-type", "application/grpc"),
        ("user-agent", "grpc-python"),
        ("grpc-accept-encoding", "identity,deflate,gzip"),
        ("accept-encoding", "identity,gzip"),
    ]
)

conn = hyper.HTTP20Connection("http://127.0.0.1", 50051, force_proto="h2", secure=False)
conn.request("POST", "/helloworld.Greeter/SayHello", b"\n\x04asdf", headers)
response = conn.get_response()
print("Response Headers:", response.headers)
data = response.read()
print(data)
