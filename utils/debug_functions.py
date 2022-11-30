from flask import request
from datetime import datetime, timezone


def get_client_request_ip_address() -> str:
    return request.remote_addr


def get_current_timestamp_millis_utc() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)
