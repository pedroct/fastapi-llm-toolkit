https://fastapi.tiangolo.com/reference/uploadfile/
# `UploadFile` class[¶](#uploadfile-class "Permanent link")

You can define *path operation function* parameters to be of the type `UploadFile` to receive files from the request.

You can import it directly from `fastapi`:

```python
from fastapi import UploadFile
```

## fastapi.UploadFile [¶](#fastapi.UploadFile "Permanent link")

```python
UploadFile(file, *, size=None, filename=None, headers=None)
```

Bases: `UploadFile`

A file uploaded in a request.

Define it as a *path operation function* (or dependency) parameter.

If you are using a regular `def` function, you can use the `upload_file.file`
attribute to access the raw standard Python file (blocking, not async), useful and
needed for non-async code.

Read more about it in the
[FastAPI docs for Request Files](https://fastapi.tiangolo.com/tutorial/request-files/).

#### Example[¶](#fastapi.UploadFile--example "Permanent link")

```python
from typing import Annotated

from fastapi import FastAPI, File, UploadFile

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}
```

Source code in `starlette/datastructures.py`

```python
def __init__(
    self,
    file: BinaryIO,
    *,
    size: int | None = None,
    filename: str | None = None,
    headers: Headers | None = None,
) -> None:
    self.filename = filename
    self.file = file
    self.size = size
    self.headers = headers or Headers()

    # Capture max size from SpooledTemporaryFile if one is provided. This slightly speeds up future checks.
    # Note 0 means unlimited mirroring SpooledTemporaryFile's __init__
    self._max_mem_size = getattr(self.file, "_max_size", 0)
```

### file `instance-attribute` [¶](#fastapi.UploadFile.file "Permanent link")

```python
file
```

The standard Python file object (non-async).

### filename `instance-attribute` [¶](#fastapi.UploadFile.filename "Permanent link")

```python
filename
```

The original file name.

### size `instance-attribute` [¶](#fastapi.UploadFile.size "Permanent link")

```python
size
```

The size of the file in bytes.

### headers `instance-attribute` [¶](#fastapi.UploadFile.headers "Permanent link")

```python
headers
```

The headers of the request.

### content\_type `instance-attribute` [¶](#fastapi.UploadFile.content_type "Permanent link")

```python
content_type
```

The content type of the request, from the headers.

### read `async` [¶](#fastapi.UploadFile.read "Permanent link")

```python
read(size=-1)
```

Read some bytes from the file.

To be awaitable, compatible with async, this is run in threadpool.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `size` | The number of bytes to read from the file.  **TYPE:** `int`  **DEFAULT:** `-1` |

Source code in `fastapi/datastructures.py`

```python
async def read(
    self,
    size: Annotated[
        int,
        Doc(
            """
            The number of bytes to read from the file.
            """
        ),
    ] = -1,
) -> bytes:
    """
    Read some bytes from the file.

    To be awaitable, compatible with async, this is run in threadpool.
    """
    return await super().read(size)
```

### write `async` [¶](#fastapi.UploadFile.write "Permanent link")

```python
write(data)
```

Write some bytes to the file.

You normally wouldn't use this from a file you read in a request.

To be awaitable, compatible with async, this is run in threadpool.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `data` | The bytes to write to the file.  **TYPE:** `bytes` |

Source code in `fastapi/datastructures.py`

```python
async def write(
    self,
    data: Annotated[
        bytes,
        Doc(
            """
            The bytes to write to the file.
            """
        ),
    ],
) -> None:
    """
    Write some bytes to the file.

    You normally wouldn't use this from a file you read in a request.

    To be awaitable, compatible with async, this is run in threadpool.
    """
    return await super().write(data)
```

### seek `async` [¶](#fastapi.UploadFile.seek "Permanent link")

```python
seek(offset)
```

Move to a position in the file.

Any next read or write will be done from that position.

To be awaitable, compatible with async, this is run in threadpool.

| PARAMETER | DESCRIPTION |
| --- | --- |
| `offset` | The position in bytes to seek to in the file.  **TYPE:** `int` |

Source code in `fastapi/datastructures.py`

```python
async def seek(
    self,
    offset: Annotated[
        int,
        Doc(
            """
            The position in bytes to seek to in the file.
            """
        ),
    ],
) -> None:
    """
    Move to a position in the file.

    Any next read or write will be done from that position.

    To be awaitable, compatible with async, this is run in threadpool.
    """
    return await super().seek(offset)
```

### close `async` [¶](#fastapi.UploadFile.close "Permanent link")

```python
close()
```

Close the file.

To be awaitable, compatible with async, this is run in threadpool.

Source code in `fastapi/datastructures.py`

```python
async def close(self) -> None:
    """
    Close the file.

    To be awaitable, compatible with async, this is run in threadpool.
    """
    return await super().close()
```
