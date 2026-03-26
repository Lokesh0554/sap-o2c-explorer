import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

import networkx as nx


def _load_jsonl(path: Path):
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            yield json.loads(line)


def build_graph(data_root: str) -> nx.DiGraph:
    data_root = Path(data_root)
    G = nx.DiGraph()

    # 1. Sales orders
    for path in sorted((data_root / "sales_order_headers").glob("*.jsonl")):
        for row in _load_jsonl(path):
            order = row.get("salesOrder")
            if not order:
                continue
            node = f"SO:{order}"
            G.add_node(node, type="sales_order", **row)
            sold_to = row.get("soldToParty")
            if sold_to:
                cust = f"CUST:{sold_to}"
                G.add_node(cust, type="customer", soldToParty=sold_to)
                G.add_edge(node, cust, rel="sold_to")

    # 2. Sales order items
    for path in sorted((data_root / "sales_order_items").glob("*.jsonl")):
        for row in _load_jsonl(path):
            order = row.get("salesOrder")
            item = row.get("salesOrderItem")
            material = row.get("material")
            if not order or not item:
                continue
            soi = f"SOI:{order}-{item}"
            so = f"SO:{order}"
            G.add_node(soi, type="sales_order_item", **row)
            G.add_edge(so, soi, rel="has_item")
            if material:
                mat = f"MAT:{material}"
                G.add_node(mat, type="material", material=material)
                G.add_edge(soi, mat, rel="material")
            plant = row.get("productionPlant")
            if plant:
                plant_n = f"PLANT:{plant}"
                G.add_node(plant_n, type="plant", plant=plant)
                G.add_edge(soi, plant_n, rel="production_plant")

    # 3. Outbound delivery headers
    for path in sorted((data_root / "outbound_delivery_headers").glob("*.jsonl")):
        for row in _load_jsonl(path):
            delivery = row.get("deliveryDocument")
            if not delivery:
                continue
            dnode = f"DEL:{delivery}"
            G.add_node(dnode, type="delivery", **row)
            shipping = row.get("shippingPoint")
            if shipping:
                sp = f"SHIPPING_POINT:{shipping}"
                G.add_node(sp, type="shipping_point", shippingPoint=shipping)
                G.add_edge(dnode, sp, rel="shipping_point")

    # 4. Outbound delivery items
    for path in sorted((data_root / "outbound_delivery_items").glob("*.jsonl")):
        for row in _load_jsonl(path):
            delivery = row.get("deliveryDocument")
            item = row.get("deliveryDocumentItem")
            ref_so = row.get("referenceSdDocument")
            ref_so_item = row.get("referenceSdDocumentItem")
            plant = row.get("plant")
            if not delivery or not item:
                continue
            di = f"DELI:{delivery}-{item}"
            dnode = f"DEL:{delivery}"
            G.add_node(di, type="delivery_item", **row)
            G.add_edge(dnode, di, rel="has_item")
            if zone := row.get("referenceSdDocument"):
                so_item_key = f"SOI:{zone}-{(row.get('referenceSdDocumentItem') or '').lstrip('0')}"
                if so_item_key in G:
                    G.add_edge(di, so_item_key, rel="fulfills")
                else:
                    base_so = f"SO:{zone}"
                    if base_so in G:
                        G.add_edge(di, base_so, rel="fulfills")
            if plant:
                plant_n = f"PLANT:{plant}"
                G.add_node(plant_n, type="plant", plant=plant)
                G.add_edge(di, plant_n, rel="plant")

    # 5. Billing document headers
    for path in sorted((data_root / "billing_document_headers").glob("*.jsonl")):
        for row in _load_jsonl(path):
            bd = row.get("billingDocument")
            if not bd:
                continue
            bnode = f"BD:{bd}"
            G.add_node(bnode, type="billing_document", **row)
            cust = row.get("soldToParty")
            if cust:
                cust_n = f"CUST:{cust}"
                G.add_node(cust_n, type="customer", soldToParty=cust)
                G.add_edge(bnode, cust_n, rel="sold_to")

    # 6. Billing document items
    for path in sorted((data_root / "billing_document_items").glob("*.jsonl")):
        for row in _load_jsonl(path):
            bd = row.get("billingDocument")
            item = row.get("billingDocumentItem")
            ref_del = row.get("referenceSdDocument")
            ref_del_item = row.get("referenceSdDocumentItem")
            mat = row.get("material")
            if not bd or not item:
                continue
            bdi = f"BDI:{bd}-{item}"
            bnode = f"BD:{bd}"
            G.add_node(bdi, type="billing_document_item", **row)
            G.add_edge(bnode, bdi, rel="has_item")
            if mat:
                mat_n = f"MAT:{mat}"
                G.add_node(mat_n, type="material", material=mat)
                G.add_edge(bdi, mat_n, rel="material")
            if ref_del and ref_del_item:
                de_item = f"DELI:{ref_del}-{ref_del_item.zfill(5)}"
                if de_item in G:
                    G.add_edge(bdi, de_item, rel="references_delivery_item")
                else:
                    de_item2 = f"DELI:{ref_del}-{ref_del_item}"
                    if de_item2 in G:
                        G.add_edge(bdi, de_item2, rel="references_delivery_item")
            if ref_del:
                dnode = f"DEL:{ref_del}"
                if dnode in G:
                    G.add_edge(bdi, dnode, rel="references_delivery")

    return G


