# Mujica Frontend

React + TypeScript + Vite frontend for the Mujica music cluster visualization application.

## 🚀 Quick Start

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

The application will be available at http://localhost:5173

### Build for Production

```bash
npm run build
```

### Preview Production Build

```bash
npm run preview
```

## 📁 Project Structure

```
src/
├── components/
│   ├── Upload/
│   │   ├── FileUpload.tsx       # Drag & drop MP3 upload
│   │   └── YouTubeUpload.tsx    # YouTube URL input
│   ├── Visualization/
│   │   └── DecagonViz.tsx       # D3.js decagon visualization
│   └── SongInfo/
│       └── SongPanel.tsx        # Song details panel
├── services/
│   └── api.ts                   # API service layer
├── store/
│   └── useSongStore.ts          # Zustand state management
├── types/
│   └── index.ts                 # TypeScript type definitions
├── utils/
│   └── helpers.ts               # Utility functions
├── App.tsx                      # Main app component
├── main.tsx                     # Entry point
└── index.css                    # Global styles
```

## 🎨 Features

### ✅ Implemented

- **File Upload**: Drag & drop MP3 files with validation
- **YouTube Integration**: Download and analyze from YouTube URLs
- **D3.js Visualization**: Interactive 10-sided decagon showing genre clusters
- **Song Details**: Comprehensive genre breakdown panel
- **State Management**: Zustand for efficient state handling
- **Responsive Design**: Works on desktop and mobile
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback during processing

### 🎯 Components

#### Upload Components

- **FileUpload**: Accepts MP3 files up to 50MB
- **YouTubeUpload**: Processes YouTube music video URLs

#### Visualization

- **DecagonViz**: 
  - 10 genre vertices (blues, classical, country, disco, hiphop, jazz, metal, pop, reggae, rock)
  - Songs positioned based on genre probability weights
  - Interactive hover tooltips
  - Click to view details
  - Zoom and pan support

#### Song Information

- **SongPanel**:
  - Primary genre with confidence
  - All genre probabilities with bar charts
  - Metadata (duration, upload date, source)
  - Delete functionality

## 🛠️ Technology Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **D3.js** - Data visualization
- **TailwindCSS** - Styling
- **Zustand** - State management
- **Axios** - HTTP client
- **react-dropzone** - File upload
- **Lucide React** - Icons

## 🎨 Styling

The app uses a dark theme with:
- Slate background colors
- Blue accents for primary actions
- Genre-specific colors for visualization
- Responsive grid layout
- Custom Tailwind utilities

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000/api
```

### Tailwind Configuration

Genre colors are defined in `tailwind.config.js`:

```js
colors: {
  'genre-blues': '#4169E1',
  'genre-classical': '#DDA0DD',
  // ... etc
}
```

## 📝 Development

### Adding New Features

1. Create component in appropriate directory
2. Add types to `src/types/index.ts`
3. Update store if needed in `src/store/useSongStore.ts`
4. Add API methods to `src/services/api.ts`

### Type Safety

All components use TypeScript with strict mode enabled. Type definitions are centralized in `src/types/index.ts`.

### State Management

The app uses Zustand for state management with a single store:

```typescript
import { useSongStore } from '@/store/useSongStore';

const { songs, selectedSong, setSelectedSong } = useSongStore();
```

## 🐛 Troubleshooting

### Backend Connection Issues

Make sure the backend is running on port 8000:
```bash
cd ../backend
uvicorn app.main:app --reload
```

### TypeScript Errors

Run type checking:
```bash
npm run lint
```

### Build Issues

Clear node_modules and reinstall:
```bash
rm -rf node_modules package-lock.json
npm install
```

## 📦 Building for Production

```bash
# Build
npm run build

# Output is in dist/
# Deploy dist/ folder to Vercel, Netlify, etc.
```

## 🚀 Deployment

### Vercel (Recommended)

1. Push to GitHub
2. Import in Vercel
3. Set environment variable:
   - `VITE_API_URL`: Your backend URL
4. Deploy!

### Other Platforms

The built files in `dist/` can be deployed to any static hosting service.

---

**Happy coding!** 🎵✨