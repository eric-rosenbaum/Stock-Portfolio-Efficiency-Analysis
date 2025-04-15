# 📈 Portfolio Optimizer

A web app built with Streamlit to analyze and visualize portfolio efficiency using Modern Portfolio Theory.

## Features

- Dynamic portfolio input (edit tickers and weights)
- Donut chart showing portfolio allocation
- Efficient frontier chart with user portfolio plotted
- Wrnings and auto-normalization of weights
- Real-time data fetching and caching from local DB/API


## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/)
- [Plotly](https://plotly.com/)
- [pandas](https://pandas.pydata.org/)
- [streamlit-plotly-events](https://github.com/stefanrmmr/streamlit-plotly-events)

## 📦 Installation

```bash
git clone https://github.com/YOUR_USERNAME/portfolio-optimizer.git
cd portfolio-optimizer
pip install -r requirements.txt
streamlit run app.py
