# SmartDesk Protocol 1.0

Transport: TCP for commands. Messages are UTF-8 JSON objects terminated by newline (`\\n`). UDP port 8766 is used only for discovery.

## Common fields

| Field | Meaning |
|---|---|
| `version` | Protocol version, currently `1.0` |
| `id` | Controller-generated request identifier |
| `type` | Command group |
| `action` | Action within the group |
| `data` | Action-specific object |
| `token` | Session token after authentication |

## Pair

```json
{"version":"1.0","id":"1","type":"auth","action":"pair","data":{"code":"482731"}}
```

The host returns a session token. The pairing code is random and one-time-use until a new code is generated.

## Resume after reconnect

```json
{"version":"1.0","id":"2","type":"auth","action":"resume","data":{"token":"..."}}
```

## Mouse

- `move`: `dx`, `dy`
- `left_click`
- `right_click`
- `double_click`
- `middle_click`
- `scroll`: optional `dx`, `dy`

## Keyboard

- `press`: `key`
- `release`: `key`
- `combo`: `keys` list

Supported named keys include ENTER, ESC, BACKSPACE, TAB, SHIFT, CTRL, ALT, SPACE, arrows, HOME, END, PAGEUP, PAGEDOWN, DELETE, INSERT, CAPSLOCK and F1-F12. Single printable characters are also accepted.

## Media

- `play_pause`
- `next`
- `previous`
- `volume_up`
- `volume_down`
- `mute`

## Presentation

- `next`
- `previous`

The MVP maps presentation actions to RIGHT/LEFT arrow input because this works with many presentation applications without knowing the presentation software.

## System

- `ping`
- `get_host_info`
- `disconnect`

## Success response

```json
{"id":"12345","status":"ok","data":{}}
```

## Error response

```json
{"id":"12345","status":"error","error":{"code":"INVALID_COMMAND","message":"Unknown command"}}
```

## Validation

The host checks protocol version, message ID, type/action, required fields, key names, numeric ranges and pairing-code format. Unknown commands are never passed to the OS layer.
