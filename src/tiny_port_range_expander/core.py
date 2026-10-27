"""Core port-range expansion logic."""


class InvalidPortRange(ValueError):
    """Raised when a port specification cannot be parsed.

    Subclassing ValueError so callers catching ValueError still catch it.
    """


def _parse_port(token: str) -> int:
    """Parse a single port number from *token*.

    int(token) alone would accept surrounding whitespace and signs ('+80'),
    so we validate the raw characters first to keep the error message precise.
    """
    if not token.isdigit():
        raise InvalidPortRange(f"invalid port: {token!r}")
    return int(token)


def expand_ports(spec: str) -> frozenset:
    """Expand a port specification into a sorted frozenset of integers.

    Accepted syntax:
      - Single ports:          '80'
      - Ranges (inclusive):    '8000-8100'
      - Comma-separated lists: '80,443,8000-8100'
      - Whitespace around tokens is ignored: ' 80 , 443 '

    The empty string yields an empty frozenset.

    Returns a *frozenset* (immutable and hashable) rather than a list so the
    result can be used directly as a dict key or set member if needed.
    """
    if not isinstance(spec, str):
        raise TypeError("spec must be a string")

    spec = spec.strip()
    if not spec:
        return frozenset()

    parts = spec.split(",")
    result = set()

    for part in parts:
        token = part.strip()
        if not token:
            # An empty token (e.g. '80,,443') is treated as malformed input
            # rather than silently dropped, so the caller is alerted.
            raise InvalidPortRange("empty token in port specification")

        if "-" in token:
            segments = token.split("-")
            if len(segments) != 2:
                # More than one dash means something like '1-2-3', which is
                # ambiguous and rejected.
                raise InvalidPortRange(f"invalid range: {token!r}")
            start = _parse_port(segments[0].strip())
            end = _parse_port(segments[1].strip())
            if start > end:
                raise InvalidPortRange(
                    f"range start {start} is greater than end {end}"
                )
            result.update(range(start, end + 1))
        else:
            result.add(_parse_port(token))

    return frozenset(result)
