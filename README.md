# tiny_port_range_expander

Expand comma-and-dash port specifications like `'80,443,8000-8100'` into a sorted set of individual port numbers.

```python
from tiny_port_range_expander import expand_ports

ports = expand_ports("80,443,8000-8100")
# frozenset({80, 443, 8000, 8001, ..., 8100})

print(8080 in ports)  # True
```

## Why

Configuration files, CLI flags, and firewall rules frequently accept port ranges in a compact `start-end` notation, but downstream logic often needs to test membership against individual ports. This library does exactly that expansion and nothing else: parse, validate, return a `frozenset`.

The trade-off is simplicity over flexibility. There is no support for named protocols, service lookups, or IPv6 brackets. If you need those, use a heavier library.

## Edge cases

- The empty string returns an empty `frozenset`.
- Whitespace around tokens is tolerated: `' 80 , 443 '` works.
- An empty token between commas (`'80,,443'`) raises `InvalidPortRange` rather than being silently skipped, so malformed input is surfaced.
- Port `0` is accepted as a valid port number.
- Overlapping ranges and duplicates are collapsed into the set.
