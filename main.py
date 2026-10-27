import argparse
import sys
from time import sleep

from cex import get_box, get_nearest_stores, get_stores
from wishlist import add_platforms_argument, get_wishlist_box_ids


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

    stores = {
        x["storeId"]: {**x, "wishlistBoxes": [], "totalWeighting": 0}
        for x in get_stores()
    }

    boxes = {}
    for box_id in wishlist_box_ids:
        box = get_box(box_id)
        if box is None:
            continue
        box["weighting"] = _calculate_weighting(box)
        box["nearestStoreNames"] = []

        if box["collectionQuantity"] > 0:
            for store in get_nearest_stores(box_id, 54.664533, -1.632944):
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
        filter(lambda box: box[1]["collectionQuantity"] > 0, boxes.items()),
        key=lambda x: x[1]["collectionQuantity"],
    )
    out_of_stock_boxes = list(
        filter(lambda box: box[1]["collectionQuantity"] == 0, boxes.items())
    )
    t = 0
    t = 1


if __name__ == "__main__":
    sys.exit(main())
