https://fastapi.tiangolo.com/reference/status/
# Status Codes[¶](#status-codes "Permanent link")

You can import the `status` module from `fastapi`:

```python
from fastapi import status
```

`status` is provided directly by Starlette.

It contains a group of named constants (variables) with integer status codes.

For example:

* 200: `status.HTTP_200_OK`
* 403: `status.HTTP_403_FORBIDDEN`
* etc.

It can be convenient to quickly access HTTP (and WebSocket) status codes in your app, using autocompletion for the name without having to remember the integer status codes by memory.

Read more about it in the [FastAPI docs about Response Status Code](https://fastapi.tiangolo.com/tutorial/response-status-code/).

## Example[¶](#example "Permanent link")

```python
from fastapi import FastAPI, status

app = FastAPI()


@app.get("/items/", status_code=status.HTTP_418_IM_A_TEAPOT)
def read_items():
    return [{"name": "Plumbus"}, {"name": "Portal Gun"}]
```

## fastapi.status [¶](#fastapi.status "Permanent link")

HTTP codes
See HTTP Status Code Registry:
https://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml

And RFC 9110 - https://www.rfc-editor.org/rfc/rfc9110

### HTTP\_100\_CONTINUE `module-attribute` [¶](#fastapi.status.HTTP_100_CONTINUE "Permanent link")

```python
HTTP_100_CONTINUE = 100
```

### HTTP\_101\_SWITCHING\_PROTOCOLS `module-attribute` [¶](#fastapi.status.HTTP_101_SWITCHING_PROTOCOLS "Permanent link")

```python
HTTP_101_SWITCHING_PROTOCOLS = 101
```

### HTTP\_102\_PROCESSING `module-attribute` [¶](#fastapi.status.HTTP_102_PROCESSING "Permanent link")

```python
HTTP_102_PROCESSING = 102
```

### HTTP\_103\_EARLY\_HINTS `module-attribute` [¶](#fastapi.status.HTTP_103_EARLY_HINTS "Permanent link")

```python
HTTP_103_EARLY_HINTS = 103
```

### HTTP\_200\_OK `module-attribute` [¶](#fastapi.status.HTTP_200_OK "Permanent link")

```python
HTTP_200_OK = 200
```

### HTTP\_201\_CREATED `module-attribute` [¶](#fastapi.status.HTTP_201_CREATED "Permanent link")

```python
HTTP_201_CREATED = 201
```

### HTTP\_202\_ACCEPTED `module-attribute` [¶](#fastapi.status.HTTP_202_ACCEPTED "Permanent link")

```python
HTTP_202_ACCEPTED = 202
```

### HTTP\_203\_NON\_AUTHORITATIVE\_INFORMATION `module-attribute` [¶](#fastapi.status.HTTP_203_NON_AUTHORITATIVE_INFORMATION "Permanent link")

```python
HTTP_203_NON_AUTHORITATIVE_INFORMATION = 203
```

### HTTP\_204\_NO\_CONTENT `module-attribute` [¶](#fastapi.status.HTTP_204_NO_CONTENT "Permanent link")

```python
HTTP_204_NO_CONTENT = 204
```

### HTTP\_205\_RESET\_CONTENT `module-attribute` [¶](#fastapi.status.HTTP_205_RESET_CONTENT "Permanent link")

```python
HTTP_205_RESET_CONTENT = 205
```

### HTTP\_206\_PARTIAL\_CONTENT `module-attribute` [¶](#fastapi.status.HTTP_206_PARTIAL_CONTENT "Permanent link")

```python
HTTP_206_PARTIAL_CONTENT = 206
```

### HTTP\_207\_MULTI\_STATUS `module-attribute` [¶](#fastapi.status.HTTP_207_MULTI_STATUS "Permanent link")

```python
HTTP_207_MULTI_STATUS = 207
```

### HTTP\_208\_ALREADY\_REPORTED `module-attribute` [¶](#fastapi.status.HTTP_208_ALREADY_REPORTED "Permanent link")

```python
HTTP_208_ALREADY_REPORTED = 208
```

### HTTP\_226\_IM\_USED `module-attribute` [¶](#fastapi.status.HTTP_226_IM_USED "Permanent link")

```python
HTTP_226_IM_USED = 226
```

### HTTP\_300\_MULTIPLE\_CHOICES `module-attribute` [¶](#fastapi.status.HTTP_300_MULTIPLE_CHOICES "Permanent link")

```python
HTTP_300_MULTIPLE_CHOICES = 300
```

### HTTP\_301\_MOVED\_PERMANENTLY `module-attribute` [¶](#fastapi.status.HTTP_301_MOVED_PERMANENTLY "Permanent link")

```python
HTTP_301_MOVED_PERMANENTLY = 301
```

### HTTP\_302\_FOUND `module-attribute` [¶](#fastapi.status.HTTP_302_FOUND "Permanent link")

```python
HTTP_302_FOUND = 302
```

### HTTP\_303\_SEE\_OTHER `module-attribute` [¶](#fastapi.status.HTTP_303_SEE_OTHER "Permanent link")

```python
HTTP_303_SEE_OTHER = 303
```

### HTTP\_304\_NOT\_MODIFIED `module-attribute` [¶](#fastapi.status.HTTP_304_NOT_MODIFIED "Permanent link")

```python
HTTP_304_NOT_MODIFIED = 304
```

### HTTP\_305\_USE\_PROXY `module-attribute` [¶](#fastapi.status.HTTP_305_USE_PROXY "Permanent link")

```python
HTTP_305_USE_PROXY = 305
```

### HTTP\_306\_RESERVED `module-attribute` [¶](#fastapi.status.HTTP_306_RESERVED "Permanent link")

```python
HTTP_306_RESERVED = 306
```

### HTTP\_307\_TEMPORARY\_REDIRECT `module-attribute` [¶](#fastapi.status.HTTP_307_TEMPORARY_REDIRECT "Permanent link")

```python
HTTP_307_TEMPORARY_REDIRECT = 307
```

### HTTP\_308\_PERMANENT\_REDIRECT `module-attribute` [¶](#fastapi.status.HTTP_308_PERMANENT_REDIRECT "Permanent link")

```python
HTTP_308_PERMANENT_REDIRECT = 308
```

### HTTP\_400\_BAD\_REQUEST `module-attribute` [¶](#fastapi.status.HTTP_400_BAD_REQUEST "Permanent link")

```python
HTTP_400_BAD_REQUEST = 400
```

### HTTP\_401\_UNAUTHORIZED `module-attribute` [¶](#fastapi.status.HTTP_401_UNAUTHORIZED "Permanent link")

```python
HTTP_401_UNAUTHORIZED = 401
```

### HTTP\_402\_PAYMENT\_REQUIRED `module-attribute` [¶](#fastapi.status.HTTP_402_PAYMENT_REQUIRED "Permanent link")

```python
HTTP_402_PAYMENT_REQUIRED = 402
```

### HTTP\_403\_FORBIDDEN `module-attribute` [¶](#fastapi.status.HTTP_403_FORBIDDEN "Permanent link")

```python
HTTP_403_FORBIDDEN = 403
```

### HTTP\_404\_NOT\_FOUND `module-attribute` [¶](#fastapi.status.HTTP_404_NOT_FOUND "Permanent link")

```python
HTTP_404_NOT_FOUND = 404
```

### HTTP\_405\_METHOD\_NOT\_ALLOWED `module-attribute` [¶](#fastapi.status.HTTP_405_METHOD_NOT_ALLOWED "Permanent link")

```python
HTTP_405_METHOD_NOT_ALLOWED = 405
```

### HTTP\_406\_NOT\_ACCEPTABLE `module-attribute` [¶](#fastapi.status.HTTP_406_NOT_ACCEPTABLE "Permanent link")

```python
HTTP_406_NOT_ACCEPTABLE = 406
```

### HTTP\_407\_PROXY\_AUTHENTICATION\_REQUIRED `module-attribute` [¶](#fastapi.status.HTTP_407_PROXY_AUTHENTICATION_REQUIRED "Permanent link")

```python
HTTP_407_PROXY_AUTHENTICATION_REQUIRED = 407
```

### HTTP\_408\_REQUEST\_TIMEOUT `module-attribute` [¶](#fastapi.status.HTTP_408_REQUEST_TIMEOUT "Permanent link")

```python
HTTP_408_REQUEST_TIMEOUT = 408
```

### HTTP\_409\_CONFLICT `module-attribute` [¶](#fastapi.status.HTTP_409_CONFLICT "Permanent link")

```python
HTTP_409_CONFLICT = 409
```

### HTTP\_410\_GONE `module-attribute` [¶](#fastapi.status.HTTP_410_GONE "Permanent link")

```python
HTTP_410_GONE = 410
```

### HTTP\_411\_LENGTH\_REQUIRED `module-attribute` [¶](#fastapi.status.HTTP_411_LENGTH_REQUIRED "Permanent link")

```python
HTTP_411_LENGTH_REQUIRED = 411
```

### HTTP\_412\_PRECONDITION\_FAILED `module-attribute` [¶](#fastapi.status.HTTP_412_PRECONDITION_FAILED "Permanent link")

```python
HTTP_412_PRECONDITION_FAILED = 412
```

### HTTP\_413\_CONTENT\_TOO\_LARGE `module-attribute` [¶](#fastapi.status.HTTP_413_CONTENT_TOO_LARGE "Permanent link")

```python
HTTP_413_CONTENT_TOO_LARGE = 413
```

### HTTP\_414\_URI\_TOO\_LONG `module-attribute` [¶](#fastapi.status.HTTP_414_URI_TOO_LONG "Permanent link")

```python
HTTP_414_URI_TOO_LONG = 414
```

### HTTP\_415\_UNSUPPORTED\_MEDIA\_TYPE `module-attribute` [¶](#fastapi.status.HTTP_415_UNSUPPORTED_MEDIA_TYPE "Permanent link")

```python
HTTP_415_UNSUPPORTED_MEDIA_TYPE = 415
```

### HTTP\_416\_RANGE\_NOT\_SATISFIABLE `module-attribute` [¶](#fastapi.status.HTTP_416_RANGE_NOT_SATISFIABLE "Permanent link")

```python
HTTP_416_RANGE_NOT_SATISFIABLE = 416
```

### HTTP\_417\_EXPECTATION\_FAILED `module-attribute` [¶](#fastapi.status.HTTP_417_EXPECTATION_FAILED "Permanent link")

```python
HTTP_417_EXPECTATION_FAILED = 417
```

### HTTP\_418\_IM\_A\_TEAPOT `module-attribute` [¶](#fastapi.status.HTTP_418_IM_A_TEAPOT "Permanent link")

```python
HTTP_418_IM_A_TEAPOT = 418
```

### HTTP\_421\_MISDIRECTED\_REQUEST `module-attribute` [¶](#fastapi.status.HTTP_421_MISDIRECTED_REQUEST "Permanent link")

```python
HTTP_421_MISDIRECTED_REQUEST = 421
```

### HTTP\_422\_UNPROCESSABLE\_CONTENT `module-attribute` [¶](#fastapi.status.HTTP_422_UNPROCESSABLE_CONTENT "Permanent link")

```python
HTTP_422_UNPROCESSABLE_CONTENT = 422
```

### HTTP\_423\_LOCKED `module-attribute` [¶](#fastapi.status.HTTP_423_LOCKED "Permanent link")

```python
HTTP_423_LOCKED = 423
```

### HTTP\_424\_FAILED\_DEPENDENCY `module-attribute` [¶](#fastapi.status.HTTP_424_FAILED_DEPENDENCY "Permanent link")

```python
HTTP_424_FAILED_DEPENDENCY = 424
```

### HTTP\_425\_TOO\_EARLY `module-attribute` [¶](#fastapi.status.HTTP_425_TOO_EARLY "Permanent link")

```python
HTTP_425_TOO_EARLY = 425
```

### HTTP\_426\_UPGRADE\_REQUIRED `module-attribute` [¶](#fastapi.status.HTTP_426_UPGRADE_REQUIRED "Permanent link")

```python
HTTP_426_UPGRADE_REQUIRED = 426
```

### HTTP\_428\_PRECONDITION\_REQUIRED `module-attribute` [¶](#fastapi.status.HTTP_428_PRECONDITION_REQUIRED "Permanent link")

```python
HTTP_428_PRECONDITION_REQUIRED = 428
```

### HTTP\_429\_TOO\_MANY\_REQUESTS `module-attribute` [¶](#fastapi.status.HTTP_429_TOO_MANY_REQUESTS "Permanent link")

```python
HTTP_429_TOO_MANY_REQUESTS = 429
```

### HTTP\_431\_REQUEST\_HEADER\_FIELDS\_TOO\_LARGE `module-attribute` [¶](#fastapi.status.HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE "Permanent link")

```python
HTTP_431_REQUEST_HEADER_FIELDS_TOO_LARGE = 431
```

### HTTP\_451\_UNAVAILABLE\_FOR\_LEGAL\_REASONS `module-attribute` [¶](#fastapi.status.HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS "Permanent link")

```python
HTTP_451_UNAVAILABLE_FOR_LEGAL_REASONS = 451
```

### HTTP\_500\_INTERNAL\_SERVER\_ERROR `module-attribute` [¶](#fastapi.status.HTTP_500_INTERNAL_SERVER_ERROR "Permanent link")

```python
HTTP_500_INTERNAL_SERVER_ERROR = 500
```

### HTTP\_501\_NOT\_IMPLEMENTED `module-attribute` [¶](#fastapi.status.HTTP_501_NOT_IMPLEMENTED "Permanent link")

```python
HTTP_501_NOT_IMPLEMENTED = 501
```

### HTTP\_502\_BAD\_GATEWAY `module-attribute` [¶](#fastapi.status.HTTP_502_BAD_GATEWAY "Permanent link")

```python
HTTP_502_BAD_GATEWAY = 502
```

### HTTP\_503\_SERVICE\_UNAVAILABLE `module-attribute` [¶](#fastapi.status.HTTP_503_SERVICE_UNAVAILABLE "Permanent link")

```python
HTTP_503_SERVICE_UNAVAILABLE = 503
```

### HTTP\_504\_GATEWAY\_TIMEOUT `module-attribute` [¶](#fastapi.status.HTTP_504_GATEWAY_TIMEOUT "Permanent link")

```python
HTTP_504_GATEWAY_TIMEOUT = 504
```

### HTTP\_505\_HTTP\_VERSION\_NOT\_SUPPORTED `module-attribute` [¶](#fastapi.status.HTTP_505_HTTP_VERSION_NOT_SUPPORTED "Permanent link")

```python
HTTP_505_HTTP_VERSION_NOT_SUPPORTED = 505
```

### HTTP\_506\_VARIANT\_ALSO\_NEGOTIATES `module-attribute` [¶](#fastapi.status.HTTP_506_VARIANT_ALSO_NEGOTIATES "Permanent link")

```python
HTTP_506_VARIANT_ALSO_NEGOTIATES = 506
```

### HTTP\_507\_INSUFFICIENT\_STORAGE `module-attribute` [¶](#fastapi.status.HTTP_507_INSUFFICIENT_STORAGE "Permanent link")

```python
HTTP_507_INSUFFICIENT_STORAGE = 507
```

### HTTP\_508\_LOOP\_DETECTED `module-attribute` [¶](#fastapi.status.HTTP_508_LOOP_DETECTED "Permanent link")

```python
HTTP_508_LOOP_DETECTED = 508
```

### HTTP\_510\_NOT\_EXTENDED `module-attribute` [¶](#fastapi.status.HTTP_510_NOT_EXTENDED "Permanent link")

```python
HTTP_510_NOT_EXTENDED = 510
```

### HTTP\_511\_NETWORK\_AUTHENTICATION\_REQUIRED `module-attribute` [¶](#fastapi.status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED "Permanent link")

```python
HTTP_511_NETWORK_AUTHENTICATION_REQUIRED = 511
```

WebSocket codes
https://www.iana.org/assignments/websocket/websocket.xml#close-code-number
https://developer.mozilla.org/en-US/docs/Web/API/CloseEvent

### WS\_1000\_NORMAL\_CLOSURE `module-attribute` [¶](#fastapi.status.WS_1000_NORMAL_CLOSURE "Permanent link")

```python
WS_1000_NORMAL_CLOSURE = 1000
```

### WS\_1001\_GOING\_AWAY `module-attribute` [¶](#fastapi.status.WS_1001_GOING_AWAY "Permanent link")

```python
WS_1001_GOING_AWAY = 1001
```

### WS\_1002\_PROTOCOL\_ERROR `module-attribute` [¶](#fastapi.status.WS_1002_PROTOCOL_ERROR "Permanent link")

```python
WS_1002_PROTOCOL_ERROR = 1002
```

### WS\_1003\_UNSUPPORTED\_DATA `module-attribute` [¶](#fastapi.status.WS_1003_UNSUPPORTED_DATA "Permanent link")

```python
WS_1003_UNSUPPORTED_DATA = 1003
```

### WS\_1005\_NO\_STATUS\_RCVD `module-attribute` [¶](#fastapi.status.WS_1005_NO_STATUS_RCVD "Permanent link")

```python
WS_1005_NO_STATUS_RCVD = 1005
```

### WS\_1006\_ABNORMAL\_CLOSURE `module-attribute` [¶](#fastapi.status.WS_1006_ABNORMAL_CLOSURE "Permanent link")

```python
WS_1006_ABNORMAL_CLOSURE = 1006
```

### WS\_1007\_INVALID\_FRAME\_PAYLOAD\_DATA `module-attribute` [¶](#fastapi.status.WS_1007_INVALID_FRAME_PAYLOAD_DATA "Permanent link")

```python
WS_1007_INVALID_FRAME_PAYLOAD_DATA = 1007
```

### WS\_1008\_POLICY\_VIOLATION `module-attribute` [¶](#fastapi.status.WS_1008_POLICY_VIOLATION "Permanent link")

```python
WS_1008_POLICY_VIOLATION = 1008
```

### WS\_1009\_MESSAGE\_TOO\_BIG `module-attribute` [¶](#fastapi.status.WS_1009_MESSAGE_TOO_BIG "Permanent link")

```python
WS_1009_MESSAGE_TOO_BIG = 1009
```

### WS\_1010\_MANDATORY\_EXT `module-attribute` [¶](#fastapi.status.WS_1010_MANDATORY_EXT "Permanent link")

```python
WS_1010_MANDATORY_EXT = 1010
```

### WS\_1011\_INTERNAL\_ERROR `module-attribute` [¶](#fastapi.status.WS_1011_INTERNAL_ERROR "Permanent link")

```python
WS_1011_INTERNAL_ERROR = 1011
```

### WS\_1012\_SERVICE\_RESTART `module-attribute` [¶](#fastapi.status.WS_1012_SERVICE_RESTART "Permanent link")

```python
WS_1012_SERVICE_RESTART = 1012
```

### WS\_1013\_TRY\_AGAIN\_LATER `module-attribute` [¶](#fastapi.status.WS_1013_TRY_AGAIN_LATER "Permanent link")

```python
WS_1013_TRY_AGAIN_LATER = 1013
```

### WS\_1014\_BAD\_GATEWAY `module-attribute` [¶](#fastapi.status.WS_1014_BAD_GATEWAY "Permanent link")

```python
WS_1014_BAD_GATEWAY = 1014
```

### WS\_1015\_TLS\_HANDSHAKE `module-attribute` [¶](#fastapi.status.WS_1015_TLS_HANDSHAKE "Permanent link")

```python
WS_1015_TLS_HANDSHAKE = 1015
```
