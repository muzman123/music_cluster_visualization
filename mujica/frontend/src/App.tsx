/**
 * Main App Component
 */

import { useEffect, useState } from 'react';
import { Music2, AlertCircle, Upload as UploadIcon, Youtube } from 'lucide-react';
import { FileUpload } from './components/Upload/FileUpload';
import { YouTubeUpload } from './components/Upload/YouTubeUpload';
import { DecagonViz } from './components/Visualization/DecagonViz';
import { SongPanel } from './components/SongInfo/SongPanel';
import { useSongStore } from './store/useSongStore';
import apiService from './services/api';

function App() {
  const [activeTab, setActiveTab] = useState<'file' | 'youtube'>('file');
  const { clusterData, setClusterData, error, clearError, setLoading, setError } = useSongStore();

  // Load cluster data on mount
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    setLoading(true);
    try {
      const data = await apiService.getClusterData();
      setClusterData(data);
    } catch (err: any) {
      setError('Failed to load data. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      {/* Header */}
      <header className="bg-slate-900 border-b border-slate-800 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center gap-3">
            <Music2 className="w-8 h-8 text-blue-500" />
            <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-400 to-purple-500 bg-clip-text text-transparent">
              Mujica
            </h1>
            <span className="text-slate-400 text-sm">Music Cluster Visualization</span>
          </div>
        </div>
      </header>

      {/* Error Banner */}
      {error && (
        <div className="bg-red-500/10 border-b border-red-500/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <AlertCircle className="w-5 h-5 text-red-400 flex-shrink-0" />
                <p className="text-red-400 text-sm">{error}</p>
              </div>
              <button
                onClick={clearError}
                className="text-red-400 hover:text-red-300 text-sm font-medium"
              >
                Dismiss
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Sidebar - Upload */}
          <div className="lg:col-span-1 space-y-6">
            <div className="card">
              <h2 className="text-xl font-bold mb-4">Upload Music</h2>
              
              {/* Tabs */}
              <div className="flex gap-2 mb-6 bg-slate-800 p-1 rounded-lg">
                <button
                  onClick={() => setActiveTab('file')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'file'
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <div className="flex items-center justify-center gap-2">
                    <UploadIcon className="w-4 h-4" />
                    <span>File</span>
                  </div>
                </button>
                <button
                  onClick={() => setActiveTab('youtube')}
                  className={`flex-1 py-2 px-4 rounded-md text-sm font-medium transition-colors ${
                    activeTab === 'youtube'
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-400 hover:text-slate-200'
                  }`}
                >
                  <div className="flex items-center justify-center gap-2">
                    <Youtube className="w-4 h-4" />
                    <span>YouTube</span>
                  </div>
                </button>
              </div>

              {/* Upload Components */}
              {activeTab === 'file' ? <FileUpload /> : <YouTubeUpload />}
            </div>

            {/* Stats */}
            {clusterData && (
              <div className="card">
                <h3 className="text-lg font-bold mb-4">Statistics</h3>
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400">Total Songs</span>
                    <span className="text-2xl font-bold text-blue-500">
                      {clusterData.songs.length}
                    </span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-slate-400">Genres</span>
                    <span className="text-2xl font-bold text-purple-500">10</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Right - Visualization */}
          <div className="lg:col-span-2">
            <div className="card h-[calc(100vh-12rem)]">
              <DecagonViz key={clusterData?.songs.length || 0} />
            </div>
          </div>
        </div>
      </div>

      {/* Song Info Panel */}
      <SongPanel />

      {/* Footer */}
      <footer className="mt-16 py-6 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <p className="text-center text-sm text-slate-500">
            Built with ❤️ using BiLSTM Neural Networks and D3.js
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;