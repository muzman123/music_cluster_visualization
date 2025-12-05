/**
 * TypeScript type definitions for Mujica
 */

export interface GenreProbabilities {
  blues: number;
  classical: number;
  country: number;
  disco: number;
  hiphop: number;
  jazz: number;
  metal: number;
  pop: number;
  reggae: number;
  rock: number;
}

export interface Position {
  x: number;
  y: number;
}

export interface Song {
  id: number;
  title: string;
  source: 'upload' | 'youtube';
  source_url?: string;
  predicted_genre: string;
  confidence: number;
  probabilities: GenreProbabilities;
  position: Position;
  created_at: string;
  duration?: number;
}

export interface Vertex {
  genre: string;
  x: number;
  y: number;
  angle: number;
  color: string;
}

export interface ClusterData {
  vertices: Vertex[];
  songs: Song[];
}

export interface UploadProgress {
  fileName: string;
  progress: number;
  status: 'uploading' | 'processing' | 'complete' | 'error';
  error?: string;
}

export type GenreType = keyof GenreProbabilities;

export const GENRES: GenreType[] = [
  'blues',
  'classical',
  'country',
  'disco',
  'hiphop',
  'jazz',
  'metal',
  'pop',
  'reggae',
  'rock'
];

export const GENRE_COLORS: Record<GenreType, string> = {
  blues: '#4169E1',
  classical: '#DDA0DD',
  country: '#D2691E',
  disco: '#FF1493',
  hiphop: '#FF4500',
  jazz: '#FFD700',
  metal: '#2F4F4F',
  pop: '#FF69B4',
  reggae: '#32CD32',
  rock: '#8B0000'
};