import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';

export default function MapOverlay({ routeCoordinates, height = '400px' }) {
  const mapRef = useRef(null);
  const mapInstance = useRef(null);
  const routeLayer = useRef(null);

  useEffect(() => {
    if (!mapInstance.current && mapRef.current) {
      mapInstance.current = L.map(mapRef.current, { zoomControl: false }).setView([12.9716, 77.5946], 13);
      
      // Use CartoDB Dark Matter for the premium dark mode look
      L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
        attribution: '&copy; OpenStreetMap contributors &copy; CARTO'
      }).addTo(mapInstance.current);
    }

    if (mapInstance.current && routeCoordinates && routeCoordinates.length > 0) {
      const routeKey = JSON.stringify(routeCoordinates);
      if (mapInstance.current._lastRouteKey === routeKey) return;
      mapInstance.current._lastRouteKey = routeKey;

      if (routeLayer.current) {
        mapInstance.current.removeLayer(routeLayer.current);
      }

      const latlngs = routeCoordinates.map(c => [c.lat, c.lng]);
      
      routeLayer.current = L.polyline(latlngs, {
        color: '#3b82f6',
        weight: 6,
        opacity: 0.8,
        lineCap: 'round',
        lineJoin: 'round'
      }).addTo(mapInstance.current);

      try {
        mapInstance.current.fitBounds(routeLayer.current.getBounds(), { padding: [50, 50] });
      } catch (e) {}
    }
  }, [routeCoordinates]);

  return (
    <div 
      ref={mapRef} 
      style={{ height, width: '100%', borderRadius: '12px', zIndex: 1 }} 
      className="border border-slate-700 shadow-inner"
    />
  );
}
