import streamlit as st
from pathlib import Path
import networkx as nx
import pandas as pd
from sap_o2c_graph import (
    build_graph,
    identify_broken_flows,
    node_subgraph,
    top_products_by_billing_doc,
    trace_billing_document_flow,
)

@st.cache_data(show_spinner=False)
def load_graph(data_root: str) -> nx.DiGraph:
    return build_graph(data_root)


def process_query(query: str, G: nx.Graph):
    text = query.strip().lower()
    if "highest number of billing documents" in text or "top products" in text:
        return top_products_by_billing_doc(G, top_n=20)
    if "trace" in text and "billing" in text:
        tokens = [t.strip().upper().replace("BD:", "") for t in text.split()]
        candidate = next((t for t in tokens if t.isdigit()), None)
        if not candidate:
            return {"error": "Specify a numeric billing document ID."}
        return trace_billing_document_flow(G, candidate)
    if "broken" in text or "incomplete" in text or "not billed" in text or "not delivered" in text:
        return identify_broken_flows(G, limit=200)
    return {"error": "This system is designed to answer questions related to the provided dataset only."}


def main():
    st.set_page_config(page_title="SAP O2C Explorer", layout="wide")
    st.title("SAP Order-to-Cash Graph Explorer")

    st.sidebar.header("Dataset configuration")
    BASE_DIR = Path(__file__).parent
    DEFAULT_DATA_PATH = BASE_DIR / "sap-o2c-data"

    data_root = st.sidebar.text_input(
    "Dataset root directory",
    value=str(DEFAULT_DATA_PATH))
    st.sidebar.caption("Set path where sales_order_headers etc. folders exist")
    load_graph_btn = st.sidebar.button("Load Graph")

    if not Path(data_root).exists():
        st.sidebar.error("Path not found: " + str(data_root))
        return

    if "graph" not in st.session_state or load_graph_btn:
        with st.spinner("Building graph..."):
            st.session_state.graph = load_graph(data_root)

    G = st.session_state.graph
    st.sidebar.write(f"Graph: {len(G.nodes)} nodes, {len(G.edges)} edges")

    tab1, tab2, tab3 = st.tabs(["Explorer", "Analytics", "Chat Query"])

    with tab1:
        st.header("Graph Explorer")
        node_id = st.text_input("Node ID (e.g. SO:1234, DEL:567, BD:789)")
        depth = st.slider("Depth", 1, 3, 1)
        if node_id:
            if node_id in G:
                subG = node_subgraph(G, node_id, depth)
                st.write(f"Node subgraph: {len(subG.nodes)} nodes, {len(subG.edges)} edges")
                st.dataframe(pd.DataFrame([{"node": n, **d} for n, d in subG.nodes(data=True)]))
                st.dataframe(pd.DataFrame([{"from": u, "to": v, **d} for u, v, d in subG.edges(data=True)]))
            else:
                st.warning("Node not found: " + node_id)

    with tab2:
        st.header("Analytics")
        if st.button("Top products by billing doc count"):
            top = top_products_by_billing_doc(G, top_n=30)
            df = pd.DataFrame(top, columns=["product", "billing_document_count"])
            st.bar_chart(df.set_index("product"))
            st.dataframe(df)

        if st.button("Identify broken flows"):
            st.json(identify_broken_flows(G, limit=200))

        billing_doc_id = st.text_input("Billing Document to trace")
        if st.button("Trace Billing Document") and billing_doc_id.strip():
            st.json(trace_billing_document_flow(G, billing_doc_id.strip()))

    with tab3:
        st.header("Chat Query")
        q = st.text_input("Ask a dataset question", value="Which products are associated with the highest number of billing documents?")
        if st.button("Run query"):
            result = process_query(q, G)
            if isinstance(result, list):
                st.dataframe(pd.DataFrame(result, columns=["entity", "count"]))
            else:
                st.json(result)

if __name__ == "__main__":
    main()
