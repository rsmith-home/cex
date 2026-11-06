import html
from datetime import datetime
from pathlib import Path

# Field selection for each output. A spec is a dict of {field_name: sub_spec}:
#   None        -> include the field's whole value
#   dict        -> include only the listed fields of the value; for lists the
#                  spec is applied to every item, and the "*" key applies the
#                  spec to every value of a dict (e.g. wishlistBoxes, which is
#                  keyed by box name)
# Fields that are missing from an entry are skipped. A spec of None for a whole
# output includes every field.
BOX_FIELDS = {
    "boxName": None,
    "categoryName": None,
    "sellPrice": None,
    "previousPrice": None,
    "lastPriceUpdatedDate": None,
    "collectionQuantity": None,
    "outOfStock": None,
    "ecomQuantityOnHand": None,
    "nearestStoreNames": None,
}

DEFAULT_FIELDS = {
    "best_stores": {
        "storeName": None,
        "regionName": None,
        "wishlistBoxes": {"*": BOX_FIELDS},
    },
    "rarest_boxes": BOX_FIELDS,
    "out_of_stock_boxes": BOX_FIELDS,
}

# Collapsed-row label for each output, formatted from the unfiltered entry.
SUMMARY_FORMATS = {
    "best_stores": "{storeName}",
    "rarest_boxes": "{boxName} (in stock: {collectionQuantity})",
    "out_of_stock_boxes": "{boxName}",
}

TITLES = {
    "best_stores": "Best stores",
    "rarest_boxes": "Rarest boxes",
    "out_of_stock_boxes": "Out of stock boxes",
    "wishlist": "Wishlist",
}

HOME_TITLE = "CeX wishlist stock"

# Pages in navigation order, as (file stem, nav label).
NAV_PAGES = [
    ("index", "Home"),
    ("best_stores", TITLES["best_stores"]),
    ("rarest_boxes", TITLES["rarest_boxes"]),
    ("out_of_stock_boxes", TITLES["out_of_stock_boxes"]),
    ("wishlist", TITLES["wishlist"]),
]

_STYLE = """
body { font-family: monospace; font-size: 14px; margin: 0; }
nav { position: fixed; top: 0; left: 0; bottom: 0; width: 14em; box-sizing: border-box;
  padding: 1.5em 1em; background: #f4f4f8; border-right: 1px solid #ccc; overflow-y: auto; }
nav a { display: block; padding: 0.4em 0.6em; color: #222; text-decoration: none; }
nav a:hover { background: #dde; }
nav a.current { background: #cce; font-weight: bold; }
main { margin-left: 14em; padding: 1.5em; }
details { margin-left: 1.5em; }
details > summary { cursor: pointer; }
details > summary:hover { background: #eef; }
.row { margin-left: 1.5em; }
.key { color: #881391; }
.str { color: #1a1aa6; }
.num { color: #1c00cf; }
.meta { color: #888; }
.generated { color: #666; margin-bottom: 1em; }
.toolbar { margin-bottom: 1em; }
main > details { margin-left: 0; }
"""

_SCRIPT = """
function setAll(open) {
  document.querySelectorAll("details").forEach(d => d.open = open);
}
"""


def _filter(value, spec):
    if spec is None:
        return value
    if isinstance(value, list):
        return [_filter(item, spec) for item in value]
    if isinstance(value, dict):
        if "*" in spec:
            return {k: _filter(v, spec["*"]) for k, v in value.items()}
        return {k: _filter(value[k], sub) for k, sub in spec.items() if k in value}
    return value


def _scalar(value):
    text = html.escape(repr(value))
    if isinstance(value, str):
        return f'<span class="str">{text}</span>'
    return f'<span class="num">{text}</span>'


def _label(key):
    return f'<span class="key">{html.escape(str(key))}</span>'


def _node(key, value):
    if isinstance(value, dict):
        children = value.items()
        meta = f"{{{len(value)}}}"
    elif isinstance(value, (list, tuple)):
        children = enumerate(value)
        meta = f"[{len(value)}]"
    else:
        return f'<div class="row">{_label(key)}: {_scalar(value)}</div>'

    body = "".join(_node(k, v) for k, v in children)
    return (
        f"<details><summary>{_label(key)} "
        f'<span class="meta">{meta}</span></summary>{body}</details>'
    )


