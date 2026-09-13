# ⚡ Volt & Vogue Executive Performance Dashboard

An interactive, production-ready web application built using **Streamlit**, **Pandas**, and **Plotly Express** to analyze fictional retail operational data. This project serves as an analytical proof-of-work dashboard tailored for executive corporate review.

## 🚀 Live Application
👉 **https://volt-vogue-sales-dashboard-7ms2e8pdxjyhx5rv5cthjz.streamlit.app/**

## 💡 Key Business Insights Discovered
* **Regional Satisfaction Bottleneck:** Identified that while the **West Region** drives the highest overall net revenue volume, it suffers from the lowest average customer satisfaction rating (below 2.8/5), highlighting an urgent local logistics or customer service bottleneck.
* **Macro Seasonality Trends:** Visualized distinct, predictable revenue surges during the Q3 Back-to-School window (August electronics spikes) and the Q4 Holiday rush (November/December apparel surges).

## 🛠️ Tech Stack & Key Concepts Demonstrated
* **Frontend UI Framework:** Streamlit (including sidebar layouts, data container stretching, and interactive slider filters).
* **Data Processing Memory Optimization:** Implemented `@st.cache_data` logic to cache disk reads and optimize execution speed.
* **Data Aggregation & Manipulation:** Utilized Pandas vectorization, data type parsing, and multi-variable `.groupby().agg()` methods.
* **Interactive Visualizations:** Built multi-dimensional charts (Bar color-scaling gradients, chronological line-trends, and scatter configurations) using Plotly Express.
