https://fastapi.tiangolo.com/reference/middleware/
# Middleware[¶](#middleware "Permanent link")

There are several middlewares available provided by Starlette directly.

Read more about them in the [FastAPI docs for Middleware](https://fastapi.tiangolo.com/advanced/middleware/).

## fastapi.middleware.cors.CORSMiddleware [¶](#fastapi.middleware.cors.CORSMiddleware "Permanent link")

```python
CORSMiddleware(
    app,
    allow_origins=(),
    allow_methods=("GET",),
    allow_headers=(),
    allow_credentials=False,
    allow_origin_regex=None,
    allow_private_network=False,
    expose_headers=(),
    max_age=600,
)
```

Source code in `starlette/middleware/cors.py`

```python
def __init__(
    self,
    app: ASGIApp,
    allow_origins: Sequence[str] = (),
    allow_methods: Sequence[str] = ("GET",),
    allow_headers: Sequence[str] = (),
    allow_credentials: bool = False,
    allow_origin_regex: str | None = None,
    allow_private_network: bool = False,
    expose_headers: Sequence[str] = (),
    max_age: int = 600,
) -> None:
    if "*" in allow_methods:
        allow_methods = ALL_METHODS

    compiled_allow_origin_regex = None
    if allow_origin_regex is not None:
        compiled_allow_origin_regex = re.compile(allow_origin_regex)

    allow_all_origins = "*" in allow_origins
    allow_all_headers = "*" in allow_headers
    preflight_explicit_allow_origin = not allow_all_origins or allow_credentials

    simple_headers: dict[str, str] = {}
    if allow_all_origins:
        simple_headers["Access-Control-Allow-Origin"] = "*"
    if allow_credentials:
        simple_headers["Access-Control-Allow-Credentials"] = "true"
    if expose_headers:
        simple_headers["Access-Control-Expose-Headers"] = ", ".join(expose_headers)

    preflight_headers: dict[str, str] = {}
    if preflight_explicit_allow_origin:
        # The origin value will be set in preflight_response() if it is allowed.
        preflight_headers["Vary"] = "Origin"
    else:
        preflight_headers["Access-Control-Allow-Origin"] = "*"
    preflight_headers.update(
        {
            "Access-Control-Allow-Methods": ", ".join(allow_methods),
            "Access-Control-Max-Age": str(max_age),
        }
    )
    allow_headers = sorted(SAFELISTED_HEADERS | set(allow_headers))
    if allow_headers and not allow_all_headers:
        preflight_headers["Access-Control-Allow-Headers"] = ", ".join(allow_headers)
    if allow_credentials:
        preflight_headers["Access-Control-Allow-Credentials"] = "true"

    self.app = app
    self.allow_origins = allow_origins
    self.allow_methods = allow_methods
    self.allow_headers = [h.lower() for h in allow_headers]
    self.allow_all_origins = allow_all_origins
    self.allow_all_headers = allow_all_headers
    self.allow_credentials = allow_credentials
    self.preflight_explicit_allow_origin = preflight_explicit_allow_origin
    self.allow_origin_regex = compiled_allow_origin_regex
    self.allow_private_network = allow_private_network
    self.simple_headers = simple_headers
    self.preflight_headers = preflight_headers
```

### app `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.app "Permanent link")

```python
app = app
```

### allow\_origins `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.allow_origins "Permanent link")

```python
allow_origins = allow_origins
```

### allow\_methods `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.allow_methods "Permanent link")

```python
allow_methods = allow_methods
```

### allow\_headers `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.allow_headers "Permanent link")

```python
allow_headers = [(lower()) for h in allow_headers]
```

### allow\_all\_origins `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.allow_all_origins "Permanent link")

```python
allow_all_origins = allow_all_origins
```

### allow\_all\_headers `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.allow_all_headers "Permanent link")

```python
allow_all_headers = allow_all_headers
```

### allow\_credentials `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.allow_credentials "Permanent link")

```python
allow_credentials = allow_credentials
```

### preflight\_explicit\_allow\_origin `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.preflight_explicit_allow_origin "Permanent link")

```python
preflight_explicit_allow_origin = (
    preflight_explicit_allow_origin
)
```

### allow\_origin\_regex `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.allow_origin_regex "Permanent link")

```python
allow_origin_regex = compiled_allow_origin_regex
```

### allow\_private\_network `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.allow_private_network "Permanent link")

```python
allow_private_network = allow_private_network
```

### simple\_headers `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.simple_headers "Permanent link")

```python
simple_headers = simple_headers
```

### preflight\_headers `instance-attribute` [¶](#fastapi.middleware.cors.CORSMiddleware.preflight_headers "Permanent link")

```python
preflight_headers = preflight_headers
```

### is\_allowed\_origin [¶](#fastapi.middleware.cors.CORSMiddleware.is_allowed_origin "Permanent link")

```python
is_allowed_origin(origin)
```

Source code in `starlette/middleware/cors.py`

```python
def is_allowed_origin(self, origin: str) -> bool:
    if self.allow_all_origins:
        return True

    if self.allow_origin_regex is not None and self.allow_origin_regex.fullmatch(origin):
        return True

    return origin in self.allow_origins
```

### preflight\_response [¶](#fastapi.middleware.cors.CORSMiddleware.preflight_response "Permanent link")

```python
preflight_response(request_headers)
```

Source code in `starlette/middleware/cors.py`

```python
def preflight_response(self, request_headers: Headers) -> Response:
    requested_origin = request_headers["origin"]
    requested_method = request_headers["access-control-request-method"]
    requested_headers = request_headers.get("access-control-request-headers")
    requested_private_network = request_headers.get("access-control-request-private-network")

    headers = dict(self.preflight_headers)
    failures: list[str] = []

    if self.is_allowed_origin(origin=requested_origin):
        if self.preflight_explicit_allow_origin:
            # The "else" case is already accounted for in self.preflight_headers
            # and the value would be "*".
            headers["Access-Control-Allow-Origin"] = requested_origin
    else:
        failures.append("origin")

    if requested_method not in self.allow_methods:
        failures.append("method")

    # If we allow all headers, then we have to mirror back any requested
    # headers in the response.
    if self.allow_all_headers and requested_headers is not None:
        headers["Access-Control-Allow-Headers"] = requested_headers
    elif requested_headers is not None:
        for header in [h.lower() for h in requested_headers.split(",")]:
            if header.strip() not in self.allow_headers:
                failures.append("headers")
                break

    if requested_private_network is not None:
        if self.allow_private_network:
            headers["Access-Control-Allow-Private-Network"] = "true"
        else:
            failures.append("private-network")

    # We don't strictly need to use 400 responses here, since its up to
    # the browser to enforce the CORS policy, but its more informative
    # if we do.
    if failures:
        failure_text = "Disallowed CORS " + ", ".join(failures)
        return PlainTextResponse(failure_text, status_code=400, headers=headers)

    return PlainTextResponse("OK", status_code=200, headers=headers)
```

### simple\_response `async` [¶](#fastapi.middleware.cors.CORSMiddleware.simple_response "Permanent link")

```python
simple_response(scope, receive, send, request_headers)
```

Source code in `starlette/middleware/cors.py`

```python
async def simple_response(self, scope: Scope, receive: Receive, send: Send, request_headers: Headers) -> None:
    send = functools.partial(self.send, send=send, request_headers=request_headers)
    await self.app(scope, receive, send)
```

### send `async` [¶](#fastapi.middleware.cors.CORSMiddleware.send "Permanent link")

```python
send(message, send, request_headers)
```

Source code in `starlette/middleware/cors.py`

```python
async def send(self, message: Message, send: Send, request_headers: Headers) -> None:
    if message["type"] != "http.response.start":
        await send(message)
        return

    message.setdefault("headers", [])
    headers = MutableHeaders(scope=message)
    headers.update(self.simple_headers)
    origin = request_headers["Origin"]

    # If credentials are allowed, then we must respond with the specific origin instead of '*'.
    if self.allow_all_origins and self.allow_credentials:
        self.allow_explicit_origin(headers, origin)

    # If we only allow specific origins, then we have to mirror back the Origin header in the response.
    elif not self.allow_all_origins and self.is_allowed_origin(origin=origin):
        self.allow_explicit_origin(headers, origin)

    await send(message)
```

### allow\_explicit\_origin `staticmethod` [¶](#fastapi.middleware.cors.CORSMiddleware.allow_explicit_origin "Permanent link")

```python
allow_explicit_origin(headers, origin)
```

Source code in `starlette/middleware/cors.py`

```python
@staticmethod
def allow_explicit_origin(headers: MutableHeaders, origin: str) -> None:
    headers["Access-Control-Allow-Origin"] = origin
    headers.add_vary_header("Origin")
```

It can be imported from `fastapi`:

```python
from fastapi.middleware.cors import CORSMiddleware
```

## fastapi.middleware.gzip.GZipMiddleware [¶](#fastapi.middleware.gzip.GZipMiddleware "Permanent link")

```python
GZipMiddleware(app, minimum_size=500, compresslevel=9)
```

Source code in `starlette/middleware/gzip.py`

```python
def __init__(self, app: ASGIApp, minimum_size: int = 500, compresslevel: int = 9) -> None:
    self.app = app
    self.minimum_size = minimum_size
    self.compresslevel = compresslevel
```

### app `instance-attribute` [¶](#fastapi.middleware.gzip.GZipMiddleware.app "Permanent link")

```python
app = app
```

### minimum\_size `instance-attribute` [¶](#fastapi.middleware.gzip.GZipMiddleware.minimum_size "Permanent link")

```python
minimum_size = minimum_size
```

### compresslevel `instance-attribute` [¶](#fastapi.middleware.gzip.GZipMiddleware.compresslevel "Permanent link")

```python
compresslevel = compresslevel
```

It can be imported from `fastapi`:

```python
from fastapi.middleware.gzip import GZipMiddleware
```

## fastapi.middleware.httpsredirect.HTTPSRedirectMiddleware [¶](#fastapi.middleware.httpsredirect.HTTPSRedirectMiddleware "Permanent link")

```python
HTTPSRedirectMiddleware(app)
```

Source code in `starlette/middleware/httpsredirect.py`

```python
def __init__(self, app: ASGIApp) -> None:
    self.app = app
```

### app `instance-attribute` [¶](#fastapi.middleware.httpsredirect.HTTPSRedirectMiddleware.app "Permanent link")

```python
app = app
```

It can be imported from `fastapi`:

```python
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
```

## fastapi.middleware.trustedhost.TrustedHostMiddleware [¶](#fastapi.middleware.trustedhost.TrustedHostMiddleware "Permanent link")

```python
TrustedHostMiddleware(
    app, allowed_hosts=None, www_redirect=True
)
```

Source code in `starlette/middleware/trustedhost.py`

```python
def __init__(
    self,
    app: ASGIApp,
    allowed_hosts: Sequence[str] | None = None,
    www_redirect: bool = True,
) -> None:
    if allowed_hosts is None:
        allowed_hosts = ["*"]

    for pattern in allowed_hosts:
        assert "*" not in pattern[1:], ENFORCE_DOMAIN_WILDCARD
        if pattern.startswith("*") and pattern != "*":
            assert pattern.startswith("*."), ENFORCE_DOMAIN_WILDCARD
    self.app = app
    self.allowed_hosts = list(allowed_hosts)
    self.allow_any = "*" in allowed_hosts
    self.www_redirect = www_redirect
```

### app `instance-attribute` [¶](#fastapi.middleware.trustedhost.TrustedHostMiddleware.app "Permanent link")

```python
app = app
```

### allowed\_hosts `instance-attribute` [¶](#fastapi.middleware.trustedhost.TrustedHostMiddleware.allowed_hosts "Permanent link")

```python
allowed_hosts = list(allowed_hosts)
```

### allow\_any `instance-attribute` [¶](#fastapi.middleware.trustedhost.TrustedHostMiddleware.allow_any "Permanent link")

```python
allow_any = '*' in allowed_hosts
```

### www\_redirect `instance-attribute` [¶](#fastapi.middleware.trustedhost.TrustedHostMiddleware.www_redirect "Permanent link")

```python
www_redirect = www_redirect
```

It can be imported from `fastapi`:

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware
```
