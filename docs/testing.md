# Testing

Run the complete test suite from the project directory:

```bash
python -m unittest discover -s tests -v
```

The tests cover:

- newline framing and malformed JSON
- protocol and command validation
- keyboard/mouse dispatcher routing
- pairing and one-time code behavior
- session tokens
- loopback TCP behavior
- authentication and resume
- heartbeat response
- single active controller behavior
- discovery module loading/startup

The OS adapters are tested through a fake adapter in network/dispatcher tests so the suite does not inject real mouse or keyboard events.
