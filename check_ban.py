"""Check whether the CeX API is currently blocking this IP (403 ban).

Sends exactly one request, so running it repeatedly is safe, but avoid running it
in a tight loop: requests made while banned may prolong the ban.

Exit codes:
  0  OK, no ban (request succeeded)
  1  banned (403)
  2  rate limited (429/529) - not banned, but wait a minute before running main.py
  3  inconclusive (network error or unexpected status)
"""

import sys

import requests

from cex import headers, url_root
from wishlist import available_platforms, load_platform_box_ids


def _sample_box_id():
    for platform in available_platforms():
        ids = load_platform_box_ids(platform)
        if ids:
            return ids[0]
    return "sps1g1015ab"


def main():
    url = f"{url_root}/boxes/{_sample_box_id()}/detail"
    try:
        resp = requests.get(url, headers=headers, timeout=30)
    except requests.RequestException as e:
        print(f"INCONCLUSIVE: request failed: {e}")
        return 3

    status = resp.status_code
    if status == 200:
        print("OK: no ban detected (200). Safe to run main.py.")
        return 0
    if status == 403:
        print("BANNED: 403 Forbidden. Don't run main.py yet; try again later.")
        return 1
    if status in (429, 529):
        print(f"RATE LIMITED: {status}. Not banned; wait a minute and retry.")
        return 2
    print(f"INCONCLUSIVE: unexpected status {status}")
    return 3


if __name__ == "__main__":
    sys.exit(main())
