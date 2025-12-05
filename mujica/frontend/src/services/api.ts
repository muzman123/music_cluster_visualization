/**
 * API service for communicating with the Mujica backend
 */

import axios from 'axios';
import type { Song, ClusterData } from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const apiService = {
  /**
   * Upload an MP3 file
   */
  async uploadMp3(file: File): Promise<Song> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post<Song>('/upload/mp3', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });

    return response.data;
  },

  /**
   * Process a YouTube URL
   */
  async uploadYoutube(url: string): Promise<Song> {
    const response = await api.post<Song>('/upload/youtube', { url });
    return response.data;
  },

  /**
   * Get all songs
   */
  async getSongs(params?: {
    limit?: number;
    offset?: number;
    genre?: string;
  }): Promise<{ songs: Song[]; total: number; limit: number; offset: number }> {
    const response = await api.get('/songs', { params });
    return response.data;
  },

  /**
   * Get a specific song
   */
  async getSong(id: number): Promise<Song> {
    const response = await api.get<Song>(`/songs/${id}`);
    return response.data;
  },

  /**
   * Delete a song
   */
  async deleteSong(id: number): Promise<void> {
    await api.delete(`/songs/${id}`);
  },

  /**
   * Get cluster visualization data
   */
  async getClusterData(): Promise<ClusterData> {
    const response = await api.get<ClusterData>('/cluster-data');
    return response.data;
  },

  /**
   * Health check
   */
  async healthCheck(): Promise<{
    status: string;
    model_loaded: boolean;
    db_connected: boolean;
  }> {
    const response = await api.get('/health');
    return response.data;
  },
};

export default apiService;