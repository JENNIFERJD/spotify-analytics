# 🎵 Spotify Analytics Dashboard

A business intelligence dashboard analyzing Spotify listening patterns to derive actionable music strategy insights.

## 📊 Project Overview

This project analyzes 4,831 Spotify tracks (1,686 high popularity, 3,145 low popularity) across 35 genres to answer key business questions:

- What audio features drive song popularity?
- Which genres perform best?
- How do successful artists differ from others?
- What decisions should music strategists make?

## 🛠️ Technologies Used

- **Python 3.12**
- **Streamlit** - Interactive web dashboard
- **Pandas** - Data manipulation and analysis
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical computations

## 📁 Project Structure
```
spotify-analytics/
├── data/
│   ├── high_popularity.csv
│   └── low_popularity.csv
├── src/
│   ├── data_loader.py      # Data loading utilities
│   └── app.py              # Main Streamlit application
├── outputs/
├── requirements.txt
└── README.md
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/spotify-analytics.git
cd spotify-analytics
```

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Run the dashboard
```bash
streamlit run src/app.py
```

4. Open your browser to `http://localhost:8501`

### Data Setup

**Note:** The dataset files are not included in this repository for security and size reasons.

To run this project:

1. Download the **Spotify Music Dataset** from Kaggle:
   - [Spotify Dataset on Kaggle](https://www.kaggle.com/datasets)
   - You'll need: `high_popularity.csv` and `low_popularity.csv`

2. Create a `data/` folder in the project root (if it doesn't exist):
```bash
   mkdir -p data
```

3. Place both CSV files in the `data/` folder:
```
   spotify-analytics/
   └── data/
       ├── high_popularity.csv
       └── low_popularity.csv
```

4. Now you can run the dashboard!

## 📈 Dashboard Features

### 1. Overview
- Dataset summary and key metrics
- Genre distribution visualization
- High vs low popularity comparison

### 2. Popularity Analysis
- Audio feature comparison (9 features)
- Top differentiating factors
- Statistical insights

### 3. Genre Insights
- Genre performance analysis
- Energy and danceability positioning
- Strategy recommendations by genre

### 4. Audio Features
- Interactive feature explorer
- Distribution and box plot comparisons
- Correlation analysis with popularity

### 5. Artist Analysis
- Most prolific artists
- Average popularity rankings
- Artist success rates

### 6. Business Recommendations
- Data-driven strategic insights
- Short, mid, and long-term action plans
- Feature optimization strategies

## 📊 Key Findings

- **Average Popularity**: High (75.8) vs Low (43.5)
- **Total Genres**: 35 unique genres analyzed
- **Unique Artists**: 3,390 artists in dataset
- **Top differentiating features**: Identified through comparative analysis

## 🎯 Business Value

This dashboard enables music strategists to:
- Make data-driven playlist curation decisions
- Identify promising artists and tracks
- Optimize audio features for maximum engagement
- Develop genre-specific strategies
- Plan resource allocation effectively

## 📚 Data Source

Dataset: Spotify Music Dataset from Kaggle
- High popularity songs: 1,686 tracks
- Low popularity songs: 3,145 tracks
- Features: 29 columns including audio characteristics

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

Your Name - [Your GitHub Profile]

## 🙏 Acknowledgments

- Kaggle for providing the Spotify dataset
- Streamlit for the amazing dashboard framework
- Plotly for interactive visualizations 