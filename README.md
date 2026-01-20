# 🚕 Urban Mobility Analytics & GenAI Insights Platform

A production-ready, AI-powered analytics platform for NYC taxi trip data with interactive visualizations and natural language querying.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red)
![Groq](https://img.shields.io/badge/AI-Groq%20Llama3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **📊 Executive Dashboard**: Real-time KPIs, revenue trends, demand analysis
- **🗺️ Geospatial Intelligence**: 4 interactive map types (heatmap, scatter, time-based, revenue)
- **🤖 AI Assistant**: Natural language queries powered by Groq AI (free tier)
- **📋 Data Explorer**: Interactive data table with statistics and visualizations
- **⚡ Scalable ETL**: PySpark pipeline for 100GB+ datasets

## 🏗️ Architecture

![Architecture Diagram](Arch_Diagram.png)

## 📁 Project Structure

```
├── code/
│   ├── app.py                    # Streamlit UI (main entry point)
│   ├── mobility_analytics.py     # Python OOP data processing
│   ├── database_manager.py       # SQLite database layer
│   ├── genai_assistant.py        # Multi-provider AI client
│   ├── spark_etl.py             # PySpark ETL for large datasets
│   ├── analytics_demo.py        # Demo script without UI
│   ├── sql_queries.sql          # Analytics SQL queries
│   └── requirements.txt          # Python dependencies
├── Project-documentation.md      # Detailed Technical Documentation
├── README.md                     # Project Overview
└── .env                          # API keys (not committed)
```

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/HrsFlex/gen-ai-assignment.git
cd gen-ai-assignment
```

### 2. Install Dependencies
```bash
pip install -r code/requirements.txt
```

### 3. Configure API Keys
Create `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_key_here
```
Get free key at: https://console.groq.com

### 4. Add Dataset
Place `yellow_tripdata_2016-01.csv` in the `code/` directory or update path.

### 5. Launch Application
```bash
cd code
streamlit run app.py
```
Access at: http://localhost:8501

## 📊 KPI Visualizations

| Metric | Description |
|--------|-------------|
| Total Revenue | Sum of all fare amounts |
| Total Trips | Count of taxi rides |
| Avg Fare | Average fare per trip |
| Avg Distance | Average trip distance |
| Peak Hours | 8-9 AM, 5-7 PM |
| Busiest Zone | Midtown Manhattan |

## 🤖 AI Assistant Capabilities

Ask questions in natural language:
- "What's the revenue trend?"
- "When is peak demand?"
- "Which zones are busiest?"
- "Show average fare breakdown"

The AI generates SQL queries and provides data-driven insights.

## ⚡ Scalability

For large datasets (100GB+), use the PySpark ETL:
```bash
spark-submit spark_etl.py
```

Features:
- Distributed processing
- Parquet output (compressed)
- Partitioned by day
- Schema validation

## 🛠️ Tech Stack

- **UI**: Streamlit, Plotly, PyDeck
- **Data**: Pandas, NumPy, SQLite
- **AI**: Groq (Llama 3.3 70B), OpenAI-compatible
- **ETL**: PySpark
- **Design**: Custom CSS, Glassmorphism

## 📸 Screenshots

*Dashboard with KPIs and charts*
*Geospatial heatmap visualization*
*AI Assistant conversation*

## 📄 License

MIT License - Free for educational and commercial use.

## 👨‍💻 Author

Harsh Kumar
- GitHub: [@HrsFlex](https://github.com/HrsFlex)
