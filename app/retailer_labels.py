"""Public display labels for Cinderhaven's trade partners.

The data keeps the real names (chain_name, retailer_id, cluster_id) and
every computation runs on them. Anything rendered (hero, cluster
callout, grid, charts, filter dropdown, Excel export) maps through here
so a real retailer or distributor name never sits beside a Cinderhaven
dollar figure. Source: reference/retailer_display_labels.json, vendored
from cinderhaven-data-platform by scripts/refresh_canonical.py.

Names not in the map (a client's own retailers in client mode) pass
through unchanged.
"""

import json
from pathlib import Path

_PATH = Path(__file__).resolve().parent.parent / "reference" / "retailer_display_labels.json"


def _load():
    # Fail loudly: a missing map would otherwise fall back to the real
    # names on a public page.
    raw = json.loads(_PATH.read_text(encoding="utf-8"))
    by_name, by_id = {}, {}
    for group in ("retailers", "distributors"):
        for partner_id, entry in raw[group].items():
            by_name[entry["name"]] = entry["label"]
            by_id[partner_id] = entry["label"]
    return by_name, by_id


_BY_NAME, _BY_ID = _load()


def label_lower(name):
    """Label for mid-sentence use ("the conventional grocer's ...")."""
    return _BY_NAME.get(name, name)


def label(name):
    """Capitalized label for table, legend and chart entries and
    sentence starts ("Conventional grocer")."""
    text = label_lower(name)
    if not isinstance(text, str) or not text:
        return text
    return text[0].upper() + text[1:]


def store_label(store_id):
    """Store number without the partner prefix: "RET-KROGER-S0021"
    shows as "S0021" (the Retailer column carries the label)."""
    if isinstance(store_id, str):
        for partner_id in _BY_ID:
            if store_id.startswith(partner_id + "-"):
                return store_id[len(partner_id) + 1:]
    return store_id


def cluster_label(cluster_id):
    """Display form of a "RETAILER_ID|region" cluster id."""
    if not isinstance(cluster_id, str) or "|" not in cluster_id:
        return cluster_id
    partner_id, region = cluster_id.split("|", 1)
    text = _BY_ID.get(partner_id, partner_id)
    return f"{text[0].upper() + text[1:]} · {region}"
