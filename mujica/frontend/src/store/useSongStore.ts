/**
 * Zustand store for managing song state
 */

import { create } from 'zustand';
import type { Song, ClusterData, UploadProgress } from '../types';

interface SongStore {
  // State
  songs: Song[];
  clusterData: ClusterData | null;
  selectedSong: Song | null;
  uploadProgress: UploadProgress | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  setSongs: (songs: Song[]) => void;
  addSong: (song: Song) => void;
  removeSong: (id: number) => void;
  setSelectedSong: (song: Song | null) => void;
  setClusterData: (data: ClusterData) => void;
  setUploadProgress: (progress: UploadProgress | null) => void;
  setLoading: (loading: boolean) => void;
  setError: (error: string | null) => void;
  clearError: () => void;
}

export const useSongStore = create<SongStore>((set) => ({
  // Initial state
  songs: [],
  clusterData: null,
  selectedSong: null,
  uploadProgress: null,
  isLoading: false,
  error: null,

  // Actions
  setSongs: (songs) => set({ songs }),
  
  addSong: (song) => set((state) => {
    // Create a completely new clusterData object to force re-render
    const newClusterData = state.clusterData ? {
      vertices: state.clusterData.vertices,
      songs: [song, ...state.clusterData.songs]
    } : null;
    
    return {
      songs: [song, ...state.songs],
      clusterData: newClusterData
    };
  }),
  
  removeSong: (id) => set((state) => {
    // Create new clusterData object to force re-render
    const newClusterData = state.clusterData ? {
      vertices: state.clusterData.vertices,
      songs: state.clusterData.songs.filter((s) => s.id !== id)
    } : null;
    
    return {
      songs: state.songs.filter((s) => s.id !== id),
      clusterData: newClusterData,
      selectedSong: state.selectedSong?.id === id ? null : state.selectedSong
    };
  }),
  
  setSelectedSong: (song) => set({ selectedSong: song }),
  
  setClusterData: (data) => set({ clusterData: data, songs: data.songs }),
  
  setUploadProgress: (progress) => set({ uploadProgress: progress }),
  
  setLoading: (loading) => set({ isLoading: loading }),
  
  setError: (error) => set({ error }),
  
  clearError: () => set({ error: null }),
}));