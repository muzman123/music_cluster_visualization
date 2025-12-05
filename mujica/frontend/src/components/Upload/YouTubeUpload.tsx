/**
 * YouTube URL upload component
 */

import { useState } from 'react';
import { Youtube, Loader2, AlertCircle } from 'lucide-react';
import { useSongStore } from '../../store/useSongStore';
import apiService from '../../services/api';
import { isValidYouTubeUrl } from '../../utils/helpers';

export function YouTubeUpload() {
  const [url, setUrl] = useState('');
  const [isUploading, setIsUploading] = useState(false);
  const [localError, setLocalError] = useState<string | null>(null);
  const { addSong, setError } = useSongStore();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!url.trim()) {
      setLocalError('Please enter a YouTube URL');
      return;
    }

    if (!isValidYouTubeUrl(url)) {
      setLocalError('Please enter a valid YouTube URL');
      return;
    }

    setIsUploading(true);
    setLocalError(null);
    setError(null);

    try {
      const song = await apiService.uploadYoutube(url);
      addSong(song);  // Store automatically updates clusterData
      setUrl('');
    } catch (error: any) {
      const errorMsg = error.response?.data?.detail || 'Failed to process YouTube URL';
      setLocalError(errorMsg);
      setError(errorMsg);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="w-full">
      <form onSubmit={handleSubmit} className="space-y-4">
        <div className="relative">
          <div className="absolute left-4 top-1/2 -translate-y-1/2">
            <Youtube className="w-5 h-5 text-slate-400" />
          </div>
          <input
            type="text"
            value={url}
            onChange={(e) => {
              setUrl(e.target.value);
              setLocalError(null);
            }}
            placeholder="Paste YouTube URL here..."
            className="input pl-12"
            disabled={isUploading}
          />
        </div>

        {localError && (
          <div className="flex items-center gap-2 px-4 py-3 bg-red-500/10 border border-red-500/50 rounded-lg text-red-400 text-sm">
            <AlertCircle className="w-4 h-4 flex-shrink-0" />
            <p>{localError}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={isUploading || !url.trim()}
          className="btn btn-primary w-full flex items-center justify-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          {isUploading ? (
            <>
              <Loader2 className="w-5 h-5 animate-spin" />
              <span>Downloading & Processing...</span>
            </>
          ) : (
            <>
              <Youtube className="w-5 h-5" />
              <span>Download & Analyze</span>
            </>
          )}
        </button>
      </form>

      <div className="mt-4 text-xs text-slate-500 space-y-1">
        <p>• Supports most YouTube music videos</p>
        <p>• Processing may take 30-60 seconds</p>
        <p>• Audio will be downloaded and analyzed automatically</p>
      </div>
    </div>
  );
}