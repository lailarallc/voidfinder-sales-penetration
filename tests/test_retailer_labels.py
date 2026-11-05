"""Display-label mapping (2026-11-05 rule): rendered surfaces show the
shared label, never the real trade-partner name beside a dollar figure."""

import pandas as pd

from app import retailer_labels
from app.views.exceptions import _cluster_callout


def test_labels_come_from_the_vendored_map():
    assert retailer_labels.label("Kroger") == "Conventional grocer"
    assert retailer_labels.label_lower("Kroger") == "conventional grocer"
    assert retailer_labels.label("Whole Foods") == "Natural grocer"
    assert retailer_labels.label("Regional Group") == "Regional Group"
    assert retailer_labels.label("UNFI") == "Distributor A"


def test_unknown_names_pass_through_for_client_mode():
    assert retailer_labels.label("Acme Foods") == "Acme Foods"
    assert retailer_labels.store_label("S0001") == "S0001"
    assert retailer_labels.cluster_label(None) is None


def test_store_and_cluster_ids_drop_the_partner_name():
    assert retailer_labels.store_label("RET-KROGER-S0021") == "S0021"
    assert retailer_labels.cluster_label("RET-KROGER|Southeast") == (
        "Conventional grocer · Southeast"
    )


def _text(component):
    if component is None:
        return ""
    if isinstance(component, str):
        return component
    if isinstance(component, (list, tuple)):
        return "".join(_text(c) for c in component)
    return _text(getattr(component, "children", None))


def test_cluster_callout_uses_the_label():
    shown = pd.DataFrame(
        {
            "cluster_id": ["RET-KROGER|Southeast"] * 2,
            "void_dollars": [100.0, 200.0],
            "sku": ["A", "B"],
            "store_id": ["RET-KROGER-S0001", "RET-KROGER-S0002"],
            "chain_name": ["Kroger", "Kroger"],
            "region": ["Southeast", "Southeast"],
        }
    )
    text = _text(_cluster_callout(shown))
    assert text.startswith("Cluster detected: Conventional grocer · Southeast has 2")
    assert "Kroger" not in text
