# Testing and Demonstration

## Automated tests

```bash
python -m unittest discover -s tests -v
```

## Manual demo order

1. Start the host.
2. Note the pairing code and listening port.
3. Start `python test_client/client.py`.
4. Click Discover or manually enter the host IP.
5. Connect.
6. Enter the pairing code and click Pair.
7. Click Get Host Info.
8. Click Ping several times and observe latency.
9. Test touchpad movement and clicks.
10. Test Enter, Backspace, Escape and modifier keys.
11. Test media controls.
12. Test presentation next/previous.
13. Close the client and reconnect. The same session token can be resumed while it remains valid.
14. Stop/restart the host and confirm that a new pairing is required.

## Real LAN latency measurement

The temporary client shows one RTT measurement. For a larger academic experiment, run repeated pings and record min/average/max RTT and success rate. Repeat under different conditions such as close to the access point and farther away.

## Negative tests

- Send malformed JSON.
- Send an unknown action.
- Omit required fields.
- Send a command before pairing.
- Use a wrong pairing code.
- Use an invalid token.
- Disconnect during communication.

The expected behavior is a controlled error response or clean disconnect, not a server crash.
