# WebScraper 

**Intelligent Competitor Asset Extraction & Analysis System**

[![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B?logo=streamlit)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> Scan any competitor website and extract visual assets, color palettes, typography, and AI-powered brand personality insights in seconds.

---

##  Features

- ** Smart Asset Extraction** - Scrapes images, fonts, and design elements from any website
- ** Battle Mode** - Side-by-side competitor comparison with visual reports
- ** AI Vibe Analysis** - Gemini-powered brand personality scoring  
- ** Color Palette Generator** - Dominant colors with hex codes
- ** PDF & CSV Reports** - Export professional analysis documents
- ** Scan History** - Auto-saves last 20 scans with localStorage
- ** 3D Asset Orbit** - Interactive visual gallery
- ** Mood Board Generator** - Pinterest-style inspiration boards

---

##  Screenshots

*Coming soon - Run the app to see it in action!*

---

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/AssetFlow.git
cd AssetFlow
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up API Key (Optional but Recommended)
```bash
# Create .env file
echo "GEMINI_API_KEY=your-api-key-here" > .env
```

**Get a free API key:** [Google AI Studio](https://makersuite.google.com/app/apikey)

> **Note:** AssetFlow works without an API key, but AI features (Vibe Check, Personality Analysis) will be disabled.

### 4. Run the App
```bash
streamlit run src/app.py
```

The app will open at `http://localhost:8501`

---

##  Usage

### Normal Scan Mode
1. Enter a competitor URL (e.g., `https://nike.com`)
2. Click **"SCRAPE SCAN"**
3. View results: color palettes, fonts, assets, AI insights
4. Export as **PDF** or **CSV**

### Battle Mode
1. Enable **"BATTLE MODE"** in sidebar
2. Enter two competitor URLs
3. Click **"BATTLE SCAN"**
4. Compare side-by-side analysis
5. Download comparison PDF

---

##  Tech Stack

| Category | Technology |
|----------|-----------|
| **Framework** | Streamlit |
| **Web Scraping** | BeautifulSoup4, Requests |
| **AI Analysis** | Google Gemini API |
| **PDF Generation** | ReportLab |
| **Image Processing** | Pillow |
| **Styling** | Custom CSS |

---

##  Project Structure

```
AssetFlow/
├── src/
│   ├── app.py                 # Main Streamlit app
│   ├── scraper.py             # Web scraping engine
│   ├── analysis.py            # AI-powered analysis
│   ├── export_engine.py       # PDF/CSV export system
│   ├── history_manager.py     # Scan history management
│   ├── moodboard.py           # Mood board generator
│   └── orbit_component.py     # 3D asset orbit
├── assets/                    # Downloaded images (gitignored)
├── requirements.txt           # Python dependencies
├── .env.example               # Environment variables template
├── README.md                  # You are here!
└── DEPLOYMENT.md              # Deployment guide
```

---

##  Configuration

### Environment Variables

Create a `.env` file:

```bash
GEMINI_API_KEY=your-google-gemini-api-key
```

### Scan Settings

- **FAST Mode:** Scans 3 pages (quick preview)
- **DEEP Mode:** Scans 15 pages (comprehensive analysis)

Configure in the sidebar before scanning.

---

##  Deployment

AssetFlow can be deployed on:

- **Streamlit Cloud** (Recommended, Free) - [Guide](DEPLOYMENT.md#streamlit-cloud)
- **Heroku** - [Guide](DEPLOYMENT.md#heroku)
- **Docker** - [Guide](DEPLOYMENT.md#docker)

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions.

---

##  Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

##  License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file formdetails.

---

##  Acknowledgments

- Google Gemini for AI analysis
- Streamlit for the amazing framework
- The open-source community

---

##  Support

Having issues? Have ideas?

-  Email: your@email.com
-  [Report a Bug](https://github.com/yourusername/AssetFlow/issues)
-  [Request a Feature](https://github.com/yourusername/AssetFlow/issues)

---

**Made with ❤️ by Sarth**

 **Star this repo if AssetFlow helped you!**
