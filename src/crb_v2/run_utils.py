from __future__ import annotations

import signal
from contextlib import contextmanager


class TimeoutException(RuntimeError):
    pass


@contextmanager
def timeout(seconds: int | None):
    if not seconds:
        yield
        return

    def _handler(signum, frame):  # type: ignore[no-untyped-def]
        raise TimeoutException(f"Timed out after {seconds} seconds")

    previous = signal.signal(signal.SIGALRM, _handler)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)
