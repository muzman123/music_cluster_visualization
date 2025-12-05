/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'genre-blues': '#4169E1',
        'genre-classical': '#DDA0DD',
        'genre-country': '#D2691E',
        'genre-disco': '#FF1493',
        'genre-hiphop': '#FF4500',
        'genre-jazz': '#FFD700',
        'genre-metal': '#2F4F4F',
        'genre-pop': '#FF69B4',
        'genre-reggae': '#32CD32',
        'genre-rock': '#8B0000',
      },
    },
  },
  plugins: [],
}