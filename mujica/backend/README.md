# SoundScape Backend

FastAPI backend for music genre classification and cluster visualization.

## Setup

1. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run the server:**
```bash
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

4. **Access the API:**
- API: http://localhost:8000
- Swagger Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## API Endpoints

### Upload
- `POST /api/upload/mp3` - Upload MP3 file
- `POST /api/upload/youtube` - Process YouTube URL

### Songs
- `GET /api/songs` - Get all songs (paginated)
- `GET /api/songs/{id}` - Get specific song
- `DELETE /api/songs/{id}` - Delete song

### Cluster
- `GET /api/cluster-data` - Get visualization data
- `GET /api/health` - Health check

## Project Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── models/       # Database models
│   ├── schemas/      # Pydantic schemas
│   ├── services/     # Business logic
│   ├── config.py     # Configuration
│   ├── database.py   # Database setup
│   └── main.py       # FastAPI app
├── ml_models/        # ML model files
├── uploads/          # Uploaded audio files
└── requirements.txt
```

## Features

- ✅ MP3 file upload and processing
- ✅ YouTube audio download and processing
- ✅ Genre classification using BiLSTM model
- ✅ Decagon position calculation
- ✅ SQLite database storage
- ✅ RESTful API with FastAPI
- ✅ Auto-generated API documentation