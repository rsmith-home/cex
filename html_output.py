import html
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
}

_STYLE = """
body { font-family: monospace; font-size: 14px; margin: 1.5em; }
details { margin-left: 1.5em; }
details > summary { cursor: pointer; }
details > summary:hover { background: #eef; }
.row { margin-left: 1.5em; }
.key { color: #881391; }
.str { color: #1a1aa6; }
.num { color: #1c00cf; }
.meta { color: #888; }
.toolbar { margin-bottom: 1em; }
body > details { margin-left: 0; }
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


def _render_page(name, entries, spec):
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
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title><style>{_STYLE}</style></head><body>"
        f"<h1>{html.escape(title)}</h1>"
        '<div class="toolbar">'
        "<button onclick='setAll(true)'>Expand all</button> "
        "<button onclick='setAll(false)'>Collapse all</button></div>"
        f"{''.join(items)}<script>{_SCRIPT}</script></body></html>"
    )


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
    fields=None,
):
    """Write one HTML file per output into output_dir, printing each path.

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

    for name, entries in outputs.items():
        path = output_dir / f"{name}.html"
        path.write_text(_render_page(name, entries, specs[name]), encoding="utf-8")
        print(f"Wrote {path}")
