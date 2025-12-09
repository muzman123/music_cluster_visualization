/**
 * D3.js Decagon Visualization Component
 * Displays songs in a 10-sided polygon based on genre probabilities
 */

import { useEffect, useRef } from 'react';
import * as d3 from 'd3';
import { useSongStore } from '../../store/useSongStore';
import { GENRE_COLORS, GENRES } from '../../types';
import type { Song, Vertex } from '../../types';

const WIDTH = 800;
const HEIGHT = 800;
const RADIUS = 300;
const CENTER_X = WIDTH / 2;
const CENTER_Y = HEIGHT / 2;

export function DecagonViz() {
  const svgRef = useRef<SVGSVGElement>(null);
  const { clusterData, selectedSong, setSelectedSong } = useSongStore();

  useEffect(() => {
    if (!svgRef.current || !clusterData) return;
    
    console.log('Rendering visualization with', clusterData.songs.length, 'songs');

    // Clear previous content
    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3.select(svgRef.current)
      .attr('viewBox', `0 0 ${WIDTH} ${HEIGHT}`)
      .attr('preserveAspectRatio', 'xMidYMid meet');

    // Create main group
    const g = svg.append('g');

    // Add zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.5, 3])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom);

    // Calculate vertex positions
    const vertices: Vertex[] = GENRES.map((genre, i) => {
      const angle = (i * 2 * Math.PI / 10) - (Math.PI / 2);
      return {
        genre,
        x: CENTER_X + RADIUS * Math.cos(angle),
        y: CENTER_Y + RADIUS * Math.sin(angle),
        angle,
        color: GENRE_COLORS[genre],
      };
    });

    // Draw decagon outline
    const lineGenerator = d3.line<Vertex>()
      .x(d => d.x)
      .y(d => d.y);

    g.append('path')
      .datum([...vertices, vertices[0]])
      .attr('d', lineGenerator)
      .attr('fill', 'none')
      .attr('stroke', '#475569')
      .attr('stroke-width', 2)
      .attr('stroke-dasharray', '5,5');

    // Draw radial lines from center to vertices
    vertices.forEach(vertex => {
      g.append('line')
        .attr('x1', CENTER_X)
        .attr('y1', CENTER_Y)
        .attr('x2', vertex.x)
        .attr('y2', vertex.y)
        .attr('stroke', '#334155')
        .attr('stroke-width', 1)
        .attr('stroke-dasharray', '3,3');
    });

    // Draw genre vertices
    const vertexGroup = g.selectAll('.vertex')
      .data(vertices)
      .enter()
      .append('g')
      .attr('class', 'vertex')
      .attr('transform', d => `translate(${d.x},${d.y})`);

    vertexGroup.append('circle')
      .attr('r', 20)
      .attr('fill', d => d.color)
      .attr('stroke', '#1e293b')
      .attr('stroke-width', 2);

    // Add genre labels
    vertexGroup.append('text')
      .attr('text-anchor', 'middle')
      .attr('dy', d => {
        const dy = d.y < CENTER_Y ? -30 : 35;
        return dy;
      })
      .attr('fill', '#e2e8f0')
      .attr('font-size', '14px')
      .attr('font-weight', 'bold')
      .attr('text-transform', 'uppercase')
      .text(d => d.genre);

    // Draw songs
    const songs = clusterData.songs;
    
    const songGroup = g.selectAll('.song')
      .data(songs)
      .enter()
      .append('g')
      .attr('class', 'song')
      .attr('transform', d => {
        const x = CENTER_X + d.position.x * RADIUS;
        const y = CENTER_Y + d.position.y * RADIUS;
        return `translate(${x},${y})`;
      })
      .style('cursor', 'pointer')
      .on('click', (event, d) => {
        event.stopPropagation();
        setSelectedSong(d);
      });

    // Song circles
    songGroup.append('circle')
      .attr('r', d => 5 + d.confidence * 8)
      .attr('fill', d => GENRE_COLORS[d.predicted_genre as keyof typeof GENRE_COLORS])
      .attr('stroke', d => selectedSong?.id === d.id ? '#fff' : 'none')
      .attr('stroke-width', 3)
      .attr('opacity', d => selectedSong?.id === d.id ? 1 : 0.8)
      .transition()
      .duration(500)
      .attr('r', d => 5 + d.confidence * 8);

    // Add hover effect
    songGroup.on('mouseenter', function(event, d) {
      d3.select(this).select('circle')
        .transition()
        .duration(200)
        .attr('r', 8 + d.confidence * 12)
        .attr('stroke', '#fff')
        .attr('stroke-width', 2);

      // Show tooltip
      const tooltip = g.append('g')
        .attr('class', 'tooltip')
        .attr('transform', () => {
          const x = CENTER_X + d.position.x * RADIUS;
          const y = CENTER_Y + d.position.y * RADIUS - 20;
          return `translate(${x},${y})`;
        });

      tooltip.append('rect')
        .attr('x', -80)
        .attr('y', -40)
        .attr('width', 160)
        .attr('height', 35)
        .attr('fill', '#1e293b')
        .attr('stroke', '#475569')
        .attr('stroke-width', 1)
        .attr('rx', 4);

      tooltip.append('text')
        .attr('text-anchor', 'middle')
        .attr('dy', -25)
        .attr('fill', '#e2e8f0')
        .attr('font-size', '12px')
        .attr('font-weight', 'bold')
        .text(d.title.length > 20 ? d.title.substring(0, 20) + '...' : d.title);

      tooltip.append('text')
        .attr('text-anchor', 'middle')
        .attr('dy', -10)
        .attr('fill', GENRE_COLORS[d.predicted_genre as keyof typeof GENRE_COLORS])
        .attr('font-size', '11px')
        .text(`${d.predicted_genre} (${(d.confidence * 100).toFixed(0)}%)`);
    })
    .on('mouseleave', function(event, d) {
      d3.select(this).select('circle')
        .transition()
        .duration(200)
        .attr('r', 5 + d.confidence * 8)
        .attr('stroke', selectedSong?.id === d.id ? '#fff' : 'none')
        .attr('stroke-width', selectedSong?.id === d.id ? 3 : 0);

      g.selectAll('.tooltip').remove();
    });

    // Click outside to deselect
    svg.on('click', () => setSelectedSong(null));

  }, [clusterData, selectedSong, setSelectedSong]); // Re-render when clusterData changes

  if (!clusterData) {
    return (
      <div className="w-full h-full flex items-center justify-center">
        <p className="text-slate-400">Upload a song to see the visualization</p>
      </div>
    );
  }

  return (
    <div className="w-full h-full flex items-center justify-center">
      <svg ref={svgRef} className="w-full h-full max-w-4xl max-h-[800px]" />
    </div>
  );
}