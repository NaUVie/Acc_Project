import time
import threading
from collections import defaultdict, deque
from fastapi import Request, HTTPException, status

_rate_limit_lock = threading.Lock()
_request_buckets: dict[str, deque] = defaultdict(deque)
_MAX_BUCKETS = 10000


def get_client_ip(request: Request) -> str:
    """Safely extract client IP for rate limiting."""
    client_host = request.client.host if request.client else "127.0.0.1"
    # Only trust X-Forwarded-For if request comes from localhost / private reverse proxy
    if client_host in ("127.0.0.1", "::1", "localhost") or client_host.startswith(("10.", "172.", "192.168.")):
        forwarded_for = request.headers.get("x-forwarded-for")
        if forwarded_for:
            first_ip = forwarded_for.split(",")[0].strip()
            if first_ip:
                return first_ip
    return client_host


def rate_limit(max_requests: int = 10, window_seconds: int = 60, scope: str = "default"):
    """
    FastAPI dependency for sliding-window rate limiting per IP and scope.
    """
    def _limiter(request: Request):
        ip = get_client_ip(request)
        key = f"{scope}:{ip}"
        now = time.monotonic()
        cutoff = now - window_seconds

        with _rate_limit_lock:
            # Prevent unbounded memory growth if many unique IPs hit the server
            if len(_request_buckets) > _MAX_BUCKETS and key not in _request_buckets:
                expired_keys = [
                    k for k, dq in _request_buckets.items()
                    if not dq or dq[-1] <= cutoff
                ]
                for k in expired_keys:
                    del _request_buckets[k]

            bucket = _request_buckets[key]
            while bucket and bucket[0] <= cutoff:
                bucket.popleft()

            if len(bucket) >= max_requests:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Bạn thao tác quá nhanh. Vui lòng đợi ít phút rồi thử lại!"
                )

            bucket.append(now)

    return _limiter

