https://fastapi.tiangolo.com/reference/request/
# `Request` class[¶](#request-class "Permanent link")

You can declare a parameter in a *path operation function* or dependency to be of type `Request` and then you can access the raw request object directly, without any validation, etc.

Read more about it in the [FastAPI docs about using Request directly](https://fastapi.tiangolo.com/advanced/using-request-directly/)

You can import it directly from `fastapi`:

```python
from fastapi import Request
```

Tip

When you want to define dependencies that should be compatible with both HTTP and WebSockets, you can define a parameter that takes an `HTTPConnection` instead of a `Request` or a `WebSocket`.

## fastapi.Request [¶](#fastapi.Request "Permanent link")

```python
Request(scope, receive=empty_receive, send=empty_send)
```

Bases: `HTTPConnection[StateT]`

Source code in `starlette/requests.py`

```python
def __init__(self, scope: Scope, receive: Receive = empty_receive, send: Send = empty_send):
    super().__init__(scope)
    assert scope["type"] == "http"
    self._receive = receive
    self._send = send
    self._stream_consumed = False
    self._is_disconnected = False
    self._form = None
```

### scope `instance-attribute` [¶](#fastapi.Request.scope "Permanent link")

```python
scope = scope
```

### app `property` [¶](#fastapi.Request.app "Permanent link")

```python
app
```

### url `property` [¶](#fastapi.Request.url "Permanent link")

```python
url
```

### base\_url `property` [¶](#fastapi.Request.base_url "Permanent link")

```python
base_url
```

### headers `property` [¶](#fastapi.Request.headers "Permanent link")

```python
headers
```

### query\_params `property` [¶](#fastapi.Request.query_params "Permanent link")

```python
query_params
```

### path\_params `property` [¶](#fastapi.Request.path_params "Permanent link")

```python
path_params
```

### cookies `property` [¶](#fastapi.Request.cookies "Permanent link")

```python
cookies
```

### client `property` [¶](#fastapi.Request.client "Permanent link")

```python
client
```

### session `property` [¶](#fastapi.Request.session "Permanent link")

```python
session
```

### auth `property` [¶](#fastapi.Request.auth "Permanent link")

```python
auth
```

### user `property` [¶](#fastapi.Request.user "Permanent link")

```python
user
```

### state `property` [¶](#fastapi.Request.state "Permanent link")

```python
state
```

### method `property` [¶](#fastapi.Request.method "Permanent link")

```python
method
```

### receive `property` [¶](#fastapi.Request.receive "Permanent link")

```python
receive
```

### url\_for [¶](#fastapi.Request.url_for "Permanent link")

```python
url_for(name, /, **path_params)
```

Source code in `starlette/requests.py`

```python
def url_for(self, name: str, /, **path_params: Any) -> URL:
    url_path_provider: Router | Starlette | None = self.scope.get("router") or self.scope.get("app")
    if url_path_provider is None:
        raise RuntimeError("The `url_for` method can only be used inside a Starlette application or with a router.")
    url_path = url_path_provider.url_path_for(name, **path_params)
    return url_path.make_absolute_url(base_url=self.base_url)
```

### stream `async` [¶](#fastapi.Request.stream "Permanent link")

```python
stream()
```

Source code in `starlette/requests.py`

```python
async def stream(self) -> AsyncGenerator[bytes, None]:
    if hasattr(self, "_body"):
        yield self._body
        yield b""
        return
    if self._stream_consumed:
        raise RuntimeError("Stream consumed")
    while not self._stream_consumed:
        message = await self._receive()
        if message["type"] == "http.request":
            body = message.get("body", b"")
            if not message.get("more_body", False):
                self._stream_consumed = True
            if body:
                yield body
        elif message["type"] == "http.disconnect":  # pragma: no branch
            self._is_disconnected = True
            raise ClientDisconnect()
    yield b""
```

### body `async` [¶](#fastapi.Request.body "Permanent link")

```python
body()
```

Source code in `starlette/requests.py`

```python
async def body(self) -> bytes:
    if not hasattr(self, "_body"):
        chunks: list[bytes] = []
        async for chunk in self.stream():
            chunks.append(chunk)
        self._body = b"".join(chunks)
    return self._body
```

### json `async` [¶](#fastapi.Request.json "Permanent link")

```python
json()
```

Source code in `starlette/requests.py`

```python
async def json(self) -> Any:
    if not hasattr(self, "_json"):  # pragma: no branch
        body = await self.body()
        self._json = json.loads(body)
    return self._json
```

### form [¶](#fastapi.Request.form "Permanent link")

```python
form(
    *,
    max_files=1000,
    max_fields=1000,
    max_part_size=1024 * 1024
)
```

Source code in `starlette/requests.py`

```python
def form(
    self,
    *,
    max_files: int | float = 1000,
    max_fields: int | float = 1000,
    max_part_size: int = 1024 * 1024,
) -> AwaitableOrContextManager[FormData]:
    return AwaitableOrContextManagerWrapper(
        self._get_form(max_files=max_files, max_fields=max_fields, max_part_size=max_part_size)
    )
```

### close `async` [¶](#fastapi.Request.close "Permanent link")

```python
close()
```

Source code in `starlette/requests.py`

```python
async def close(self) -> None:
    if self._form is not None:  # pragma: no branch
        await self._form.close()
```

### is\_disconnected `async` [¶](#fastapi.Request.is_disconnected "Permanent link")

```python
is_disconnected()
```

Source code in `starlette/requests.py`

```python
async def is_disconnected(self) -> bool:
    if not self._is_disconnected:
        message: Message = {}

        # If message isn't immediately available, move on
        with anyio.CancelScope() as cs:
            cs.cancel()
            message = await self._receive()

        if message.get("type") == "http.disconnect":
            self._is_disconnected = True

    return self._is_disconnected
```

### send\_push\_promise `async` [¶](#fastapi.Request.send_push_promise "Permanent link")

```python
send_push_promise(path)
```

Source code in `starlette/requests.py`

```python
async def send_push_promise(self, path: str) -> None:
    if "http.response.push" in self.scope.get("extensions", {}):
        raw_headers: list[tuple[bytes, bytes]] = []
        for name in SERVER_PUSH_HEADERS_TO_COPY:
            for value in self.headers.getlist(name):
                raw_headers.append((name.encode("latin-1"), value.encode("latin-1")))
        await self._send({"type": "http.response.push", "path": path, "headers": raw_headers})
```
