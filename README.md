Attempt at using httpx as a client for gRPC calls over HTTP/2.

The `httpcore` library seems to think the connection is HTTP/1.1 and not HTTP/2 over 127.0.0.1. 

Install the dependencies: `pip install -r requirements.txt` (alternatively `pip install httpx[http2] grpcio protobuf`)

Start the local gRPC server on 50051: `python grpc-server.py`

gRPC client (works): `python grpc-client.py`
<details><summary>output</summary>
Hello world
</details>

httpx client (doesn't work): `python httpx-client.py`
<details><summary>output</summary>

```
$ python httpx-client.py 
Traceback (most recent call last):
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpx/_exceptions.py", line 326, in map_exceptions
    yield
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpx/_client.py", line 869, in _send_single_request
    ext={"timeout": timeout.as_dict()},
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpx/_transports/default.py", line 102, in request
    return self._pool.request(method, url, headers=headers, stream=stream, ext=ext)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_sync/connection_pool.py", line 219, in request
    method, url, headers=headers, stream=stream, ext=ext
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_sync/connection.py", line 115, in request
    return self.connection.request(method, url, headers, stream, ext)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_sync/http11.py", line 72, in request
    ) = self._receive_response(timeout)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_sync/http11.py", line 133, in _receive_response
    event = self._receive_event(timeout)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_sync/http11.py", line 169, in _receive_event
    event = self.h11_state.next_event()
  File "/Users/alkasm/.pyenv/versions/3.7.7/lib/python3.7/contextlib.py", line 130, in __exit__
    self.gen.throw(type, value, traceback)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_exceptions.py", line 12, in map_exceptions
    raise to_exc(exc) from None
httpcore.RemoteProtocolError: illegal request line

The above exception was the direct cause of the following exception:

Traceback (most recent call last):
  File "httpx-client.py", line 16, in <module>
    response = client.post(route, content=serialized_request, headers=headers)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpx/_client.py", line 1008, in post
    timeout=timeout,
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpx/_client.py", line 729, in request
    request, auth=auth, allow_redirects=allow_redirects, timeout=timeout
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpx/_client.py", line 770, in send
    history=[],
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpx/_client.py", line 810, in _send_handling_auth
    history=history,
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpx/_client.py", line 839, in _send_handling_redirects
    response = self._send_single_request(request, timeout)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpx/_client.py", line 869, in _send_single_request
    ext={"timeout": timeout.as_dict()},
  File "/Users/alkasm/.pyenv/versions/3.7.7/lib/python3.7/contextlib.py", line 130, in __exit__
    self.gen.throw(type, value, traceback)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpx/_exceptions.py", line 343, in map_exceptions
    raise mapped_exc(message, **kwargs) from exc  # type: ignore
httpx.RemoteProtocolError: illegal request line
```
</details>

httpcore client (doesn't work): `python httpcore-client.py`
<details><summary>output</summary>

```
$ python httpcore-client.py 
Traceback (most recent call last):
  File "httpcore-client.py", line 17, in <module>
    headers=[(b"host", b"127.0.0.1"), *headers],
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_sync/connection_pool.py", line 219, in request
    method, url, headers=headers, stream=stream, ext=ext
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_sync/connection.py", line 115, in request
    return self.connection.request(method, url, headers, stream, ext)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_sync/http11.py", line 72, in request
    ) = self._receive_response(timeout)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_sync/http11.py", line 133, in _receive_response
    event = self._receive_event(timeout)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_sync/http11.py", line 169, in _receive_event
    event = self.h11_state.next_event()
  File "/Users/alkasm/.pyenv/versions/3.7.7/lib/python3.7/contextlib.py", line 130, in __exit__
    self.gen.throw(type, value, traceback)
  File "/Users/alkasm/prog/httpx-grpc/venv/lib/python3.7/site-packages/httpcore/_exceptions.py", line 12, in map_exceptions
    raise to_exc(exc) from None
httpcore.RemoteProtocolError: illegal request line
```
</details>

Additionally when setting up an HTTP/2 server via hyper-h2 (`python hyper-server.py`), the same `RemoteProtocolError: illegal request line` error crops up when hitting it from httpcore or httpx, and the server raises an `h2.exceptions.ProtocolError: Invalid HTTP/2 preamble`. Httpcore is still going through an HTTP/1.1 connection in both cases, according to a little print I added in `SyncHTTPConnection.request()` (and according to the traceback):
```
http2: True
is_http11: True
is_http2: False
```

When hitting the hyper-h2 server with the gRPC client, the request is logged as expected:
```
<RequestReceived stream_id:1, headers:[(':scheme', 'http'), (':method', 'POST'), (':authority', '127.0.0.1:50051'), (':path', '/helloworld.Greeter/SayHello'), ('te', 'trailers'), ('content-type', 'application/grpc'), ('user-agent', 'grpc-python/1.36.1 grpc-c/15.0.0 (osx; chttp2)'), ('grpc-accept-encoding', 'identity,deflate,gzip'), ('accept-encoding', 'identity,gzip')]>
```
