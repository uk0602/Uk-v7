# 🔱 King Kashmiri: 1xBet Crash Monitoring System

Real-time monitoring system for 1xBet Crash game with interactive dashboard, high-speed WebSocket scraping, and complete Docker containerization.

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

---

## ✨ Features

### 🎯 🔱 King Kashmiri Real-time Scraper
- **Persistent Connection**: WebSocket connection to 1xBet with auto-reconnection.
- **Instant Storage**: Automatic collection of each crash into **King Kashmiri DB**.
- **Handshake Logic**: Optimized for real-time data flow with zero lag.

### 📊 Analytics Dashboard (Streamlit)
- **Live Stats**: Average, median, volatility, and distribution metrics.
- **Dynamic Charts**: Interactive visual history of all game crashes.
- **Data Control**: CSV export and auto-refresh configuration.

### 🐳 Docker Infrastructure
- **Microservices**: Fully orchestrated services (DB, Scraper, Dashboard).
- **Branded Containers**: All services prefixed with `king_kashmiri_` for easy management.
- **Persistence**: Volumes included to ensure your data is safe across restarts.

---

## 🏗️ Quick Installation (Docker)

### 1. Clone the repository
```bash
git clone [https://github.com/uk0602/King-Kashmiri-Crash.git](https://github.com/uk0602/King-Kashmiri-Crash.git)
cd King-Kashmiri-Crash
