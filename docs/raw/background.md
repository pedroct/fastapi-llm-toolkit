https://fastapi.tiangolo.com/reference/background/
# Background Tasks - `BackgroundTasks`[¶](#background-tasks-backgroundtasks "Permanent link")

You can declare a parameter in a *path operation function* or dependency function with the type `BackgroundTasks`, and then you can use it to schedule the execution of background tasks after the response is sent.

You can import it directly from `fastapi`:

```python
from fastapi import BackgroundTasks
```

## fastapi.BackgroundTasks [¶](#fastapi.BackgroundTasks "Permanent link")

```python
BackgroundTasks(tasks=None)
```

Bases: `BackgroundTasks`

A collection of background tasks that will be called after a response has been
sent to the client.

Read more about it in the
[FastAPI docs for Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).

#### Example[¶](#fastapi.BackgroundTasks--example "Permanent link")

```python
from fastapi import BackgroundTasks, FastAPI

app = FastAPI()


def write_notification(email: str, message=""):
    with open("log.txt", mode="w") as email_file:
        content = f"notification for {email}: {message}"
        email_file.write(content)


@app.post("/send-notification/{email}")
async def send_notification(email: str, background_tasks: BackgroundTasks):
    background_tasks.add_task(write_notification, email, message="some notification")
    return {"message": "Notification sent in the background"}
```

Source code in `starlette/background.py`

```python
def __init__(self, tasks: Sequence[BackgroundTask] | None = None):
    self.tasks = list(tasks) if tasks else []
```

### func `instance-attribute` [¶](#fastapi.BackgroundTasks.func "Permanent link")

```python
func = func
```

### args `instance-attribute` [¶](#fastapi.BackgroundTasks.args "Permanent link")

```python
args = args
```

### kwargs `instance-attribute` [¶](#fastapi.BackgroundTasks.kwargs "Permanent link")

```python
kwargs = kwargs
```

### is\_async `instance-attribute` [¶](#fastapi.BackgroundTasks.is_async "Permanent link")

```python
is_async = is_async_callable(func)
```

### tasks `instance-attribute` [¶](#fastapi.BackgroundTasks.tasks "Permanent link")

```python
tasks = list(tasks) if tasks else []
```

### add\_task [¶](#fastapi.BackgroundTasks.add_task "Permanent link")

```python
add_task(func, *args, **kwargs)
```

Add a function to be called in the background after the response is sent.

Read more about it in the
[FastAPI docs for Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).

| PARAMETER | DESCRIPTION |
| --- | --- |
| `func` | The function to call after the response is sent.  It can be a regular `def` function or an `async def` function.  **TYPE:** `Callable[P, Any]` |

Source code in `fastapi/background.py`

```python
def add_task(
    self,
    func: Annotated[
        Callable[P, Any],
        Doc(
            """
            The function to call after the response is sent.

            It can be a regular `def` function or an `async def` function.
            """
        ),
    ],
    *args: P.args,
    **kwargs: P.kwargs,
) -> None:
    """
    Add a function to be called in the background after the response is sent.

    Read more about it in the
    [FastAPI docs for Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/).
    """
    return super().add_task(func, *args, **kwargs)
```