def _entry_summary(name, entry, index):
    template = SUMMARY_FORMATS.get(name)
    if template:
        try:
            return template.format(**entry)
        except (KeyError, IndexError):
            pass
    return str(index)


def _page(stem, title, generated, content, toolbar=True):
    links = "".join(
        f'<a href="{page}.html" class="{"current" if page == stem else ""}">'
        f"{html.escape(label)}</a>"
        for page, label in NAV_PAGES
    )
    buttons = (
        '<div class="toolbar">'
        "<button onclick='setAll(true)'>Expand all</button> "
        "<button onclick='setAll(false)'>Collapse all</button></div>"
        if toolbar
        else ""
    )
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title><style>{_STYLE}</style></head><body>"
        f"<nav>{links}</nav><main>"
        f"<h1>{html.escape(title)}</h1>"
        f'<div class="generated">Generated: {html.escape(generated)}</div>'
        f"{buttons}{content}</main><script>{_SCRIPT}</script></body></html>"
    )


def _render_page(name, entries, spec, generated):
    """entries is a list of (id, dict) pairs, as produced by main.py."""
    items = []
    for index, (entry_id, entry) in enumerate(entries):
        label = _entry_summary(name, entry, entry_id)
        fields = _filter(entry, spec)
        body = "".join(_node(k, v) for k, v in fields.items())
        items.append(
            f"<details><summary>{html.escape(label)}</summary>{body}</details>"
        )

    title = f"{TITLES.get(name, name)} ({len(entries)})"
    return _page(name, title, generated, "".join(items))


def _render_wishlist_page(wishlist, boxes, generated):
    """wishlist maps platform -> box ids; boxes maps box id -> box details."""
    items = []
    total = 0
    for platform, box_ids in wishlist.items():
        titles = sorted(
            (
                boxes[box_id]["boxName"] if box_id in boxes else box_id
                for box_id in box_ids
            ),
            key=str.casefold,
        )
        total += len(titles)
        body = "".join(f'<div class="row">{html.escape(t)}</div>' for t in titles)
        items.append(
            f"<details><summary>{html.escape(platform)} "
            f'<span class="meta">[{len(titles)}]</span></summary>{body}</details>'
        )

    title = f"{TITLES['wishlist']} ({total})"
    return _page("wishlist", title, generated, "".join(items))


def _render_home_page(generated):
    return _page("index", HOME_TITLE, generated, "", toolbar=False)


def add_html_argument(parser):
    parser.add_argument(
        "--html-dir",
        help="write the results as HTML files into this directory",
    )


def write_html_outputs(
    output_dir,
    best_stores,
    rarest_boxes,
    out_of_stock_boxes,
    wishlist,
    boxes,
    fields=None,
):
    """Write one HTML file per page into output_dir, printing each path.

    wishlist maps platform name -> list of box ids; boxes maps box id -> box
    details, used to look up the title of each wishlist entry (the box id is
    shown for boxes that could not be fetched).

    Does nothing if output_dir is None. fields overrides DEFAULT_FIELDS, per
    output name, e.g. {"rarest_boxes": {"boxName": None}}. Use None for an
    output to include all of its fields.
    """
    if output_dir is None:
        return

    specs = {**DEFAULT_FIELDS, **(fields or {})}
    outputs = {
        "best_stores": best_stores,
        "rarest_boxes": rarest_boxes,
        "out_of_stock_boxes": out_of_stock_boxes,
    }

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    generated = datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    pages = {"index": _render_home_page(generated)}
    for name, entries in outputs.items():
        pages[name] = _render_page(name, entries, specs[name], generated)
    pages["wishlist"] = _render_wishlist_page(wishlist, boxes, generated)

    for name, content in pages.items():
        path = output_dir / f"{name}.html"
        path.write_text(content, encoding="utf-8")
        print(f"Wrote {path}")
