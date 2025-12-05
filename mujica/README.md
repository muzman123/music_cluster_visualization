# 🎵 Mujica - Music Cluster Visualization

An interactive web application that visualizes music clustering based on AI genre classification. Upload MP3 files or YouTube URLs to see songs positioned in a decagon based on their genre probabilities.

## 🌟 Features

- **AI Genre Classification**: BiLSTM neural network with attention mechanism
- **Interactive Decagon Visualization**: D3.js-powered 10-sided polygon showing genre clusters
- **Dual Upload Methods**: Support for both MP3 files and YouTube URLs
- **Real-time Processing**: Fast audio feature extraction and prediction
- **Beautiful UI**: Modern React interface with Tailwind CSS
- **RESTful API**: FastAPI backend with automatic documentation

## 🏗️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **PyTorch** - Deep learning framework for the BiLSTM model
- **librosa** - Audio feature extraction
- **SQLAlchemy** - Database ORM
- **yt-dlp** - YouTube audio downloading

### Frontend
- **React 18** + **TypeScript** - UI framework
- **Vite** - Build tool
- **D3.js** - Data visualization
- **TailwindCSS** - Styling
- **Zustand** - State management
- **Axios** - HTTP client

## 📊 Model Architecture

The genre classifier uses a Configurable BiLSTM with Attention:
- **Input**: 58 audio features (MFCCs, spectral features, tempo, etc.)
- **Architecture**: 3-layer BiLSTM with attention mechanism
- **Output**: 10 genre probabilities (blues, classical, country, disco, hiphop, jazz, metal, pop, reggae, rock)
- **Training Accuracy**: ~90%+ on GTZAN dataset

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- npm or yarn

### Backend Setup

```bash
# Navigate to backend
cd soundscape/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will be available at http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Frontend Setup

```bash
# Navigate to frontend
cd soundscape/frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at http://localhost:5173

## 📁 Project Structure

```
soundscape/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   ├── models/           # Database models
│   │   ├── schemas/          # Pydantic schemas
│   │   ├── services/         # Business logic
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── ml_models/            # Trained PyTorch models
│   ├── uploads/              # Temporary audio storage
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── components/       # React components
│   │   ├── services/         # API services
│   │   ├── store/            # State management
│   │   ├── types/            # TypeScript types
│   │   └── utils/            # Utilities
│   └── package.json
│
└── README.md
```

## 🎨 Decagon Visualization

Each song is positioned in a 10-sided polygon based on its genre probabilities:

```
         CLASSICAL
             ●
            /|\
   JAZZ ●  / | \  ● COUNTRY
          /  |  \
BLUES ●─────●─────●──── DISCO ●
          \  |  /
   POP ●   \ | /   ● HIPHOP
            \|/
         REGGAE ●
             |
          METAL ●
             |
          ROCK ●
```

## 🔧 API Endpoints

### Upload
- `POST /api/upload/mp3` - Upload MP3 file
- `POST /api/upload/youtube` - Process YouTube URL

### Songs
- `GET /api/songs` - Get all songs (paginated)
- `GET /api/songs/{id}` - Get specific song
- `DELETE /api/songs/{id}` - Delete song

### Visualization
- `GET /api/cluster-data` - Get all data for visualization
- `GET /api/health` - Health check

## 🎯 Genre Colors

- **Blues**: Royal Blue (#4169E1)
- **Classical**: Plum (#DDA0DD)
- **Country**: Chocolate (#D2691E)
- **Disco**: Deep Pink (#FF1493)
- **Hip-hop**: Orange Red (#FF4500)
- **Jazz**: Gold (#FFD700)
- **Metal**: Dark Slate Gray (#2F4F4F)
- **Pop**: Hot Pink (#FF69B4)
- **Reggae**: Lime Green (#32CD32)
- **Rock**: Dark Red (#8B0000)

## 📝 Usage Example

1. **Upload a song**: Drag and drop an MP3 file or paste a YouTube URL
2. **Wait for processing**: The system extracts audio features and predicts genres
3. **View results**: The song appears in the decagon visualization
4. **Explore**: Click on songs to see detailed genre breakdowns

## 🛠️ Development

### Backend
```bash
# Run with auto-reload
uvicorn app.main:app --reload

# Check API docs
open http://localhost:8000/docs
```

### Frontend
```bash
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 📦 Deployment

### Backend (Railway/Render)
1. Connect repository
2. Set environment variables
3. Deploy

### Frontend (Vercel)
1. Connect repository
2. Set build command: `npm run build`
3. Set output directory: `dist`
4. Deploy

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- GTZAN Dataset for training data
- librosa for audio processing
- PyTorch for the ML framework
- FastAPI and React communities

---

Built with ❤️ using AI-powered genre classification