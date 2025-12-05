# 🚀 SoundScape Setup Guide

Complete step-by-step guide to get SoundScape running on your machine.

## ✅ Prerequisites Checklist

Before starting, ensure you have:

- [ ] Python 3.10 or higher installed
- [ ] Node.js 18 or higher installed
- [ ] npm or yarn package manager
- [ ] Git (optional, for version control)
- [ ] At least 2GB free disk space

## 📋 Step-by-Step Setup

### Step 1: Backend Setup (15-20 minutes)

#### 1.1 Navigate to Backend Directory
```bash
cd c:/Users/muzam/mujica/soundscape/backend
```

#### 1.2 Create Virtual Environment
```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

#### 1.3 Install Python Dependencies
```bash
pip install -r requirements.txt
```

**Note**: This may take 10-15 minutes as it installs PyTorch and other large packages.

#### 1.4 Verify Model File
Check that the model file exists:
```bash
# Should see: pytorch_genre_classifier_best.pkl
dir ml_models\
```

If missing, copy from your training directory:
```bash
copy ..\..\..\models\classification_model\pytorch_genre_classifier_best.pkl ml_models\
```

#### 1.5 Test Backend
```bash
# Start the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
🚀 Starting SoundScape Backend...
📊 Creating database tables...
🤖 Loading ML model...
✓ Model loaded successfully on cpu
  Test Accuracy: XX.XX%
✓ Backend ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Test it**: Open http://localhost:8000/docs in your browser to see the API documentation.

Press `Ctrl+C` to stop the server when done testing.

### Step 2: Frontend Setup (10-15 minutes)

#### 2.1 Navigate to Frontend Directory
```bash
# Open a NEW terminal (keep backend running in the first one)
cd c:/Users/muzam/mujica/soundscape/frontend
```

#### 2.2 Install Node Dependencies
```bash
npm install
```

**Note**: This may take 5-10 minutes.

#### 2.3 Verify Environment File
Check that `.env` file exists with:
```
VITE_API_URL=http://localhost:8000/api
```

#### 2.4 Start Development Server
```bash
npm run dev
```

You should see:
```
  VITE v5.0.8  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h to show help
```

**Test it**: Open http://localhost:5173 in your browser.

## 🎯 Quick Test Workflow

### Test 1: Upload an MP3 File

1. Make sure both backend (port 8000) and frontend (port 5173) are running
2. Go to http://localhost:5173
3. Drag and drop an MP3 file (or use the sample from your audios folder)
4. Wait for processing (3-10 seconds)
5. See the song appear in the visualization!

### Test 2: YouTube URL

1. Copy any YouTube music video URL
2. Paste it into the YouTube input field
3. Click "Download & Analyze"
4. Wait for download and processing
5. See results!

### Test 3: API Direct Test

Use the Swagger UI at http://localhost:8000/docs:

1. Expand `POST /api/upload/mp3`
2. Click "Try it out"
3. Choose a file
4. Click "Execute"
5. See the JSON response with genre predictions!

## 🐛 Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError: No module named 'app'`
**Solution**: Make sure you're in the `backend` directory and venv is activated

**Problem**: `FileNotFoundError: Model file not found`
**Solution**: Copy the model file to `backend/ml_models/`

**Problem**: Port 8000 already in use
**Solution**: Use a different port: `uvicorn app.main:app --port 8001`

### Frontend Issues

**Problem**: `ENOENT: no such file or directory`
**Solution**: Run `npm install` again

**Problem**: Cannot connect to API
**Solution**: Ensure backend is running on port 8000

**Problem**: Port 5173 already in use
**Solution**: Kill the process or use `npm run dev -- --port 3000`

## 📝 Development Commands

### Backend
```bash
# Start with auto-reload (development)
uvicorn app.main:app --reload

# Start without reload (production-like)
uvicorn app.main:app

# Run on different port
uvicorn app.main:app --port 8001

# Make publicly accessible
uvicorn app.main:app --host 0.0.0.0
```

### Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run lint
```

## 🚀 Production Deployment

### Backend (Railway/Render)

1. Create account on Railway.app or Render.com
2. Connect your GitHub repository
3. Set environment variables:
   ```
   DATABASE_URL=<your-postgres-url>
   ```
4. Deploy!

### Frontend (Vercel)

1. Create account on Vercel.com
2. Import your GitHub repository
3. Configure:
   - Build command: `npm run build`
   - Output directory: `dist`
   - Environment variable: `VITE_API_URL=<your-backend-url>/api`
4. Deploy!

## 📊 Project Status

✅ **Completed**:
- [x] Backend API with FastAPI
- [x] Database models and schemas
- [x] Audio feature extraction
- [x] ML model integration
- [x] Decagon position calculation
- [x] MP3 upload endpoint
- [x] YouTube download integration
- [x] Frontend configuration files

🚧 **To Complete** (for full UI):
- [ ] React components (upload, visualization, song panel)
- [ ] D3.js decagon visualization
- [ ] State management implementation
- [ ] API integration in frontend
- [ ] Styling and polish

## 💡 Next Steps

1. **Try the API**: Use the Swagger docs at `/docs` to test all endpoints
2. **Upload test files**: Use files from your `audios/` directory
3. **Build frontend**: Follow the frontend development guide
4. **Customize**: Adjust colors, add features, improve UI

## 🆘 Need Help?

- Check the API docs: http://localhost:8000/docs
- Review the code comments
- Test individual components
- Use the debugging tools

---

Good luck building SoundScape! 🎵✨