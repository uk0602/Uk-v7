# 🔱 King Kashmiri: 1xBet Crash Monitoring System

Real-time monitoring system for 1xBet Crash game with interactive dashboard, high-speed WebSocket scraping, and complete Docker containerization. Developed by **uk0602**.

[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)

---

## ✨ King Kashmiri Features

### 🎯 Real-time Scraper
- **Persistent Engine**: High-speed WebSocket connection to 1xBet.
- **Auto-Sync**: Instant data capture and storage in **King Kashmiri DB**.
- **Self-Healing**: Automatic reconnection logic if the server drops the link.

### 📊 Professional Dashboard
- **Live Metrics**: Real-time tracking of mean, median, and volatility.
- **Advanced Charts**: Interactive history, distribution, and pattern analysis.
- **Export Ready**: Download your collected crash data in CSV format.

### 🐳 Docker Architecture
- **Isolated Services**: All components (DB, Scraper, UI) run in dedicated containers.
- **Branded Containers**: Managed under the `king_kashmiri_` prefix.
- **Instant Deployment**: Launch the entire system with a single command.

---

## 🏗️ Installation & Setup

### 1. Clone the repository
```bash
git clone [https://github.com/uk0602/King-Kashmiri-Crash.git](https://github.com/uk0602/King-Kashmiri-Crash.git)
cd King-Kashmiri-Crash
