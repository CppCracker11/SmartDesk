# SmartDesk Protocol 1.0

## Transport and framing

- TCP is the command connection.
- Every message is one UTF-8 JSON object followed by `\n`.
- UDP port `8766` is discovery only; it never carries commands.
- TCP may be used directly with a manual host IP and port.

The host sends an initial state message after TCP connection:

```json
{"type":"state","state":"AUTHENTICATING"}
```

## Request fields

| Field | Required | Meaning |
|---|---|---|
| `version` | yes | Protocol version, currently `1.0` |
| `id` | yes | Non-empty request identifier |
| `type` | yes | `auth`, `mouse`, `keyboard`, `media`, `presentation`, or `system` |
| `action` | yes | Action supported by the selected type |
| `data` | yes | Object containing action parameters; may be empty |
| `token` | commands | Session token returned by pairing/resume |

Authenticated commands use the same top-level `token` field. The server validates it before dispatching the command.

## Pairing

1. Discover the host with UDP or use a manual IP/port.
2. Open TCP.
3. Send the temporary pairing code:

```json
{"version":"1.0","id":"1","type":"auth","action":"pair","data":{"code":"482731"}}
```

4. On success, the host returns a session token:

```json
{"id":"1","status":"ok","data":{"token":"SESSION_TOKEN","state":"ACTIVE"}}
```

The pairing code is single-use and expires after the configured pairing timeout.

Only one valid SmartDesk session may exist for the host at a time. A second controller receives `HOST_BUSY`, including while the existing session is temporarily disconnected but still resumable.

## Authenticated commands

Every command after authentication carries the session token:

```json
{"version":"1.0","id":"2","type":"mouse","action":"move","token":"SESSION_TOKEN","data":{"dx":10,"dy":-4}}
```

A valid token represents an authenticated session. The current TCP connection is a separate active state. Losing TCP does not immediately invalidate the token.

## Resume after reconnect

After a temporary TCP/network loss, reconnect and present the existing token:

```json
{"version":"1.0","id":"3","type":"auth","action":"resume","data":{"token":"SESSION_TOKEN"}}
```

If the token is valid and no other connection is active, the host resumes the session:

```json
{"id":"3","status":"ok","data":{"token":"SESSION_TOKEN","state":"ACTIVE"}}
```

If the token has expired or is invalid, the host returns `SESSION_EXPIRED` and a fresh pairing is required. If another connection is active, the host returns `HOST_BUSY`.

## Mouse

### Move

```json
{"version":"1.0","id":"10","type":"mouse","action":"move","token":"SESSION_TOKEN","data":{"dx":10,"dy":-4}}
```

### Click

Actions: `left_click`, `right_click`, `middle_click`.

```json
{"version":"1.0","id":"11","type":"mouse","action":"left_click","token":"SESSION_TOKEN","data":{}}
```

### Double click

```json
{"version":"1.0","id":"12","type":"mouse","action":"double_click","token":"SESSION_TOKEN","data":{}}
```

### Scroll

```json
{"version":"1.0","id":"13","type":"mouse","action":"scroll","token":"SESSION_TOKEN","data":{"dx":0,"dy":5}}
```

## Keyboard

Protocol key names are platform-independent. `CTRL` and `CMD` are separate concepts; the adapter performs the platform-specific translation.

### Press / release

```json
{"version":"1.0","id":"20","type":"keyboard","action":"press","token":"SESSION_TOKEN","data":{"key":"ENTER"}}
```

```json
{"version":"1.0","id":"21","type":"keyboard","action":"release","token":"SESSION_TOKEN","data":{"key":"ENTER"}}
```

### Combination

Windows/Linux example:

```json
{"version":"1.0","id":"22","type":"keyboard","action":"combo","token":"SESSION_TOKEN","data":{"keys":["CTRL","C"]}}
```

macOS example:

```json
{"version":"1.0","id":"23","type":"keyboard","action":"combo","token":"SESSION_TOKEN","data":{"keys":["CMD","C"]}}
```

Supported named keys include `ENTER`, `ESC`, `TAB`, `BACKSPACE`, `SHIFT`, `CTRL`, `ALT`, `CMD`, `SPACE`, `UP`, `DOWN`, `LEFT`, `RIGHT`, `HOME`, `END`, `PAGEUP`, `PAGEDOWN`, `DELETE`, `INSERT`, `CAPSLOCK`, and `F1`-`F12`. Single printable characters are also supported.

## Media

Actions: `play_pause`, `next`, `previous`, `volume_up`, `volume_down`, `mute`.

```json
{"version":"1.0","id":"30","type":"media","action":"play_pause","token":"SESSION_TOKEN","data":{}}
```

## Presentation

Actions: `next`, `previous`.

```json
{"version":"1.0","id":"40","type":"presentation","action":"next","token":"SESSION_TOKEN","data":{}}
```

## Heartbeat and latency

Send:

```json
{"version":"1.0","id":"50","type":"system","action":"ping","token":"SESSION_TOKEN","data":{}}
```

The host responds with a server timestamp:

```json
{"id":"50","status":"ok","data":{"pong_ns":123456789012345}}
```

The client measures RTT using its own monotonic clock around the request/response. The host does not fabricate a latency value.

## System

### Host information

```json
{"version":"1.0","id":"51","type":"system","action":"get_host_info","token":"SESSION_TOKEN","data":{}}
```

### Disconnect

```json
{"version":"1.0","id":"52","type":"system","action":"disconnect","token":"SESSION_TOKEN","data":{}}
```

Closing TCP releases the active connection but does not immediately invalidate the session token. The token remains resumable until session expiry.

## Responses

Success:

```json
{"id":"1","status":"ok","data":{}}
```

Error:

```json
{"id":"1","status":"error","error":{"code":"INVALID_COMMAND","message":"unknown command"}}
```

Defined error codes:

- `INVALID_JSON`
- `INVALID_MESSAGE`
- `UNSUPPORTED_VERSION`
- `INVALID_COMMAND`
- `INVALID_PARAMETER`
- `NOT_AUTHENTICATED`
- `PAIRING_FAILED`
- `SESSION_EXPIRED`
- `HOST_BUSY`
- `COMMAND_FAILED`
- `INTERNAL_ERROR`

Malformed network input is rejected without crashing the host.
