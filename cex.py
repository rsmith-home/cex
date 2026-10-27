import requests

url_root = "https://wss2.cex.uk.webuy.io/v3"
headers = {
    "user-agent": "CeXiOS/7.2.15(0) /OS 26.3.1/iPhone 14/U-03CAAE84-5AF9-4A3A-9FCE-7E991DD23AF7"
}


def get_stores():
    resp = requests.get(f"{url_root}/stores", headers=headers)
    resp.raise_for_status()
    return resp.json()["response"]["data"]["stores"]


def get_box(box_id):
    resp = requests.get(
        f"{url_root}/boxes/{box_id}/detail",
        headers=headers,
    )
    resp.raise_for_status()
    if resp.json()["response"]["data"] is not None:
        return resp.json()["response"]["data"]["boxDetails"][0]


def get_nearest_stores(box_id, latitude, longitude):
    resp = requests.get(
        f"{url_root}/boxes/{box_id}/neareststores?latitude={latitude}&longitude={longitude}",
        headers=headers,
    )
    resp.raise_for_status()
    if resp.json()["response"]["data"]:
        return resp.json()["response"]["data"]["nearestStores"]
    else:
        return []
