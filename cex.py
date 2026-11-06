import random
import time

import requests

url_root = "https://wss2.cex.uk.webuy.io/v3"
headers = {
    "user-agent": "CeXiOS/7.2.15(0) /OS 26.3.1/iPhone 14/U-03CAAE84-5AF9-4A3A-9FCE-7E991DD23AF8"
}

# Pacing and retry behaviour, based on observed API limits:
# - the origin allows ~3 simultaneous requests, so requests are strictly sequential
# - 429 means "slow down" and clears quickly; ignoring it escalates to a 403 IP ban
MIN_INTERVAL = 0.5  # minimum seconds between requests
JITTER = 0.3  # extra random 0..JITTER seconds added to each interval
MAX_INTERVAL = 4.0  # ceiling for the adaptive interval
MAX_ATTEMPTS = 4  # attempts per request before giving up
BACKOFF_BASE = 5.0  # seconds; doubled for each retry
MAX_CONSECUTIVE_THROTTLES = 6  # abort the whole run before a ban is triggered
THROTTLE_STATUSES = {429, 529}
REQUEST_TIMEOUT = 30


class CexError(Exception):
    pass


class CexBannedError(CexError):
    """The API returned 403: this IP/client is blocked. Do not retry."""


class CexRateLimitedError(CexError):
    """Persistent 429/529 responses; the run was aborted to avoid a ban."""


class _Client:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(headers)
        self.interval = MIN_INTERVAL
        self.consecutive_throttles = 0
        self._last_request = 0.0

    def _pace(self):
        wait = self._last_request + self.interval + random.uniform(0, JITTER)
        delay = wait - time.monotonic()
        if delay > 0:
            time.sleep(delay)
        self._last_request = time.monotonic()

    def _on_throttle(self):
        self.consecutive_throttles += 1
        self.interval = min(self.interval * 2, MAX_INTERVAL)
        if self.consecutive_throttles >= MAX_CONSECUTIVE_THROTTLES:
            raise CexRateLimitedError(
                f"{self.consecutive_throttles} consecutive throttled responses; "
                "aborting to avoid an IP ban"
            )

    def _on_success(self):
        self.consecutive_throttles = 0
        self.interval = max(MIN_INTERVAL, self.interval * 0.9)

    def get(self, path):
        for attempt in range(MAX_ATTEMPTS):
            self._pace()
            try:
                resp = self.session.get(f"{url_root}{path}", timeout=REQUEST_TIMEOUT)
            except (requests.ConnectionError, requests.Timeout):
                if attempt == MAX_ATTEMPTS - 1:
                    raise
                time.sleep(BACKOFF_BASE * 2**attempt)
                continue

            if resp.status_code == 403:
                raise CexBannedError(
                    "403 Forbidden from the CeX API: this IP appears to be banned. "
                    "Run check_ban.py to see when it has lifted."
                )
            if resp.status_code in THROTTLE_STATUSES:
                self._on_throttle()
                if attempt == MAX_ATTEMPTS - 1:
                    break
                time.sleep(BACKOFF_BASE * 2**attempt * random.uniform(1.0, 1.5))
                continue

            resp.raise_for_status()
            self._on_success()
            return resp.json()

        raise CexRateLimitedError(
            f"{MAX_ATTEMPTS} throttled attempts in a row for {path}"
        )


_client = _Client()


def get_stores():
    return _client.get("/stores")["response"]["data"]["stores"]


def get_box(box_id):
    data = _client.get(f"/boxes/{box_id}/detail")["response"]["data"]
    if data is not None:
        return data["boxDetails"][0]


def get_nearest_stores(box_id, latitude, longitude):
    data = _client.get(
        f"/boxes/{box_id}/neareststores?latitude={latitude}&longitude={longitude}"
    )["response"]["data"]
    if data:
        return data["nearestStores"]
    else:
        return []
