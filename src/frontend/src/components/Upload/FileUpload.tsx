/**
 * File upload component with drag-and-drop
 */

import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileAudio, X, Loader2 } from 'lucide-react';
import { useSongStore } from '../../store/useSongStore';
import apiService from '../../services/api';
import { isValidMp3File, formatFileSize } from '../../utils/helpers';

export function FileUpload() {
  const [isUploading, setIsUploading] = useState(false);
  const { addSong, setError } = useSongStore();

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    // Validate file
    if (!isValidMp3File(file)) {
      setError('Please upload a valid MP3 file');
      return;
    }

    // Check file size (max 50MB)
    if (file.size > 50 * 1024 * 1024) {
      setError('File size must be less than 50MB');
      return;
    }

    setIsUploading(true);
    setError(null);

    try {
      const song = await apiService.uploadMp3(file);
      addSong(song);  // Store automatically updates clusterData
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Failed to upload file');
    } finally {
      setIsUploading(false);
    }
  }, [addSong, setError]);

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    onDrop,
    accept: {
      'audio/mpeg': ['.mp3'],
    },
    multiple: false,
    disabled: isUploading,
  });

  return (
    <div className="w-full">
      <div
        {...getRootProps()}
        className={`
          border-2 border-dashed rounded-xl p-8 transition-all cursor-pointer
          ${isDragActive ? 'border-blue-500 bg-blue-500/10' : 'border-slate-700 hover:border-slate-600'}
          ${isUploading ? 'opacity-50 cursor-not-allowed' : ''}
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center justify-center gap-4 text-center">
          {isUploading ? (
            <>
              <Loader2 className="w-12 h-12 text-blue-500 animate-spin" />
              <div>
                <p className="text-lg font-medium text-slate-200">Processing...</p>
                <p className="text-sm text-slate-400 mt-1">Analyzing audio features</p>
              </div>
            </>
          ) : isDragActive ? (
            <>
              <Upload className="w-12 h-12 text-blue-500" />
              <p className="text-lg font-medium text-slate-200">Drop your file here</p>
            </>
          ) : (
            <>
              <FileAudio className="w-12 h-12 text-slate-400" />
              <div>
                <p className="text-lg font-medium text-slate-200">
                  Drag & drop an MP3 file
                </p>
                <p className="text-sm text-slate-400 mt-1">
                  or click to browse
                </p>
              </div>
              <p className="text-xs text-slate-500">Maximum file size: 50MB</p>
            </>
          )}
        </div>
      </div>

      {acceptedFiles.length > 0 && !isUploading && (
        <div className="mt-4 p-4 bg-slate-800 rounded-lg flex items-center justify-between">
          <div className="flex items-center gap-3">
            <FileAudio className="w-5 h-5 text-blue-500" />
            <div>
              <p className="text-sm font-medium text-slate-200">
                {acceptedFiles[0].name}
              </p>
              <p className="text-xs text-slate-400">
                {formatFileSize(acceptedFiles[0].size)}
              </p>
            </div>
          </div>
          <X className="w-5 h-5 text-slate-400" />
        </div>
      )}
    </div>
  );
}