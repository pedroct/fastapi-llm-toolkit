https://fastapi.tiangolo.com/reference/testclient/
# Test Client - `TestClient`[¶](#test-client-testclient "Permanent link")

You can use the `TestClient` class to test FastAPI applications without creating an actual HTTP and socket connection, just communicating directly with the FastAPI code.

Read more about it in the [FastAPI docs for Testing](https://fastapi.tiangolo.com/tutorial/testing/).

You can import it directly from `fastapi.testclient`:

```python
from fastapi.testclient import TestClient
```

## fastapi.testclient.TestClient [¶](#fastapi.testclient.TestClient "Permanent link")

```python
TestClient(
    app,
    base_url="http://testserver",
    raise_server_exceptions=True,
    root_path="",
    backend="asyncio",
    backend_options=None,
    cookies=None,
    headers=None,
    follow_redirects=True,
    client=("testclient", 50000),
)
```

Bases: `Client`

Source code in `starlette/testclient.py`

```python
def __init__(
    self,
    app: ASGIApp,
    base_url: str = "http://testserver",
    raise_server_exceptions: bool = True,
    root_path: str = "",
    backend: Literal["asyncio", "trio"] = "asyncio",
    backend_options: dict[str, Any] | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    headers: dict[str, str] | None = None,
    follow_redirects: bool = True,
    client: tuple[str, int] = ("testclient", 50000),
) -> None:
    self.async_backend = _AsyncBackend(backend=backend, backend_options=backend_options or {})
    if _is_asgi3(app):
        asgi_app = app
    else:
        app = cast(ASGI2App, app)  # type: ignore[assignment]
        asgi_app = _WrapASGI2(app)  # type: ignore[arg-type]
    self.app = asgi_app
    self.app_state: dict[str, Any] = {}
    transport = _TestClientTransport(
        self.app,
        portal_factory=self._portal_factory,
        raise_server_exceptions=raise_server_exceptions,
        root_path=root_path,
        app_state=self.app_state,
        client=client,
    )
    if headers is None:
        headers = {}
    headers.setdefault("user-agent", "testclient")
    super().__init__(
        base_url=base_url,
        headers=headers,
        transport=transport,
        follow_redirects=follow_redirects,
        cookies=cookies,
    )
```

### headers `property` `writable` [¶](#fastapi.testclient.TestClient.headers "Permanent link")

```python
headers
```

HTTP headers to include when sending requests.

### follow\_redirects `instance-attribute` [¶](#fastapi.testclient.TestClient.follow_redirects "Permanent link")

```python
follow_redirects = follow_redirects
```

### max\_redirects `instance-attribute` [¶](#fastapi.testclient.TestClient.max_redirects "Permanent link")

```python
max_redirects = max_redirects
```

### is\_closed `property` [¶](#fastapi.testclient.TestClient.is_closed "Permanent link")

```python
is_closed
```

Check if the client being closed

### trust\_env `property` [¶](#fastapi.testclient.TestClient.trust_env "Permanent link")

```python
trust_env
```

### timeout `property` `writable` [¶](#fastapi.testclient.TestClient.timeout "Permanent link")

```python
timeout
```

### event\_hooks `property` `writable` [¶](#fastapi.testclient.TestClient.event_hooks "Permanent link")

```python
event_hooks
```

### auth `property` `writable` [¶](#fastapi.testclient.TestClient.auth "Permanent link")

```python
auth
```

Authentication class used when none is passed at the request-level.

See also [Authentication](/quickstart/#authentication).

### base\_url `property` `writable` [¶](#fastapi.testclient.TestClient.base_url "Permanent link")

```python
base_url
```

Base URL to use when sending requests with relative URLs.

### cookies `property` `writable` [¶](#fastapi.testclient.TestClient.cookies "Permanent link")

```python
cookies
```

Cookie values to include when sending requests.

### params `property` `writable` [¶](#fastapi.testclient.TestClient.params "Permanent link")

```python
params
```

Query parameters to include in the URL when sending requests.

### task `instance-attribute` [¶](#fastapi.testclient.TestClient.task "Permanent link")

```python
task
```

### portal `class-attribute` `instance-attribute` [¶](#fastapi.testclient.TestClient.portal "Permanent link")

```python
portal = None
```

### async\_backend `instance-attribute` [¶](#fastapi.testclient.TestClient.async_backend "Permanent link")

```python
async_backend = _AsyncBackend(
    backend=backend, backend_options=backend_options or {}
)
```

### app `instance-attribute` [¶](#fastapi.testclient.TestClient.app "Permanent link")

```python
app = asgi_app
```

### app\_state `instance-attribute` [¶](#fastapi.testclient.TestClient.app_state "Permanent link")

```python
app_state = {}
```

### build\_request [¶](#fastapi.testclient.TestClient.build_request "Permanent link")

```python
build_request(
    method,
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Build and return a request instance.

* The `params`, `headers` and `cookies` arguments
  are merged with any values set on the client.
* The `url` argument is merged with any `base_url` set on the client.

See also: [Request instances](/advanced/clients/#request-instances)

Source code in `httpx/_client.py`

```python
def build_request(
    self,
    method: str,
    url: URL | str,
    *,
    content: RequestContent | None = None,
    data: RequestData | None = None,
    files: RequestFiles | None = None,
    json: typing.Any | None = None,
    params: QueryParamTypes | None = None,
    headers: HeaderTypes | None = None,
    cookies: CookieTypes | None = None,
    timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
    extensions: RequestExtensions | None = None,
) -> Request:
    """
    Build and return a request instance.

    * The `params`, `headers` and `cookies` arguments
    are merged with any values set on the client.
    * The `url` argument is merged with any `base_url` set on the client.

    See also: [Request instances][0]

    [0]: /advanced/clients/#request-instances
    """
    url = self._merge_url(url)
    headers = self._merge_headers(headers)
    cookies = self._merge_cookies(cookies)
    params = self._merge_queryparams(params)
    extensions = {} if extensions is None else extensions
    if "timeout" not in extensions:
        timeout = (
            self.timeout
            if isinstance(timeout, UseClientDefault)
            else Timeout(timeout)
        )
        extensions = dict(**extensions, timeout=timeout.as_dict())
    return Request(
        method,
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        extensions=extensions,
    )
```

### stream [¶](#fastapi.testclient.TestClient.stream "Permanent link")

```python
stream(
    method,
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Alternative to `httpx.request()` that streams the response body
instead of loading it into memory at once.

**Parameters**: See `httpx.request`.

See also: [Streaming Responses](/quickstart#streaming-responses)

Source code in `httpx/_client.py`

```python
@contextmanager
def stream(
    self,
    method: str,
    url: URL | str,
    *,
    content: RequestContent | None = None,
    data: RequestData | None = None,
    files: RequestFiles | None = None,
    json: typing.Any | None = None,
    params: QueryParamTypes | None = None,
    headers: HeaderTypes | None = None,
    cookies: CookieTypes | None = None,
    auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
    follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
    timeout: TimeoutTypes | UseClientDefault = USE_CLIENT_DEFAULT,
    extensions: RequestExtensions | None = None,
) -> typing.Iterator[Response]:
    """
    Alternative to `httpx.request()` that streams the response body
    instead of loading it into memory at once.

    **Parameters**: See `httpx.request`.

    See also: [Streaming Responses][0]

    [0]: /quickstart#streaming-responses
    """
    request = self.build_request(
        method=method,
        url=url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        timeout=timeout,
        extensions=extensions,
    )
    response = self.send(
        request=request,
        auth=auth,
        follow_redirects=follow_redirects,
        stream=True,
    )
    try:
        yield response
    finally:
        response.close()
```

### send [¶](#fastapi.testclient.TestClient.send "Permanent link")

```python
send(
    request,
    *,
    stream=False,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT
)
```

Send a request.

The request is sent as-is, unmodified.

Typically you'll want to build one with `Client.build_request()`
so that any client-level configuration is merged into the request,
but passing an explicit `httpx.Request()` is supported as well.

See also: [Request instances](/advanced/clients/#request-instances)

Source code in `httpx/_client.py`

```python
def send(
    self,
    request: Request,
    *,
    stream: bool = False,
    auth: AuthTypes | UseClientDefault | None = USE_CLIENT_DEFAULT,
    follow_redirects: bool | UseClientDefault = USE_CLIENT_DEFAULT,
) -> Response:
    """
    Send a request.

    The request is sent as-is, unmodified.

    Typically you'll want to build one with `Client.build_request()`
    so that any client-level configuration is merged into the request,
    but passing an explicit `httpx.Request()` is supported as well.

    See also: [Request instances][0]

    [0]: /advanced/clients/#request-instances
    """
    if self._state == ClientState.CLOSED:
        raise RuntimeError("Cannot send a request, as the client has been closed.")

    self._state = ClientState.OPENED
    follow_redirects = (
        self.follow_redirects
        if isinstance(follow_redirects, UseClientDefault)
        else follow_redirects
    )

    self._set_timeout(request)

    auth = self._build_request_auth(request, auth)

    response = self._send_handling_auth(
        request,
        auth=auth,
        follow_redirects=follow_redirects,
        history=[],
    )
    try:
        if not stream:
            response.read()

        return response

    except BaseException as exc:
        response.close()
        raise exc
```

### close [¶](#fastapi.testclient.TestClient.close "Permanent link")

```python
close()
```

Close transport and proxies.

Source code in `httpx/_client.py`

```python
def close(self) -> None:
    """
    Close transport and proxies.
    """
    if self._state != ClientState.CLOSED:
        self._state = ClientState.CLOSED

        self._transport.close()
        for transport in self._mounts.values():
            if transport is not None:
                transport.close()
```

### request [¶](#fastapi.testclient.TestClient.request "Permanent link")

```python
request(
    method,
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Source code in `starlette/testclient.py`

```python
def request(  # type: ignore[override]
    self,
    method: str,
    url: httpx._types.URLTypes,
    *,
    content: httpx._types.RequestContent | None = None,
    data: _RequestData | None = None,
    files: httpx._types.RequestFiles | None = None,
    json: Any = None,
    params: httpx._types.QueryParamTypes | None = None,
    headers: httpx._types.HeaderTypes | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    extensions: dict[str, Any] | None = None,
) -> httpx.Response:
    if timeout is not httpx.USE_CLIENT_DEFAULT:
        warnings.warn(
            "You should not use the 'timeout' argument with the TestClient. "
            "See https://github.com/Kludex/starlette/issues/1108 for more information.",
            DeprecationWarning,
        )
    url = self._merge_url(url)
    return super().request(
        method,
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        follow_redirects=follow_redirects,
        timeout=timeout,
        extensions=extensions,
    )
```

### get [¶](#fastapi.testclient.TestClient.get "Permanent link")

```python
get(
    url,
    *,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Source code in `starlette/testclient.py`

```python
def get(  # type: ignore[override]
    self,
    url: httpx._types.URLTypes,
    *,
    params: httpx._types.QueryParamTypes | None = None,
    headers: httpx._types.HeaderTypes | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    extensions: dict[str, Any] | None = None,
) -> httpx.Response:
    return super().get(
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        follow_redirects=follow_redirects,
        timeout=timeout,
        extensions=extensions,
    )
```

### options [¶](#fastapi.testclient.TestClient.options "Permanent link")

```python
options(
    url,
    *,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Source code in `starlette/testclient.py`

```python
def options(  # type: ignore[override]
    self,
    url: httpx._types.URLTypes,
    *,
    params: httpx._types.QueryParamTypes | None = None,
    headers: httpx._types.HeaderTypes | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    extensions: dict[str, Any] | None = None,
) -> httpx.Response:
    return super().options(
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        follow_redirects=follow_redirects,
        timeout=timeout,
        extensions=extensions,
    )
```

### head [¶](#fastapi.testclient.TestClient.head "Permanent link")

```python
head(
    url,
    *,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Source code in `starlette/testclient.py`

```python
def head(  # type: ignore[override]
    self,
    url: httpx._types.URLTypes,
    *,
    params: httpx._types.QueryParamTypes | None = None,
    headers: httpx._types.HeaderTypes | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    extensions: dict[str, Any] | None = None,
) -> httpx.Response:
    return super().head(
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        follow_redirects=follow_redirects,
        timeout=timeout,
        extensions=extensions,
    )
```

### post [¶](#fastapi.testclient.TestClient.post "Permanent link")

```python
post(
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Source code in `starlette/testclient.py`

```python
def post(  # type: ignore[override]
    self,
    url: httpx._types.URLTypes,
    *,
    content: httpx._types.RequestContent | None = None,
    data: _RequestData | None = None,
    files: httpx._types.RequestFiles | None = None,
    json: Any = None,
    params: httpx._types.QueryParamTypes | None = None,
    headers: httpx._types.HeaderTypes | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    extensions: dict[str, Any] | None = None,
) -> httpx.Response:
    return super().post(
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        follow_redirects=follow_redirects,
        timeout=timeout,
        extensions=extensions,
    )
```

### put [¶](#fastapi.testclient.TestClient.put "Permanent link")

```python
put(
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Source code in `starlette/testclient.py`

```python
def put(  # type: ignore[override]
    self,
    url: httpx._types.URLTypes,
    *,
    content: httpx._types.RequestContent | None = None,
    data: _RequestData | None = None,
    files: httpx._types.RequestFiles | None = None,
    json: Any = None,
    params: httpx._types.QueryParamTypes | None = None,
    headers: httpx._types.HeaderTypes | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    extensions: dict[str, Any] | None = None,
) -> httpx.Response:
    return super().put(
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        follow_redirects=follow_redirects,
        timeout=timeout,
        extensions=extensions,
    )
```

### patch [¶](#fastapi.testclient.TestClient.patch "Permanent link")

```python
patch(
    url,
    *,
    content=None,
    data=None,
    files=None,
    json=None,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Source code in `starlette/testclient.py`

```python
def patch(  # type: ignore[override]
    self,
    url: httpx._types.URLTypes,
    *,
    content: httpx._types.RequestContent | None = None,
    data: _RequestData | None = None,
    files: httpx._types.RequestFiles | None = None,
    json: Any = None,
    params: httpx._types.QueryParamTypes | None = None,
    headers: httpx._types.HeaderTypes | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    extensions: dict[str, Any] | None = None,
) -> httpx.Response:
    return super().patch(
        url,
        content=content,
        data=data,
        files=files,
        json=json,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        follow_redirects=follow_redirects,
        timeout=timeout,
        extensions=extensions,
    )
```

### delete [¶](#fastapi.testclient.TestClient.delete "Permanent link")

```python
delete(
    url,
    *,
    params=None,
    headers=None,
    cookies=None,
    auth=USE_CLIENT_DEFAULT,
    follow_redirects=USE_CLIENT_DEFAULT,
    timeout=USE_CLIENT_DEFAULT,
    extensions=None
)
```

Source code in `starlette/testclient.py`

```python
def delete(  # type: ignore[override]
    self,
    url: httpx._types.URLTypes,
    *,
    params: httpx._types.QueryParamTypes | None = None,
    headers: httpx._types.HeaderTypes | None = None,
    cookies: httpx._types.CookieTypes | None = None,
    auth: httpx._types.AuthTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    follow_redirects: bool | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    timeout: httpx._types.TimeoutTypes | httpx._client.UseClientDefault = httpx._client.USE_CLIENT_DEFAULT,
    extensions: dict[str, Any] | None = None,
) -> httpx.Response:
    return super().delete(
        url,
        params=params,
        headers=headers,
        cookies=cookies,
        auth=auth,
        follow_redirects=follow_redirects,
        timeout=timeout,
        extensions=extensions,
    )
```

### websocket\_connect [¶](#fastapi.testclient.TestClient.websocket_connect "Permanent link")

```python
websocket_connect(url, subprotocols=None, **kwargs)
```

Source code in `starlette/testclient.py`

```python
def websocket_connect(
    self,
    url: str,
    subprotocols: Sequence[str] | None = None,
    **kwargs: Any,
) -> WebSocketTestSession:
    url = urljoin("ws://testserver", url)
    headers = kwargs.get("headers", {})
    headers.setdefault("connection", "upgrade")
    headers.setdefault("sec-websocket-key", "testserver==")
    headers.setdefault("sec-websocket-version", "13")
    if subprotocols is not None:
        headers.setdefault("sec-websocket-protocol", ", ".join(subprotocols))
    kwargs["headers"] = headers
    try:
        super().request("GET", url, **kwargs)
    except _Upgrade as exc:
        session = exc.session
    else:
        raise RuntimeError("Expected WebSocket upgrade")  # pragma: no cover

    return session
```

### lifespan `async` [¶](#fastapi.testclient.TestClient.lifespan "Permanent link")

```python
lifespan()
```

Source code in `starlette/testclient.py`

```python
async def lifespan(self) -> None:
    scope = {"type": "lifespan", "state": self.app_state}
    try:
        await self.app(scope, self.stream_receive.receive, self.stream_send.send)
    finally:
        await self.stream_send.send(None)
```

### wait\_startup `async` [¶](#fastapi.testclient.TestClient.wait_startup "Permanent link")

```python
wait_startup()
```

Source code in `starlette/testclient.py`

```python
async def wait_startup(self) -> None:
    await self.stream_receive.send({"type": "lifespan.startup"})

    async def receive() -> Any:
        message = await self.stream_send.receive()
        if message is None:
            self.task.result()
        return message

    message = await receive()
    assert message["type"] in (
        "lifespan.startup.complete",
        "lifespan.startup.failed",
    )
    if message["type"] == "lifespan.startup.failed":
        await receive()
```

### wait\_shutdown `async` [¶](#fastapi.testclient.TestClient.wait_shutdown "Permanent link")

```python
wait_shutdown()
```

Source code in `starlette/testclient.py`

```python
async def wait_shutdown(self) -> None:
    async def receive() -> Any:
        message = await self.stream_send.receive()
        if message is None:
            self.task.result()
        return message

    await self.stream_receive.send({"type": "lifespan.shutdown"})
    message = await receive()
    assert message["type"] in (
        "lifespan.shutdown.complete",
        "lifespan.shutdown.failed",
    )
    if message["type"] == "lifespan.shutdown.failed":
        await receive()
```
