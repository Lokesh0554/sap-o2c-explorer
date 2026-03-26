# SAP Order-to-Cash (O2C) Graph Explorer

An interactive Streamlit application for analyzing SAP Order-to-Cash business process data using graph theory and network analysis.

## 🎯 Overview

This application provides tools to explore, analyze, and visualize complex relationships within SAP O2C business processes including:
- Sales Orders → Deliveries → Billing → Payments
- Product flow and material tracking
- Customer relationships and sales patterns
- Identification of broken or incomplete workflows

## 📋 Features

### 1. **Graph Explorer Tab**
- Search for entities by ID (e.g., `SO:1000001`, `BD:500001`, `CUST:ACME`)
- Explore relationships up to 3 levels deep
- View all connected nodes and edges with complete data
- Real-time graph statistics

### 2. **Analytics Tab**
- Top products by billing document count
- Identify broken/incomplete order-to-cash flows
- Trace individual billing documents through the entire process
- Visualization and detailed reporting

### 3. **Chat Query Tab**
- Natural language queries about the dataset
- Predefined question templates
- Support for complex business questions

## 🚀 Quick Start


### Requirements
- Python 3.8+
- pip

### Installation

#### 1. Clone Repository
```bash
git clone https://github.com/Lokesh0554/sap-o2c-explorer.git
cd sap-o2c-explorer
```

#### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 4. Run Application
```bash
streamlit run sap_o2c_app.py
```

The app will launch at `http://localhost:8501`

## 📁 Project Structure

```
sap-o2c-explorer/
├── sap_o2c_app.py              # Main Streamlit application
├── sap_o2c_graph.py            # Graph building and analysis logic
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .gitignore                  # Git ignore rules
└── [data directories]/         # JSONL data files
    ├── sales_order_headers/
    ├── sales_order_items/
    ├── sales_order_schedule_lines/
    ├── outbound_delivery_headers/
    ├── outbound_delivery_items/
    ├── billing_document_headers/
    ├── billing_document_items/
    ├── billing_document_cancellations/
    ├── business_partners/
    ├── business_partner_addresses/
    ├── customer_company_assignments/
    ├── customer_sales_area_assignments/
    ├── payments_accounts_receivable/
    ├── journal_entry_items_accounts_receivable/
    ├── products/
    ├── product_descriptions/
    ├── product_plants/
    ├── product_storage_locations/
    └── plants/
```

## 🔧 Technologies

- **Streamlit** - Interactive web framework
- **NetworkX** - Graph analysis and visualization
- **Pandas** - Data manipulation
- **Python 3.12** - Core language

## 📊 Supported Node Types

| Prefix | Type | Description |
|--------|------|-------------|
| `SO:` | Sales Order | Master sales order |
| `SOI:` | Sales Order Item | Line item |
| `DOC:` | Delivery Document | Outbound delivery |
| `BD:` | Billing Document | Invoice |
| `CUST:` | Customer | Business partner |
| `MAT:` | Material | Product/SKU |
| `AR:` | Accounts Receivable | Payment |

## 📈 Usage Examples

### Example: Trace a Billing Document
1. Go to **Analytics** tab
2. Enter billing document ID: `BD:1000001`
3. Click "Trace Billing Document"
4. View complete flow from sales order → delivery → billing → payment

### Example: Find Top Products
1. Go to **Analytics** tab
2. Click "Top products by billing doc count"
3. View bar chart and data table

### Example: Identify Issues
1. Go to **Analytics** tab
2. Click "Identify broken flows"
3. View list of incomplete or problematic orders

## 🔍 Data Format

Data is stored in JSONL format (one JSON object per line):

```json
{"salesOrder":"1000001","soldToParty":"CUST001","createdAt":"2025-11-19","amount":5000.00}
```

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| "Path not found" error | Ensure data directories exist in the specified path |
| Slow performance | For large datasets, consider filtering by date/business unit |
| Memory errors | Process data in batches or use a larger server |
| Streamlit not found | Run `pip install -r requirements.txt` |

## 📦 Dependencies

```
streamlit==1.25.0
networkx==3.4
pandas==2.2.3
```

## 🚀 Performance Tips

- Initial graph loading may take time for large datasets
- Use specific node IDs for faster searches
- Limit relationship depth for complex networks
- Streamlit caches the graph for fast subsequent interactions

## 📝 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit changes with clear messages
4. Push and open a Pull Request

## 📞 Support

For issues or questions:
- Check existing [GitHub Issues](https://github.com/Lokesh0554/sap-o2c-explorer/issues)
- Create a new issue with detailed description

## 🎓 Use Cases

- **Process Auditing** - Trace complete O2C workflows
- **Revenue Analysis** - Identify top products and patterns
- **Issue Investigation** - Find broken/incomplete flows
- **Data Validation** - Verify data integrity
- **Performance Monitoring** - Analyze cycle times

---

**Version:** 1.0.0  
**Last Updated:** March 2026  
**Repository:** [sap-o2c-explorer](https://github.com/Lokesh0554/sap-o2c-explorer)
successfully deployed:(https://sapo2capppy-hnyrhndlrnyumpe6wj3ssk.streamlit.app)
