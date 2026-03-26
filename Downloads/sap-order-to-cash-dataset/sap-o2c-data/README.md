# SAP Order-to-Cash (O2C) Graph Explorer

A powerful Streamlit-based interactive visualization and analysis tool for SAP Order-to-Cash business process data. This application uses graph theory to analyze and trace complex relationships between sales orders, deliveries, billing documents, and more.

## 🎯 Features

- **Interactive Graph Explorer**: Visualize and explore relationships between business entities (sales orders, customers, deliveries, billing documents)
- **Analytics Dashboard**: Identify top products by billing document count, discover broken/incomplete flows
- **Billing Document Tracing**: Trace the complete flow of any billing document through the order-to-cash process
- **Natural Language Queries**: Ask questions about your dataset in plain English (e.g., "Which products have the highest number of billing documents?")
- **Deep Relationship Analysis**: Navigate relationships up to 3 levels deep with full data inspection

## 🏗️ Project Structure

```
sap-o2c-data/
├── sap_o2c_app.py           # Main Streamlit application
├── sap_o2c_graph.py         # Graph building and analysis logic
├── requirements.txt         # Python dependencies
├── README.md               # This file
└── [data directories]/     # JSONL data files organized by entity type
    ├── sales_order_headers/
    ├── sales_order_items/
    ├── outbound_delivery_headers/
    ├── outbound_delivery_items/
    ├── billing_document_headers/
    ├── billing_document_items/
    ├── billing_document_cancellations/
    ├── business_partners/
    ├── payments_accounts_receivable/
    ├── journal_entry_items_accounts_receivable/
    ├── products/
    ├── product_descriptions/
    ├── product_plants/
    ├── product_storage_locations/
    ├── plants/
    ├── customer_company_assignments/
    └── customer_sales_area_assignments/
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/sap-o2c-explorer.git
   cd sap-o2c-explorer
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start the Streamlit app:
```bash
streamlit run sap_o2c_app.py
```

The application will open in your browser at `http://localhost:8501`

## 📊 Data Format

All data is stored in JSONL (JSON Lines) format. Each line represents a single record:

**Example Sales Order Header Record:**
```json
{
  "salesOrder": "1000001",
  "soldToParty": "CUST001",
  "createdAt": "2025-11-19",
  "amount": 5000.00,
  ...
}
```

## 🎨 Usage Guide

### Tab 1: Graph Explorer
- Enter a node ID (e.g., `SO:123456`, `BD:789`, `CUST:456`)
- Select the relationship depth (1-3 levels)
- View all connected nodes and their relationships
- Inspect complete node and edge data

### Tab 2: Analytics
- **Top Products**: View the 30 most-billed products with a bar chart
- **Broken Flows**: Identify orders that are incomplete or not fully billed/delivered
- **Trace Billing**: Track a specific billing document through the entire O2C process

### Tab 3: Chat Query
- Ask natural language questions about your dataset
- Supported queries:
  - "Which products have the highest number of billing documents?"
  - "Trace billing document BD:123456"
  - "Show me broken/incomplete flows"
  - "What orders are not delivered?"

## 🔧 Node Types

The graph contains the following entity types:

| Node ID Prefix | Entity Type | Description |
|---|---|---|
| `SO:` | Sales Order | Master sales order record |
| `SOI:` | Sales Order Item | Individual line item in a sales order |
| `DOC:` | Delivery Document | Outbound delivery record |
| `BD:` | Billing Document | Invoice/billing record |
| `CUST:` | Customer | Business partner/customer |
| `MAT:` | Material | Product/SKU |
| `AR:` | Accounts Receivable | Payment/AR posting |

## 📈 Graph Statistics

The application displays real-time graph statistics in the sidebar:
- Total number of nodes in the graph
- Total number of relationships (edges)
- Edge relationship types and frequencies

## 🔍 Data Analysis Features

### Relationship Types

- **sold_to**: Customer-Sales Order relationship
- **has_item**: Sales Order-Item relationship
- **material**: Item-Product relationship
- **delivered**: Sales Order to Delivery
- **billed**: Delivery to Billing Document
- **paid**: Billing Document to Payment

### Broken Flow Detection

The analytics identify incomplete order-to-cash flows:
- Orders not delivered
- Orders partially billed
- Billing documents without payments
- Cancellations and reversals

## 🛠️ Technologies Used

- **Streamlit**: Interactive web framework for data applications
- **NetworkX**: Python library for graph analysis
- **Pandas**: Data manipulation and analysis
- **Python 3.12+**

## 📋 Requirements

See `requirements.txt`:
```
streamlit==1.25.0
networkx==3.4
pandas==2.2.3
```

## 🚦 Performance Tips

- **Large Datasets**: For datasets with millions of records, consider filtering by date range or business unit
- **Graph Building**: Initial graph construction loads all JSONL files—this may take a few minutes for large datasets
- **Caching**: Streamlit automatically caches the graph after first load, making subsequent interactions fast

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🎓 Use Cases

- **Process Auditing**: Trace orders through the complete O2C process
- **Revenue Analysis**: Identify top products and billing patterns
- **Issue Investigation**: Find broken flows and incomplete orders
- **Performance Monitoring**: Analyze delivery and billing cycle times
- **Data Validation**: Verify data integrity and completeness

## ⚠️ Known Limitations

- Query processing is rule-based (limited to predefined patterns)
- Large graphs (1M+ nodes) may require optimization
- Real-time updates not supported (restart app to reload data)

## 🐛 Troubleshooting

**Issue: "Path not found" error**
- Ensure the data directory path contains all required JSONL folders

**Issue: Slow performance**
- Reduce dataset scope by filtering by date/business unit
- Increase Streamlit cache settings

**Issue: Memory errors**
- Process data in batches or use a server with more RAM

## 📞 Support

For issues or questions, please:
1. Check existing GitHub issues
2. Create a new issue with detailed description
3. Include error messages and data sample if applicable

## 🗺️ Roadmap

- [ ] Real-time data streaming support
- [ ] Advanced NLP for query processing
- [ ] Export graph visualizations to multiple formats
- [ ] Multi-tenant support
- [ ] REST API integration
- [ ] Custom aggregation and reporting

---

**Created:** November 2025  
**Last Updated:** March 2026  
**Version:** 1.0.0
