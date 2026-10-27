import argparse
from pathlib import Path

WISHLISTS_DIR = Path(__file__).parent / "wishlists"


def available_platforms():
    return sorted(path.stem for path in WISHLISTS_DIR.glob("*.txt"))


def load_platform_box_ids(platform):
    box_ids = []
    for line in (WISHLISTS_DIR / f"{platform}.txt").read_text().splitlines():
        box_id = line.split("#", 1)[0].strip()
        if box_id:
            box_ids.append(box_id)
    return box_ids


def parse_platforms(value):
    available = available_platforms()
    if value.strip().lower() == "all":
        return available

    selected = []
    for name in value.split(","):
        platform = name.strip().lower().replace(" ", "_").replace("-", "_")
        if not platform:
            continue
        if platform not in available:
            raise argparse.ArgumentTypeError(
                "unknown platform '{}' (available: {})".format(
                    name.strip(), ", ".join(available)
                )
            )
        if platform not in selected:
            selected.append(platform)
    if not selected:
        raise argparse.ArgumentTypeError("no platforms given")
    return selected


def add_platforms_argument(parser):
    parser.add_argument(
        "platforms",
        type=parse_platforms,
        help='comma-separated list of platforms, or "all" (available: {})'.format(
            ", ".join(available_platforms())
        ),
    )


def get_wishlist_box_ids(platforms):
    wishlist_box_ids = []
    for platform in platforms:
        wishlist_box_ids.extend(load_platform_box_ids(platform))
    return wishlist_box_ids
