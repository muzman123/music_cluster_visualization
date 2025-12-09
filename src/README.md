# 🎵 Mujica - Music Cluster Visualization

<div align="center">

**AI-Powered Music Genre Classification & Interactive Visualization**

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green.svg)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-blue.svg)](https://www.typescriptlang.org/)

**90%+ Classification Accuracy • 10 Genres • Real-Time Updates**

</div>

---

## 📖 What is Mujica?

Mujica is an interactive web application that visualizes your music collection in a beautiful **decagon (10-sided polygon)** based on AI-powered genre classification. Upload MP3 files or paste YouTube URLs to see songs positioned according to their genre probabilities.

### 🎯 Key Innovation

Unlike simple genre classifiers, Mujica analyzes **10 segments** across your entire song and averages the results for superior accuracy. Each song is then positioned in a visual decagon where proximity to vertices indicates genre strength.

---

## ✨ Features

### 🤖 Advanced AI Classification
- **BiLSTM Neural Network** with attention mechanism
- **Multi-Segment Analysis** - Analyzes 10 evenly-spaced 3-second segments
- **58 Audio Features** - MFCCs, spectral features, tempo, harmony, energy
- **90%+ Accuracy** - Trained on GTZAN music dataset
- **10 Genres** - Blues, Classical, Country, Disco, Hip-Hop, Jazz, Metal, Pop, Reggae, Rock

### 🎨 Interactive Visualization
- **D3.js Decagon** - Beautiful polygon with genre vertices
- **Real-Time Updates** - Songs appear instantly after processing
- **Interactive Controls** - Hover tooltips, click details, zoom, pan
- **Color-Coded Genres** - Each genre has distinctive color
- **Smart Positioning** - Songs placed based on probability weights

### 📤 Flexible Upload Options
- **Drag & Drop** - Simple file upload with validation
- **YouTube Integration** - Paste any YouTube music URL
- **Batch Processing** - Upload multiple songs
- **Progress Feedback** - Real-time upload and processing status

### 📊 Detailed Analysis
- **Primary Genre** - Top prediction with confidence %
- **Full Breakdown** - All 10 genre probabilities with charts
- **Metadata Display** - Duration, source, upload date
- **Song Management** - Delete songs, view history

---

## 🚀 Quick Start

### Prerequisites

Ensure you have installed:
- **Python 3.10+** ([Download](https://www.python.org/downloads/))
- **Node.js 18+** ([Download](https://nodejs.org/))
- **npm** (comes with Node.js)

### 1️⃣ Backend Setup (15 minutes)

```bash
# Navigate to backend
cd src/backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**✅ Backend Running**: http://localhost:8000  
**📚 API Docs**: http://localhost:8000/docs

### 2️⃣ Frontend Setup (10 minutes)

```bash
# Open NEW terminal (keep backend running)
# Navigate to frontend
cd src/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**✅ Frontend Running**: http://localhost:5173

### 3️⃣ Test It!

1. Open http://localhost:5173 in your browser
2. Drag & drop an MP3 file (or try files from `../audios/`)
3. Wait ~5-15 seconds for processing
4. **Watch the song appear automatically in the decagon!** ✨
5. Click the song node to see detailed genre breakdown

---

## 🎬 How It Works

### Upload Flow

```
1. Upload MP3 or YouTube URL
   ↓
2. Backend receives file
   ↓
3. Audio divided into 10 segments
   ↓
4. Each segment analyzed:
   • Extract 58 features
   • Run through BiLSTM
   • Get probabilities
   ↓
5. Average all predictions
   ↓
6. Calculate decagon position
   ↓
7. Store in database
   ↓
8. Return to frontend
   ↓
9. Node appears automatically! ✨
```

### Multi-Segment Analysis

For a 3-minute song:
- **Segment 1**: 0:00-0:03 (intro)
- **Segment 2**: 0:20-0:23
- **Segment 3**: 0:40-0:43
- ... (evenly spaced)
- **Segment 10**: 2:57-3:00 (outro)

Each segment gets independent classification, then results are averaged for the final prediction.

---

## 🏗️ Architecture

### Tech Stack

**Backend**
- **FastAPI** - Modern Python web framework
- **PyTorch** - Deep learning (BiLSTM model)
- **librosa** - Audio feature extraction
- **SQLAlchemy** - Database ORM
- **yt-dlp** - YouTube downloader
- **SQLite** - Database storage

**Frontend**
- **React 18** + **TypeScript** - UI framework
- **Vite** - Lightning-fast build tool
- **D3.js v7** - Data visualization
- **TailwindCSS** - Utility-first CSS
- **Zustand** - State management
- **Axios** - HTTP client
- **react-dropzone** - File upload

### Project Structure

```
src/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── main.py            # FastAPI app entry
│   │   ├── config.py          # Configuration
│   │   ├── database.py        # Database setup
│   │   ├── api/               # API endpoints
│   │   │   ├── upload.py     # MP3/YouTube upload
│   │   │   ├── songs.py      # Song CRUD
│   │   │   └── cluster.py    # Visualization data
│   │   ├── models/           # SQLAlchemy models
│   │   │   └── song.py
│   │   ├── schemas/          # Pydantic schemas
│   │   │   └── song.py
│   │   └── services/         # Business logic
│   │       ├── audio_processor.py    # Feature extraction
│   │       ├── predictor.py          # ML inference
│   │       ├── cluster_calculator.py # Positioning
│   │       └── youtube_downloader.py # YouTube
│   ├── ml_models/            # Trained models
│   │   ├── model_classes.py  # PyTorch architecture
│   │   └── pytorch_genre_classifier_best.pkl
│   ├── uploads/              # Uploaded files
│   └── requirements.txt      # Python dependencies
│
└── frontend/                  # React Frontend
    ├── src/
    │   ├── components/
    │   │   ├── Upload/
    │   │   │   ├── FileUpload.tsx      # Drag & drop
    │   │   │   └── YouTubeUpload.tsx   # YouTube input
    │   │   ├── Visualization/
    │   │   │   └── DecagonViz.tsx      # D3.js decagon
    │   │   └── SongInfo/
    │   │       └── SongPanel.tsx       # Details panel
    │   ├── services/
    │   │   └── api.ts                  # API layer
    │   ├── store/
    │   │   └── useSongStore.ts         # State management
    │   ├── types/
    │   │   └── index.ts                # TypeScript types
    │   ├── utils/
    │   │   └── helpers.ts              # Utilities
    │   ├── App.tsx                     # Main component
    │   ├── main.tsx                    # Entry point
    │   └── index.css                   # Styles
    └── package.json            # Dependencies
```

---

## 🎨 Genre Visualization

### Decagon Vertices

| Genre | Color | Position |
|-------|-------|----------|
| 🔵 Blues | Royal Blue `#4169E1` | West-Northwest |
| 💜 Classical | Plum `#DDA0DD` | North |
| 🟤 Country | Chocolate `#D2691E` | Northeast |
| 💗 Disco | Deep Pink `#FF1493` | East |
| 🔴 Hip-Hop | Orange Red `#FF4500` | East-Southeast |
| 💛 Jazz | Gold `#FFD700` | West |
| ⚫ Metal | Dark Slate Gray `#2F4F4F` | South |
| 💖 Pop | Hot Pink `#FF69B4` | Southwest |
| 💚 Reggae | Lime Green `#32CD32` | South-Southeast |
| 🟥 Rock | Dark Red `#8B0000` | South |

### Positioning Algorithm

Songs are positioned using weighted calculation:

```python
song_x = Σ(probability[genre] × vertex_x[genre]) × 0.8
song_y = Σ(probability[genre] × vertex_y[genre]) × 0.8
```

This means:
- **100% one genre** → Song at that vertex
- **50/50 split** → Song between those vertices
- **Mixed genres** → Song in center area

---

## 🔌 API Reference

### Base URL
```
http://localhost:8000/api
```

### Endpoints

#### Upload MP3
```http
POST /api/upload/mp3
Content-Type: multipart/form-data

Request Body:
  file: <MP3 file>

Response: Song object with predictions
```

#### Upload YouTube
```http
POST /api/upload/youtube
Content-Type: application/json

Request Body:
  {
    "url": "https://youtube.com/watch?v=..."
  }

Response: Song object with predictions
```

#### Get All Songs
```http
GET /api/songs?limit=100&offset=0&genre=rock

Response:
  {
    "songs": [...],
    "total": 42,
    "limit": 100,
    "offset": 0
  }
```

#### Get Visualization Data
```http
GET /api/cluster-data

Response:
  {
    "vertices": [...],  // 10 genre vertices
    "songs": [...]      // All songs with positions
  }
```

📚 **Full API Documentation**: http://localhost:8000/docs

---

## 🧪 Testing

### Sample Files

Try the included samples in `../audios/`:
- `beethoven.mp3` → Should classify as **Classical**
- `khaled.mp3` → Should classify as **Hip-Hop**
- `laufey.mp3` → Should show **Classical/Jazz** mix
- `skipmarley.mp3` → Should classify as **Reggae**

### Test Scenarios

1. **Short song** (<3s) → Single segment analysis
2. **Long song** (>3s) → 10 segment analysis
3. **YouTube** → Download + analyze
4. **Multiple uploads** → All appear in visualization
5. **Delete song** → Removed from visualization

---

## 📊 Performance

| Metric | Value |
|--------|-------|
| **Model Accuracy** | 90%+ |
| **Supported Genres** | 10 |
| **Audio Features** | 58 |
| **Segments Analyzed** | 10 |
| **Max File Size** | 50MB |
| **Processing Time (MP3)** | 5-15 seconds |
| **Processing Time (YouTube)** | 35-70 seconds |
| **Visualization Render** | <1 second |
| **Supported Formats** | MP3, WAV |

---

## 🛠️ Development

### Backend Development

```bash
cd src/backend

# Run with auto-reload (development)
uvicorn app.main:app --reload

# Run on different port
uvicorn app.main:app --port 8001

# Check API documentation
open http://localhost:8000/docs
```

### Frontend Development

```bash
cd src/frontend

# Development server (hot reload)
npm run dev

# Type checking
npm run lint

# Build for production
npm run build

# Preview production build
npm run preview
```

---

## 🐛 Troubleshooting

### Backend Issues

**❌ `ModuleNotFoundError: No module named 'app'`**  
✅ Solution: Activate virtual environment and ensure you're in `src/backend` directory

**❌ `FileNotFoundError: Model file not found`**  
✅ Solution: Verify `ml_models/pytorch_genre_classifier_best.pkl` exists

**❌ Port 8000 already in use**  
✅ Solution: Use different port: `uvicorn app.main:app --port 8001`

### Frontend Issues

**❌ Cannot connect to API**  
✅ Solution: 
1. Ensure backend is running on port 8000
2. Check `frontend/.env` has `VITE_API_URL=http://localhost:8000/api`

**❌ Visualization doesn't update**  
✅ Solution: Restart backend server to load latest code

**❌ npm install fails**  
✅ Solution: Delete `node_modules/` and `package-lock.json`, then run `npm install` again

---

## 🚀 Deployment

### Backend (Railway/Render)

1. Create account on [Railway](https://railway.app) or [Render](https://render.com)
2. Connect your GitHub repository
3. Set environment variables:
   ```
   DATABASE_URL=<your-postgres-url>
   ```
4. Deploy from `src/backend` directory

### Frontend (Vercel/Netlify)

1. Create account on [Vercel](https://vercel.com) or [Netlify](https://netlify.com)
2. Connect your GitHub repository
3. Configure:
   - **Build directory**: `src/frontend`
   - **Build command**: `npm run build`
   - **Output directory**: `dist`
   - **Environment variable**: `VITE_API_URL=<your-backend-url>/api`
4. Deploy!

---

## 📚 Documentation

- **[Backend README](backend/README.md)** - API documentation
- **[Frontend README](frontend/README.md)** - Component guide
- **API Docs** - Auto-generated at `/docs`

---

## 🎓 Technical Details

### Audio Feature Extraction (58 Features)

| Category | Features | Description |
|----------|----------|-------------|
| **Temporal** | Length, Tempo | Time-based characteristics |
| **Spectral** | Centroid, Bandwidth, Rolloff | Frequency distribution |
| **Energy** | RMS, Zero-Crossing Rate | Signal energy |
| **Harmonic** | Harmony, Percussive | Harmonic/percussive separation |
| **Timbre** | 20 MFCCs (mean + variance) | Sound quality |
| **Chroma** | Chroma STFT | Pitch class distribution |

### Model Training

- **Dataset**: GTZAN Music Genre Dataset
- **Samples**: ~10,000 audio clips (1000 per genre)
- **Architecture**: 3-layer Bidirectional LSTM with Attention
- **Optimizer**: Adam with learning rate scheduling
- **Regularization**: Dropout, Batch Normalization, L2
- **Test Accuracy**: 90%+

---

## 🎯 Example Use Cases

1. **Music Library Analysis**
   - Upload your entire library
   - See genre distribution
   - Find genre outliers

2. **Playlist Curation**
   - Visualize playlist diversity
   - Find songs with similar genre profiles
   - Create balanced genre mixes

3. **Music Discovery**
   - Explore genre boundaries
   - Find cross-genre songs
   - Discover unexpected classifications

4. **Educational**
   - Learn genre characteristics
   - Understand feature importance
   - Study music classification

---

## 🤝 Contributing

Contributions are welcome! Feel free to:

- 🐛 Report bugs
- 💡 Suggest features  
- 🔧 Submit pull requests
- 📖 Improve documentation
- ⭐ Star the project

---

## 📄 License

This project is open source and available under the **MIT License**.

---

## 🙏 Acknowledgments

- **GTZAN Dataset** - Music genre training data
- **librosa** - Excellent audio processing library
- **PyTorch** - Powerful deep learning framework
- **FastAPI** - Modern web framework
- **React & D3.js** - Amazing visualization tools

---

## 🌟 Project Stats

- **Total Files**: 40+ source files
- **Lines of Code**: 3,000+
- **Languages**: Python, TypeScript, CSS
- **Frameworks**: FastAPI, React, D3.js
- **Model Parameters**: ~2.5 million
- **Supported Genres**: 10
- **Accuracy**: 90%+

---

<div align="center">

## 🎵 Start Exploring Your Music!

**Backend**: http://localhost:8000  
**Frontend**: http://localhost:5173  
**API Docs**: http://localhost:8000/docs

Built with ❤️ using AI-Powered Genre Classification

**[⬆ Back to Top](#-mujica---music-cluster-visualization)**

</div>