def node_subgraph(G: nx.Graph, node_id: str, depth: int = 1) -> nx.Graph:
    if node_id not in G:
        raise KeyError(f"Node {node_id} not in graph")
    nodes = {node_id}
    frontier = {node_id}
    for _ in range(depth):
        neighbors = set()
        for n in frontier:
            neighbors |= set(G.predecessors(n))
            neighbors |= set(G.successors(n))
        nodes |= neighbors
        frontier = neighbors
    return G.subgraph(nodes).copy()


def top_products_by_billing_doc(G: nx.Graph, top_n: int = 20) -> List[Tuple[str,int]]:
    counts: Dict[str, set] = {}
    for node, data in G.nodes(data=True):
        if data.get("type") != "billing_document_item":
            continue
        bd_ids = {edge for edge in G.predecessors(node) if edge.startswith("BD:")}
        mats = [n for n in G.successors(node) if G.nodes[n].get("type") == "material"]
        for mat in mats:
            counts.setdefault(mat, set()).update(bd_ids)

    product_counts = [(mat, len(bds)) for mat, bds in counts.items()]
    product_counts.sort(key=lambda t: t[1], reverse=True)
    return product_counts[:top_n]


def trace_billing_document_flow(G: nx.Graph, billing_document: str) -> Dict[str, Any]:
    bnode = f"BD:{billing_document}"
    if bnode not in G:
        return {"error": "Billing document not found"}
    flow = {"billing_document": billing_document, "sales_orders": set(), "deliveries": set(), "materials": set()}

    for bdi in G.successors(bnode):
        if G.nodes[bdi].get("type") != "billing_document_item":
            continue
        for mat in G.successors(bdi):
            if G.nodes[mat].get("type") == "material":
                flow["materials"].add(mat)
        for dele in G.successors(bdi):
            if G.nodes[dele].get("type") == "delivery_item":
                for delv in G.predecessors(dele):
                    if G.nodes[delv].get("type") == "delivery":
                        flow["deliveries"].add(delv)
                        for so_item in G.successors(dele):
                            if G.nodes[so_item].get("type") == "sales_order_item":
                                for so in G.predecessors(so_item):
                                    if G.nodes[so].get("type") == "sales_order":
                                        flow["sales_orders"].add(so)

    flow["sales_orders"] = sorted(flow["sales_orders"])
    flow["deliveries"] = sorted(flow["deliveries"])
    flow["materials"] = sorted(flow["materials"])
    return flow


def identify_broken_flows(G: nx.Graph, limit: int = 50) -> Dict[str, List[str]]:
    result = {"delivered_not_billed": [], "billed_not_delivered": []}
    for so in [n for n, d in G.nodes(data=True) if d.get("type") == "sales_order"]:
        deliveries = set()
        billings = set()

        for soi in G.successors(so):
            if G.nodes[soi].get("type") != "sales_order_item":
                continue
            for deliv in [p for p in G.predecessors(soi) if G.nodes[p].get("type") == "delivery_item"]:
                deliveries.update(set(G.predecessors(deliv)))
            for deli in [p for p in G.predecessors(soi) if G.nodes[p].get("type") == "delivery_item"]:
                for bd_item in set(G.predecessors(deli)):
                    if G.nodes[bd_item].get("type") == "billing_document_item":
                        billings.update(set(G.predecessors(bd_item)))

        if deliveries and not billings:
            result["delivered_not_billed"].append(so)
        if billings and not deliveries:
            result["billed_not_delivered"].append(so)

        if len(result["delivered_not_billed"]) > limit and len(result["billed_not_delivered"]) > limit:
            break
    return result
