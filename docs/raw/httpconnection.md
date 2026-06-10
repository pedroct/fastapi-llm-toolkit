https://fastapi.tiangolo.com/reference/httpconnection/
# `HTTPConnection` class[¶](#httpconnection-class "Permanent link")

When you want to define dependencies that should be compatible with both HTTP and WebSockets, you can define a parameter that takes an `HTTPConnection` instead of a `Request` or a `WebSocket`.

You can import it from `fastapi.requests`:

```python
from fastapi.requests import HTTPConnection
```

## fastapi.requests.HTTPConnection [¶](#fastapi.requests.HTTPConnection "Permanent link")

```python
HTTPConnection(scope, receive=None)
```

Bases: `Mapping[str, Any]`, `Generic[StateT]`

A base class for incoming HTTP connections, that is used to provide
any functionality that is common to both `Request` and `WebSocket`.

Source code in `starlette/requests.py`

```python
def __init__(self, scope: Scope, receive: Receive | None = None) -> None:
    assert scope["type"] in ("http", "websocket")
    self.scope = scope
```

### scope `instance-attribute` [¶](#fastapi.requests.HTTPConnection.scope "Permanent link")

```python
scope = scope
```

### app `property` [¶](#fastapi.requests.HTTPConnection.app "Permanent link")

```python
app
```

### url `property` [¶](#fastapi.requests.HTTPConnection.url "Permanent link")

```python
url
```

### base\_url `property` [¶](#fastapi.requests.HTTPConnection.base_url "Permanent link")

```python
base_url
```

### headers `property` [¶](#fastapi.requests.HTTPConnection.headers "Permanent link")

```python
headers
```

### query\_params `property` [¶](#fastapi.requests.HTTPConnection.query_params "Permanent link")

```python
query_params
```

### path\_params `property` [¶](#fastapi.requests.HTTPConnection.path_params "Permanent link")

```python
path_params
```

### cookies `property` [¶](#fastapi.requests.HTTPConnection.cookies "Permanent link")

```python
cookies
```

### client `property` [¶](#fastapi.requests.HTTPConnection.client "Permanent link")

```python
client
```

### session `property` [¶](#fastapi.requests.HTTPConnection.session "Permanent link")

```python
session
```

### auth `property` [¶](#fastapi.requests.HTTPConnection.auth "Permanent link")

```python
auth
```

### user `property` [¶](#fastapi.requests.HTTPConnection.user "Permanent link")

```python
user
```

### state `property` [¶](#fastapi.requests.HTTPConnection.state "Permanent link")

```python
state
```

### url\_for [¶](#fastapi.requests.HTTPConnection.url_for "Permanent link")

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
