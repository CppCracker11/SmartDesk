# Networking Concepts Demonstrated

## LAN

The controller and host communicate over a local IP network, normally the same Wi-Fi or Ethernet network.

## IP address and port

The host is identified by an IP address and a TCP port. The default TCP port is 8765.

## Client-server model

The host listens for connections. The controller initiates a TCP connection and sends requests. The host processes them and returns responses.

## TCP

TCP provides an ordered, reliable byte stream. That is useful for control commands because commands should not silently disappear or arrive out of order.

TCP does not preserve application message boundaries. A single `recv()` may contain half a JSON object, one object, or several objects. SmartDesk therefore uses newline-delimited JSON as application-layer message framing.

## UDP discovery

UDP is useful for small, connectionless discovery messages. A controller broadcasts `SMARTDESK_DISCOVER`; hosts respond with their TCP endpoint. Discovery is optional because manual IP entry is supported.

## Application-layer protocol

JSON defines the SmartDesk application protocol above TCP. The protocol has version, ID, type, action and data fields and explicit response/error formats.

## Reliability and connection management

TCP handles byte delivery. SmartDesk separately handles application authentication, malformed data, disconnects, reconnects and session tokens.

## Authentication

A short-lived pairing code proves that the controller is intentionally pairing with the host. A random session token is then used for commands. This is application-layer authentication; it is not encryption.

## Latency

The test client sends a ping and measures elapsed time using a monotonic clock from send to response. Repeated measurements can be summarized as minimum, average and maximum RTT. TCP reliability does not guarantee a fixed latency.

## Performance test

For a real LAN test, repeat PING many times, record successful responses and calculate:

- success rate = successful pings / total pings × 100
- average RTT
- minimum RTT
- maximum RTT

Do not treat these values as universal network performance; they depend on Wi-Fi conditions, distance, congestion and the host/controller hardware.
