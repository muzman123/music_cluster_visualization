"""
Decagon position calculator service
Calculates song positions in the 10-sided polygon based on genre probabilities
"""

import math
import numpy as np
from app.config import GENRE_ORDER


def calculate_decagon_position(probabilities: np.ndarray) -> tuple[float, float]:
    """
    Calculate song position in decagon based on genre probabilities.
    
    Args:
        probabilities: Array of 10 probabilities (sum to 1.0) in GENRE_ORDER
    
    Returns:
        (x, y) coordinates in range approximately [-1, 1]
    """
    # Calculate vertex positions (unit circle)
    # Start from top and go clockwise
    vertices = []
    for i in range(10):
        # Angle for each vertex (starting from top, going clockwise)
        angle = (i * 2 * math.pi / 10) - (math.pi / 2)
        x = math.cos(angle)
        y = math.sin(angle)
        vertices.append((x, y))
    
    # Calculate weighted position based on probabilities
    song_x = sum(prob * vertices[i][0] for i, prob in enumerate(probabilities))
    song_y = sum(prob * vertices[i][1] for i, prob in enumerate(probabilities))
    
    # Scale down to 80% of radius to keep songs inside decagon
    scale_factor = 0.8
    song_x *= scale_factor
    song_y *= scale_factor
    
    return (song_x, song_y)


def get_vertex_positions():
    """
    Get all vertex positions for the decagon visualization
    
    Returns:
        List of dicts with genre, x, y, angle, and color
    """
    from app.config import GENRE_COLORS
    
    vertices = []
    for i, genre in enumerate(GENRE_ORDER):
        angle = (i * 2 * math.pi / 10) - (math.pi / 2)
        x = math.cos(angle)
        y = math.sin(angle)
        
        vertices.append({
            'genre': genre,
            'x': x,
            'y': y,
            'angle': angle,
            'color': GENRE_COLORS[genre]
        })
    
    return vertices