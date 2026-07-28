# 🏅 Olympics Analysis Dashboard

An interactive **Streamlit** dashboard for exploring **120 years of Olympic history** (1896–2016) — both Summer and Winter Games. Analyse medal tallies, country performance, athlete demographics, geographic medal distribution, and cross-season trends through dynamic Plotly visualizations.

---

## Features

| Tab | What it shows |
|-----|---------------|
| **Medal Tally** | Filter by year/country, stacked bar chart, CSV download |
| **Overall Analysis** | KPI cards, nations/events/athletes over time, year range slider, sport heatmap, top athletes |
| **Country-wise Analysis** | Per-country medal trends, sport strengths heatmap, top 10 athletes |
| **Athlete wise Analysis** | Age distributions, BMI analysis by sport, height vs weight, gender trends, repeat medalists, athlete name search |
| **🌍 Medal Map** | Interactive world choropleth colored by Gold/Silver/Bronze/Total |
| **⚔️ Country Comparison** | Head-to-head metrics, medal trend overlay, sport overlap, top athletes side-by-side |
| **☀️❄️ Summer vs Winter** | Season stat comparison, medal dominance chart, sport split, crossover athletes |

### Global Season Filter
Toggle between **☀️ Summer**, **❄️ Winter**, or **🏅 Both** from the sidebar — all tabs respond instantly.

## Tech Stack

- **Python 3.10+**
- **Streamlit** — interactive web UI
- **Plotly** — all charts, maps, and heatmaps
- **Pandas / NumPy** — data processing

## Data

The dashboard uses the [120 Years of Olympic History](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results) dataset from Kaggle. Download these two files and place them in the project root:

- `athlete_events.csv` — 271K athlete-event records
- `noc_regions.csv` — NOC-to-country mapping

## Quick Start

```bash
# 1. Clone the repository
git clone <repo-url>
cd olympics-analysis

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Download data files from Kaggle (link above) into this directory

# 5. Run the dashboard
streamlit run app.py
```

The dashboard will open at `http://localhost:8501`.

## Project Structure

```
├── app.py               # Streamlit UI — page layout, tabs, and chart rendering
├── helper.py            # Business logic — medal tallies, comparisons, search, BMI
├── preprocessing.py     # Data pipeline — merging, dedup, encoding (both seasons)
├── chart_utils.py       # Shared Plotly styling utilities and color palette
├── requirements.txt     # Pinned Python dependencies
├── .gitignore           # Git exclusions (data, cache, IDE files)
├── .streamlit/
│   └── config.toml      # Streamlit dark theme configuration
├── athlete_events.csv   # Raw data (not in repo — download from Kaggle)
└── noc_regions.csv      # NOC mapping (not in repo — download from Kaggle)
```

## License

This project is for educational and portfolio purposes. The dataset is provided under its original Kaggle license.
