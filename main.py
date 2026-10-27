import argparse
import sys
from time import sleep

import requests

from wishlist import add_platforms_argument, get_wishlist_box_ids

headers = {
    "user-agent": "CeXiOS/7.2.15(0) /OS 26.3.1/iPhone 14/U-03CAAE84-5AF9-4A3A-9FCE-7E991DD23AF7"
}

boxes = {}
stores = {}


def _calculate_weighting(box):
    if box["ecomQuantityOnHand"] == 0:
        return 0
    if box["ecomQuantityOnHand"] < 6:
        return 5
    elif box["ecomQuantityOnHand"] < 11:
        return 4
    elif box["ecomQuantityOnHand"] < 21:
        return 3
    elif box["ecomQuantityOnHand"] < 30:
        return 2
    else:
        return 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Check CeX stock for wishlist boxes, by platform."
    )
    add_platforms_argument(parser)
    args = parser.parse_args(argv)

    wishlist_box_ids = get_wishlist_box_ids(args.platforms)

    resp = requests.get("https://wss2.cex.uk.webuy.io/v3/stores", headers=headers)
    resp.raise_for_status()
    for store in resp.json()["response"]["data"]["stores"]:
        store["wishlistBoxes"] = []
        store["totalWeighting"] = 0
        stores[store["storeId"]] = store

    for box_id in wishlist_box_ids:
        resp = requests.get(
            "https://wss2.cex.uk.webuy.io/v3/boxes/{0}/detail".format(box_id),
            headers=headers,
        )
        resp.raise_for_status()
        if resp.json()["response"]["data"] is None:
            continue
        box = resp.json()["response"]["data"]["boxDetails"][0]
        box["weighting"] = _calculate_weighting(box)
        box["nearestStoreNames"] = []

        if box["collectionQuantity"] > 0:
            resp = requests.get(
                "https://wss2.cex.uk.webuy.io/v3/boxes/{0}/neareststores"
                # "?latitude=51.522556&longitude=0.592793".format(box_id), headers=headers)  # Brighton
                "?latitude=54.664533&longitude=-1.632944".format(box_id),
                headers=headers,
            )  # Home
            resp.raise_for_status()
            if resp.json()["response"]["data"]:
                for store in resp.json()["response"]["data"]["nearestStores"]:
                    store_id = int(store["storeId"])
                    box["nearestStoreNames"].append(store["storeName"])
                    stores[store_id]["wishlistBoxes"].append(box)
                    stores[store_id]["totalWeighting"] += box["weighting"]

        boxes[box_id] = box
        if (len(boxes) % 50) == 49:
            sleep(60.0)
        else:
            sleep(2.0)

    for store in stores.items():
        store[1]["wishlistBoxes"] = {
            box["boxName"]: box
            for box in sorted(
                store[1]["wishlistBoxes"], key=lambda x: x["collectionQuantity"]
            )
        }

    best_stores = sorted(
        stores.items(), key=lambda x: x[1]["totalWeighting"], reverse=True
    )
    rarest_boxes = sorted(
        list(filter(lambda box: box[1]["collectionQuantity"] > 0, boxes.items())),
        key=lambda x: x[1]["collectionQuantity"],
    )
    out_of_stock_boxes = list(
        filter(lambda box: box[1]["collectionQuantity"] == 0, boxes.items())
    )
    t = 0
    t = 1


if __name__ == "__main__":
    sys.exit(main())
