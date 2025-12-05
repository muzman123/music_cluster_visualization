# 🎵 Mujica - Complete Setup Guide

## 📋 Prerequisites

Before starting, ensure you have:

- ✅ Python 3.10 or higher
- ✅ Node.js 18 or higher  
- ✅ npm or yarn
- ✅ 2GB+ free disk space

## 🚀 Step-by-Step Setup

### Part 1: Backend Setup (15-20 minutes)

#### 1. Navigate to Backend Directory

```bash
cd mujica/backend
```

#### 2. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

#### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

**Note**: This installs PyTorch, librosa, FastAPI, and other packages. May take 10-15 minutes.

#### 4. Verify Model File

```bash
# Check that the model exists
dir ml_models\pytorch_genre_classifier_best.pkl
```

#### 5. Start Backend Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
🚀 Starting Mujica Backend...
📊 Creating database tables...
🤖 Loading ML model...
✓ Model loaded successfully on cpu
  Test Accuracy: XX.XX%
✓ Backend ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it**: Visit http://localhost:8000/docs

---

### Part 2: Frontend Setup (10-15 minutes)

#### 1. Open New Terminal

Keep the backend running, open a **new terminal window**.

#### 2. Navigate to Frontend Directory

```bash
cd mujica/frontend
```

#### 3. Install Node Dependencies

```bash
npm install
```

**Note**: This installs React, D3.js, TailwindCSS, and other packages. May take 5-10 minutes.

#### 4. Start Development Server

```bash
npm run dev
```

**Expected output:**
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

#### 5. Open Application

Visit http://localhost:5173 in your browser!

---

## 🎯 Testing the Application

### Test 1: Upload MP3 File

1. Make sure both backend (port 8000) and frontend (port 5173) are running
2. Go to http://localhost:5173
3. Drag and drop an MP3 file from your `audios/` folder
4. Wait 3-10 seconds for processing
5. See the song appear in the decagon visualization!

### Test 2: YouTube Download

1. Copy a YouTube music video URL (e.g., https://www.youtube.com/watch?v=dQw4w9WgXcQ)
2. Click the "YouTube" tab
3. Paste the URL and click "Download & Analyze"
4. Wait 30-60 seconds for download and processing
5. See results in visualization!

### Test 3: Explore Visualization

1. **Hover** over song dots to see titles and genres
2. **Click** a song to open the details panel
3. **Zoom** using mouse wheel
4. **Pan** by dragging the visualization
5. **View stats** in the left sidebar

---

## 🎨 What You'll See

### Main Interface

```
┌─────────────────────────────────────────────────────────────┐
│  🎵 Mujica - Music Cluster Visualization                    │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Upload │           Visualization              │  Details   │
│  ────────│───────────────────────────────────── │  Panel     │
│          │         CLASSICAL                    │  (click    │
│  [File]  │            ●                         │   song)    │
│  [YT]    │           /|\                        │            │
│          │  JAZZ ●  / | \  ● COUNTRY           │            │
│  Drag &  │         /  |  \                      │            │
│  Drop    │BLUES ●─────●──────● DISCO           │            │
│  Area    │         \  |  /                      │            │
│          │  POP ●   \ | /  ● HIPHOP            │            │
│          │           \|/                        │            │
│  Stats   │         REGGAE ●                     │            │
│  ─────   │           METAL ●                    │            │
│  Songs:  │            ROCK ●                    │            │
│  XX      │                                      │            │
└─────────────────────────────────────────────────────────────┘
```

### Features

- 🎵 **Upload**: Drag & drop MP3s or paste YouTube URLs
- 🎨 **Visualization**: Interactive D3.js decagon with 10 genre vertices
- 📊 **Details**: Click any song to see full genre breakdown
- 📈 **Stats**: Real-time statistics in sidebar
- 🎯 **Accurate**: 90%+ classification accuracy

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'app'`  
**Solution**: Make sure you're in `mujica/backend` directory and venv is activated

**Problem**: `FileNotFoundError: Model file not found`  
**Solution**: Verify model file exists in `backend/ml_models/`

**Problem**: Port 8000 already in use  
**Solution**: Use different port: `uvicorn app.main:app --port 8001`

### Frontend Issues

**Problem**: `ENOENT: no such file or directory`  
**Solution**: Run `npm install` again

**Problem**: Cannot connect to API  
**Solution**: 
1. Ensure backend is running on port 8000
2. Check `.env` file has `VITE_API_URL=http://localhost:8000/api`

**Problem**: Port 5173 already in use  
**Solution**: `npm run dev -- --port 3000`

### Upload Issues

**Problem**: "Failed to upload file"  
**Solution**: 
1. Check file is valid MP3 (not M4A, WAV, etc.)
2. Check file size < 50MB
3. Check backend terminal for errors

**Problem**: "Failed to process YouTube URL"  
**Solution**:
1. Verify URL is a valid YouTube link
2. Check video isn't age-restricted or private
3. Ensure `yt-dlp` is installed (included in requirements.txt)

---

## 📁 Project Structure

```
mujica/
├── backend/                    ✅ Complete
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── api/               # Upload, songs, cluster endpoints
│   │   ├── models/            # Database models
│   │   ├── schemas/           # Pydantic schemas
│   │   └── services/          # Business logic
│   └── ml_models/             # Your trained BiLSTM model
│
└── frontend/                   ✅ Complete
    ├── src/
    │   ├── components/        # React components
    │   │   ├── Upload/        # File & YouTube upload
    │   │   ├── Visualization/ # D3.js decagon
    │   │   └── SongInfo/      # Details panel
    │   ├── services/          # API integration
    │   ├── store/             # Zustand state
    │   ├── types/             # TypeScript types
    │   ├── utils/             # Helper functions
    │   ├── App.tsx            # Main component
    │   └── main.tsx           # Entry point
    └── package.json
```

---

## 🎊 Success Checklist

After setup, you should be able to:

- ✅ Visit http://localhost:8000/docs and see API documentation
- ✅ Visit http://localhost:5173 and see the Mujica interface
- ✅ Upload an MP3 file and see it processed
- ✅ See the song appear in the decagon visualization
- ✅ Click the song to view detailed genre breakdown
- ✅ Try a YouTube URL and see it download and analyze

---

## 🚀 Next Steps

1. **Upload test files** from your `audios/` directory
2. **Try different genres** and see how they cluster
3. **Explore the visualization** - hover, click, zoom, pan
4. **Check accuracy** - does it match your expectations?
5. **Build more features** - playlist creation, similar songs, etc.

---

## 📖 Additional Documentation

- **Backend API**: See `backend/README.md`
- **Frontend**: See `frontend/README.md`
- **Project Overview**: See `README.md`
- **Current Status**: See `PROJECT_STATUS.md`

---

## 🎉 You're All Set!

Your Music Cluster Visualization application is now running!

**Backend**: http://localhost:8000  
**Frontend**: http://localhost:5173  
**API Docs**: http://localhost:8000/docs

Enjoy exploring your music with AI-powered genre classification! 🎵✨

---

## 💡 Pro Tips

1. **Performance**: First upload may be slow as model loads. Subsequent uploads are faster.
2. **YouTube**: Processing time depends on video length and download speed.
3. **Accuracy**: ML model trained on GTZAN dataset with 90%+ accuracy.
4. **Genres**: 10 genres supported - blues, classical, country, disco, hiphop, jazz, metal, pop, reggae, rock.
5. **Visualization**: Songs closer to a vertex have higher probability for that genre.

---

**Need help?** Check the troubleshooting section above or review the error messages in the terminal.