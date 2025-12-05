/**
 * Song information panel component
 * Shows detailed genre breakdown when a song is selected
 */

import { X, Music, Calendar, Trash2 } from 'lucide-react';
import { useSongStore } from '../../store/useSongStore';
import apiService from '../../services/api';
import { GENRE_COLORS, GENRES } from '../../types';
import { formatPercentage, formatDate, getGenreDisplayName, formatDuration } from '../../utils/helpers';

export function SongPanel() {
  const { selectedSong, setSelectedSong, removeSong, setError } = useSongStore();

  if (!selectedSong) return null;

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this song?')) return;

    try {
      await apiService.deleteSong(selectedSong.id);
      removeSong(selectedSong.id);
      setSelectedSong(null);
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Failed to delete song');
    }
  };

  // Sort probabilities by value
  const sortedGenres = [...GENRES].sort((a, b) => {
    return selectedSong.probabilities[b] - selectedSong.probabilities[a];
  });

  return (
    <div className="fixed right-0 top-0 h-full w-full md:w-96 bg-slate-900 border-l border-slate-800 shadow-2xl z-50 overflow-y-auto">
      {/* Header */}
      <div className="sticky top-0 bg-slate-900 border-b border-slate-800 p-6 flex items-start justify-between">
        <div className="flex-1">
          <h2 className="text-xl font-bold text-slate-100 mb-1">
            {selectedSong.title}
          </h2>
          <p className="text-sm text-slate-400 flex items-center gap-2">
            <Music className="w-4 h-4" />
            {selectedSong.source === 'youtube' ? 'YouTube' : 'Uploaded File'}
          </p>
        </div>
        <button
          onClick={() => setSelectedSong(null)}
          className="text-slate-400 hover:text-slate-200 transition-colors"
        >
          <X className="w-6 h-6" />
        </button>
      </div>

      {/* Content */}
      <div className="p-6 space-y-6">
        {/* Primary Genre */}
        <div>
          <h3 className="text-sm font-medium text-slate-400 mb-3">Primary Genre</h3>
          <div 
            className="p-4 rounded-lg border-2 flex items-center justify-between"
            style={{
              backgroundColor: `${GENRE_COLORS[selectedSong.predicted_genre as keyof typeof GENRE_COLORS]}15`,
              borderColor: GENRE_COLORS[selectedSong.predicted_genre as keyof typeof GENRE_COLORS],
            }}
          >
            <span className="text-lg font-bold" style={{
              color: GENRE_COLORS[selectedSong.predicted_genre as keyof typeof GENRE_COLORS]
            }}>
              {getGenreDisplayName(selectedSong.predicted_genre as any)}
            </span>
            <span className="text-2xl font-bold" style={{
              color: GENRE_COLORS[selectedSong.predicted_genre as keyof typeof GENRE_COLORS]
            }}>
              {formatPercentage(selectedSong.confidence)}
            </span>
          </div>
        </div>

        {/* All Genre Probabilities */}
        <div>
          <h3 className="text-sm font-medium text-slate-400 mb-3">Genre Breakdown</h3>
          <div className="space-y-2">
            {sortedGenres.map(genre => {
              const probability = selectedSong.probabilities[genre];
              const color = GENRE_COLORS[genre];
              
              return (
                <div key={genre} className="space-y-1">
                  <div className="flex items-center justify-between text-sm">
                    <span className="text-slate-300">{getGenreDisplayName(genre)}</span>
                    <span className="text-slate-400 font-medium">
                      {formatPercentage(probability)}
                    </span>
                  </div>
                  <div className="h-2 bg-slate-800 rounded-full overflow-hidden">
                    <div
                      className="h-full rounded-full transition-all duration-500"
                      style={{
                        width: `${probability * 100}%`,
                        backgroundColor: color,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Metadata */}
        <div>
          <h3 className="text-sm font-medium text-slate-400 mb-3">Details</h3>
          <div className="space-y-3">
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-400">Position</span>
              <span className="text-slate-200 font-mono">
                ({selectedSong.position.x.toFixed(2)}, {selectedSong.position.y.toFixed(2)})
              </span>
            </div>
            {selectedSong.duration && (
              <div className="flex items-center justify-between text-sm">
                <span className="text-slate-400">Duration</span>
                <span className="text-slate-200">{formatDuration(selectedSong.duration)}</span>
              </div>
            )}
            <div className="flex items-center justify-between text-sm">
              <span className="text-slate-400 flex items-center gap-2">
                <Calendar className="w-4 h-4" />
                Added
              </span>
              <span className="text-slate-200">{formatDate(selectedSong.created_at)}</span>
            </div>
            {selectedSong.source_url && (
              <div className="flex flex-col gap-1">
                <span className="text-slate-400 text-sm">Source</span>
                <a
                  href={selectedSong.source_url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-400 hover:text-blue-300 text-sm truncate"
                >
                  {selectedSong.source_url}
                </a>
              </div>
            )}
          </div>
        </div>

        {/* Actions */}
        <div className="pt-4 border-t border-slate-800">
          <button
            onClick={handleDelete}
            className="btn btn-danger w-full flex items-center justify-center gap-2"
          >
            <Trash2 className="w-4 h-4" />
            <span>Delete Song</span>
          </button>
        </div>
      </div>
    </div>
  );
}